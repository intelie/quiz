
#include "NetworkAccessManager.h"



NetworkAccessManager::NetworkAccessManager(QObject *parent)
: QNetworkAccessManager(parent)
{
}

QNetworkReply *NetworkAccessManager::createRequest(QNetworkAccessManager::Operation operation, const QNetworkRequest &request, QIODevice *outgoingData)
{
    QNetworkRequest localRequest = request;
    QNetworkProxy localProxy = QNetworkProxy::applicationProxy();

    if (localProxy.type() != QNetworkProxy::NoProxy) {
        QString authCredentials = QString("%1:%2")
                                        .arg(localProxy.user())
                                        .arg(localProxy.password());

        localRequest.setRawHeader("Proxy-Authorization", QByteArray("Basic ") + authCredentials.toLocal8Bit().toBase64());
    }

    localRequest.setRawHeader("User-Agent", "Skhaz Crawler 1.0");
    localRequest.setAttribute(QNetworkRequest::HttpPipeliningAllowedAttribute, true);
    localRequest.setAttribute(QNetworkRequest::CacheLoadControlAttribute, QNetworkRequest::AlwaysNetwork);

    return QNetworkAccessManager::createRequest(operation, localRequest, outgoingData);
}
