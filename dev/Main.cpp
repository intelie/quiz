
#include "Crawler.h"



int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    if (app.arguments().count() < 2) {
        qWarning() << "The query is empty!";
        return -1;
    }

    Crawler crawler;
    crawler.search(app.arguments()[1]);
    return app.exec();
}
