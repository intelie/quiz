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
        void searchNext(quint32 index = 0);

    protected slots:
        void finished();
        void error(QNetworkReply::NetworkError error);
        void handleDone();

    signals:
        void done();

    private:
        Q_OBJECT

        static QString GOOGLE_API;

        NetworkAccessManager manager;
        QList<QFuture<QList<QPair<int, QString> > > > futures;
        QString currentQuery;
        int currentIndex;
};

#endif
