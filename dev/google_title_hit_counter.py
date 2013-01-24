#coding:utf-8
import re
import json
import requests
from urllib import urlencode

GOOGLE_SEARCH_API_URL = 'https://ajax.googleapis.com/ajax/services/search/web'

def make_google_api_request(search_term):
    """
    Make google request and return a python dict as the json response
    """
    querystring = urlencode({'v': '1.0', 'q': search_term})

    url = GOOGLE_SEARCH_API_URL + '?' + querystring
    response = requests.get(url)

    return json.loads(response.content)


def get_titles(json_dict):
    """
    Filter and sanitize the result's titles removing the HTML markup tags
    """
    results = json_dict['responseData']['results']
    return [re.sub('<(.*?)>', '', r['title']) for r in results]


def levenhtein_distance_calc(word1, word2):
    """
    Calculate the Levenhtein distance beetween two words. Based on this algorithm:
    http://en.wikipedia.org/wiki/Levenshtein_distance#Computing_Levenshtein_distance
    """
    if not (word1 and word2):
        return max(len(word1), len(word2))

    cost = 0
    if word1[-1] != word2[-1]:
        cost += 1

    return min([
        levenhtein_distance_calc(word1[0:-1], word2) + 1,
        levenhtein_distance_calc(word1, word2[0:-1]) + 1,
        levenhtein_distance_calc(word1[0:-1], word2[0:-1]) + cost,
    ])


def count_word_occurrences(title, search_word):
    """
    Given a title and a word, counts its occurrences in the title
    """
    counter = 0

    title_words = [word.lower() for word in title.split(' ') if word.isalpha()]
    for word in title_words:
        if levenhtein_distance_calc(word, search_word) <= 2:
            counter += 1

    return counter


if __name__ == '__main__':
    search_term = unicode(raw_input('Digite o termo que você deseja procurar: '), 'utf-8')
    json_dict = make_google_api_request(search_term)
    titles = get_titles(json_dict)

    total_counter = 0
    for title in titles:
        total_counter += count_word_occurrences(title, search_term)

    print "\nO termo %s foi encontrado %d vezes em %d resultados" % (search_term, total_counter, len(titles))
