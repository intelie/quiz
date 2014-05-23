#ifndef StringUtils_H_
#define StringUtils_H_

#include <string>

class StringUtils
{
public:
    explicit StringUtils() {};
    virtual ~StringUtils() {};

    static size_t getLevenshteinDistance(const std::string &s1, const std::string &s2);
    static int countLevenshteinOccurrencesWithMaxDistance(std::string _text, std::string _match, int _max);
    static void testLevenshteinDistance();
};

#endif
