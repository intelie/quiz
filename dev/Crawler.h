#ifndef _Crawler_h
#define _Crawler_h

#include <QtCore>
#include <QtNetwork>
#include <QtConcurrent/QtConcurrent>
#include "NetworkAccessManager.h"
#include "Levenshtein.h"



class Crawler : public QObject
{
    public:
        explicit Crawler(QObject *parent = 0);

    public slots:
        void search(const QString& query);

    protected slots:
        void finished();
        void error(QNetworkReply::NetworkError error);
        void handleDone();
        void nextDownload();

    signals:
        void done();

    private:
        Q_OBJECT

        static QString GOOGLE_API;
        static int MAX_CONCURRENT_REQUESTS;

        NetworkAccessManager manager;
        QList<QUrl> urls;
        QList<QFuture<QList<QPair<int, QString> > > > futures;
        QString currentQuery;
        int activeDownloads;
};

#endif
