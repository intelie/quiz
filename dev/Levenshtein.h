#ifndef _Levenshtein_h
#define _Levenshtein_h

#include <QString>
#include <QVector>



class Levenshtein
{
    public:
        static int distance(const QString& first, const QString& second);
};

#endif
