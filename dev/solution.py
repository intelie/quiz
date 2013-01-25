import requests
from bs4 import BeautifulSoup
import sys


def levenshtein(s, t):
    '''
    Iterative with Dynamic Programming implementation of Levenshtein distance.
    See: http://www.algorithmist.com/index.php/Edit_Distance#Dynamic_Programming_Approach
    '''
    m = len(s) + 1
    n = len(t) + 1
    from_0_to_m = range(m)
    from_0_to_n = range(n)
    d = [[0] * n for _ in from_0_to_m]

    for i in from_0_to_m:
        d[i][0] = i
    for j in from_0_to_n:
        d[0][j] = j

    from_1_to_m = from_0_to_m[1:]
    from_1_to_n = from_0_to_n[1:]
    for j in from_1_to_n:
        for i in from_1_to_m:
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]  # no op
            else:
                d[i][j] = min(
                    d[i - 1][j] + 1,      # a deletion
                    d[i][j - 1] + 1,      # an insertion
                    d[i - 1][j - 1] + 1,  # a substitution
                )
    return d[m - 1][n - 1]


def count_word(word, words):
    return len([x for x in words if x == word])


def count_word_with_distance(word, words):
    count = 0
    for x in words:
        if x != word and levenshtein(x, word) < 2:
            count += 1
    return count


def titles(query, limit):
    search_url = 'http://www.google.com/search'
    search_params = {'btnG': 'Google Search'}
    search_params['q'] = query

    for start in xrange(0, limit, 10):
        search_params['start'] = start
        html_doc = requests.get(search_url, params=search_params).text
        soup = BeautifulSoup(html_doc)
        h3_tags = soup.find_all('h3', class_='r')[:10]

        if len(h3_tags) == 0:
            raise StopIteration

        for h3 in h3_tags:
            yield " ".join(h3.contents[0].stripped_strings)


def main(word, limit=10):
    word = word.lower()
    count = 0
    all_titles = []
    for title in titles(word, limit):
        all_titles.append(title)
        title = title.lower()
        words = title.split()
        count += count_word(word, words) + count_word_with_distance(word, words)

    for title in all_titles:
        print title
    print count

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) > 2:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print 'missing operand'
        print 'Please give a name to search for.'
