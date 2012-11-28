
#include "Crawler.h"




QString Crawler::GOOGLE_API = QString("http://ajax.googleapis.com/ajax/services/search/web?v=2.0&rsz=8");

Crawler::Crawler(QObject *parent)
: QObject(parent)
{
    QThreadPool::globalInstance()
        ->setMaxThreadCount(8);

    connect(this, SIGNAL(done()), SLOT(handleDone()));
}

void Crawler::search(const QString& query)
{
    currentQuery = query;
    searchNext();
}

void Crawler::searchNext(quint32 index)
{
    currentIndex = index;
    QString url = QString("%1&q=%2&start=%3")
                    .arg(GOOGLE_API)
                    .arg(currentQuery)
                    .arg(currentIndex);

    QNetworkRequest request(url);
    QNetworkReply *reply = manager.get(request);

    connect(reply, SIGNAL(finished()), SLOT(finished()));
    connect(reply, SIGNAL(error(QNetworkReply::NetworkError)), SLOT(error(QNetworkReply::NetworkError)));
}

void Crawler::finished()
{
    // Warning: Verbosity ahead
    if (QNetworkReply *reply = qobject_cast<QNetworkReply *>(sender())) {
        QJsonParseError parseError;
        QJsonObject object = QJsonDocument::fromJson(reply->readAll(), &parseError).object();
        reply->deleteLater();

        if (parseError.error != QJsonParseError::NoError) {
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
        searchNext(currentIndex + 1);
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
