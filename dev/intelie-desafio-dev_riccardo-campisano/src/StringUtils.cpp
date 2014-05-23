#include "StringUtils.h"
#include <algorithm>
#include <iostream>

// from http://rosettacode.org/wiki/Levenshtein_distance#C.2B.2B

size_t StringUtils::getLevenshteinDistance(const std::string &s1, const std::string &s2)
{
  const size_t m(s1.size());
  const size_t n(s2.size());

  if( m==0 ) return n;
  if( n==0 ) return m;

  size_t *costs = new size_t[n + 1];

  for( size_t k=0; k<=n; k++ ) costs[k] = k;

  size_t i = 0;
  for ( std::string::const_iterator it1 = s1.begin(); it1 != s1.end(); ++it1, ++i )
  {
    costs[0] = i+1;
    size_t corner = i;

    size_t j = 0;
    for ( std::string::const_iterator it2 = s2.begin(); it2 != s2.end(); ++it2, ++j )
    {
      size_t upper = costs[j+1];
      if( *it1 == *it2 )
      {
		  costs[j+1] = corner;
	  }
      else
	  {
		size_t t(upper<corner?upper:corner);
        costs[j+1] = (costs[j]<t?costs[j]:t)+1;
	  }

      corner = upper;
    }
  }

  size_t result = costs[n];
  delete [] costs;

  return result;
}

int StringUtils::countLevenshteinOccurrencesWithMaxDistance(std::string _text, std::string _match, int _max)
{
    int count = 0;

    if(_text.length() > 0 &&
       _match.length() > 0 &&
       _max >= 0)
    {
        std::string::iterator it;
        std::string partial_text;
        int distance;
        int match_len = _match.length();

        for (it=_text.begin() ; it!=_text.end(); it++)
        {
            if ((_text.end() - 1) - it >= match_len)
            {
                partial_text = std::string(it, it + match_len);
            }
            else
            {
                partial_text = std::string(it, _text.end()-1);
            }

            distance = StringUtils::getLevenshteinDistance(partial_text, _match);

            if(distance<=_max)
            {
                ++count;

                if((it + match_len) >=_text.end())
                {
                    break;
                }

                it += match_len;
            }
        }
    }

    return count;
}

void StringUtils::testLevenshteinDistance()
{
    std::cout << "getLevenshteinDistance('', '') = 0 = " <<
        StringUtils::getLevenshteinDistance("", "") << std::endl;

    std::cout << "getLevenshteinDistance('', 'a') = 1 = " <<
        StringUtils::getLevenshteinDistance("", "a") << std::endl;

    std::cout << "getLevenshteinDistance('aaapppp', '') = 7 = " <<
        StringUtils::getLevenshteinDistance("aaapppp", "") << std::endl;

    std::cout << "getLevenshteinDistance('frog', 'fog') = 1 = " <<
        StringUtils::getLevenshteinDistance("frog", "fog") << std::endl;

    std::cout << "getLevenshteinDistance('fly', 'ant') = 3 = " <<
        StringUtils::getLevenshteinDistance("fly", "ant") << std::endl;

    std::cout << "getLevenshteinDistance('elephant', 'hippo') = 7 = " <<
        StringUtils::getLevenshteinDistance("elephant", "hippo") << std::endl;

    std::cout << "getLevenshteinDistance('hippo', 'elephant') = 7 = " <<
        StringUtils::getLevenshteinDistance("hippo", "elephant") << std::endl;

    std::cout << "getLevenshteinDistance('hippo', 'zzzzzzzz') = 8 = " <<
        StringUtils::getLevenshteinDistance("hippo", "zzzzzzzz") << std::endl;

    std::cout << "getLevenshteinDistance('hello', 'hallo') = 1 = " <<
        StringUtils::getLevenshteinDistance("hello", "hallo") << std::endl;
}
