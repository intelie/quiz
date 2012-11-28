#ifndef _NetworkAccessManager_h
#define _NetworkAccessManager_h

#include <QNetworkAccessManager>
#include <QNetworkProxy>
#include <QAuthenticator>
#include <QNetworkRequest>



class NetworkAccessManager : public QNetworkAccessManager
{
    public:
        explicit NetworkAccessManager(QObject *parent = 0);

    protected:
        virtual QNetworkReply *createRequest(QNetworkAccessManager::Operation operation, const QNetworkRequest &request, QIODevice *outgoingData = 0);

    private:
        Q_OBJECT
};

#endif
