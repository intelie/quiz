
#include "Crawler.h"



QString Crawler::GOOGLE_API = QString("http://ajax.googleapis.com/ajax/services/search/web?v=2.0");
int Crawler::MAX_CONCURRENT_REQUESTS = 8;

Crawler::Crawler(QObject *parent)
: QObject(parent)
{
    activeDownloads = 0;
    QThreadPool::globalInstance()
        ->setMaxThreadCount(MAX_CONCURRENT_REQUESTS);

    connect(this, SIGNAL(done()), this, SLOT(handleDone()));
}

void Crawler::search(const QString& query)
{
    currentQuery = query;

    for (int i = 0; i <= MAX_CONCURRENT_REQUESTS * 100; i += MAX_CONCURRENT_REQUESTS) {
        urls << QString("%1&rsz=%2&q=%3&start=%4")
                    .arg(GOOGLE_API)
                    .arg(MAX_CONCURRENT_REQUESTS)
                    .arg(query)
                    .arg(i);
    }

    nextDownload();
}

void Crawler::finished()
{
    // Warning: Verbosity ahead
    if (QNetworkReply *reply = qobject_cast<QNetworkReply *>(sender())) {
        activeDownloads--;
        QJsonParseError parseError;
        QJsonObject object = QJsonDocument::fromJson(reply->readAll(), &parseError).object();
        reply->deleteLater();

        if (parseError.error != QJsonParseError::NoError) {
            qWarning(qPrintable(parseError.errorString()));
            emit done();
            return;
        }

        QVariant responseData = object.toVariantMap()["responseData"];
        if (responseData.isNull()) {
            // When responseData is null, the search reached the end
            emit done();
            return;
        }

        QVariantList results = responseData.toMap()["results"].toList();
        QStringList titles;
        foreach (QVariant result, results) {
            QVariantMap resultMap = result.toMap();
            titles << resultMap["title"].toString();
        }

        // Concurrent process data
        futures << QtConcurrent::run([=] () -> QList<QPair<int, QString> > {
            QList<QPair<int, QString> > result;
            const QRegExp re("[\\s.-_\"']");

            foreach (QString title, titles) {
                quint32 count = 0;
                title.replace(QRegExp("<[^>]*>"), QLatin1String(""));
                QStringList words = title.split(re, QString::SkipEmptyParts);
                foreach (QString word, words) {
                    int distance = Levenshtein::distance(currentQuery, word);
                    if (distance <= 2) {
                        count++;
                    }
                }

                result << qMakePair<int, QString>(count, title);
            }

            return result;
        });

        // Keep looking for more results
        nextDownload();
    }
}

void Crawler::error(QNetworkReply::NetworkError error)
{
    if (error != QNetworkReply::NoError) {
        QString errorValue;
        QMetaObject meta = QNetworkReply::staticMetaObject;
        for (int i=0; i < meta.enumeratorCount(); ++i) {
            QMetaEnum m = meta.enumerator(i);
            if (m.name() == QLatin1String("NetworkError")) {
                errorValue = QLatin1String(m.valueToKey(error));
                break;
            }
        }

        qWarning(qPrintable(errorValue));
        emit done();
    }
}

void Crawler::handleDone()
{
    disconnect(this, SIGNAL(done()), this, SLOT(handleDone()));

    // Wait for all threads to complete
    int occurences = 0;
    foreach (auto future, futures) {
        future.waitForFinished();
        foreach (auto result, future.result()) {
            occurences += result.first;

            qDebug()
                << "count"
                << result.first
                << "title"
                << result.second;
        }
    }

    qDebug() << "Total occurences:" << occurences;

    // All done
    QCoreApplication::exit();
}

void Crawler::nextDownload()
{
    while (activeDownloads < MAX_CONCURRENT_REQUESTS) {
        activeDownloads++;
        if (urls.empty()) {
            qDebug("urls is empty");
            emit done();
            return;
        }

        QUrl url = urls.takeFirst();
        QNetworkRequest request(url);
        QNetworkReply *reply = manager.get(request);

        connect(reply, SIGNAL(finished()), SLOT(finished()));
        connect(reply, SIGNAL(error(QNetworkReply::NetworkError)), SLOT(error(QNetworkReply::NetworkError)));
    }
}
