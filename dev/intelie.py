# -*- coding: utf-8 -*-

import unicodedata
import urllib
import json
import sys
import re

API_KEY = "AIzaSyDUMMY3a9Tom3E1Y0umyESKXPFvCqi_X38"


def validate_result(data):
    if not "items" in data:
        if "error" in data:
            raise RuntimeError(data["error"]["message"])

        raise RuntimeError("No results found with given keyword")


def strip_accents(string):
    if type(string) is not unicode:
        string = unicode(string, 'utf-8')

    def normalize(s):
        return unicodedata.normalize('NFD', s)

    def category(c):
        return unicodedata.category(c)

    return ''.join((c for c in normalize(string) if category(c) != 'Mn'))


def normalize_string(string):
    string = strip_accents(string).lower()
    string = re.sub("[^A-Za-z0-9\s]", "", string)

    return string


def levenshtein(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def count_words(keyword, title):
    counter = 0

    for word in title.split():
        if levenshtein(keyword, word) <= 2:
            counter += 1

    return counter


def google_search(keyword):
    url = "https://www.googleapis.com/customsearch/v1?" \
        "key=" + API_KEY + "&" \
        "cx=017576662512468239146:omuauf_lfve&" \
        "q=" + keyword
    content = urllib.urlopen(url)
    return json.loads(content.read())


if __name__ == '__main__':
    argv = sys.argv[1:]

    if len(argv) < 1:
        print "\n\tUsage: python intelie.py keyword\n"
        sys.exit(-1)

    keyword = " ".join(argv)
    google_result = google_search(keyword)

    try:
        validate_result(google_result)
    except RuntimeError as e:
        print e
        sys.exit(-1)

    counter = 0
    keyword = normalize_string(keyword)

    print 'Titles:'
    for item in google_result['items']:
        print "\t- " + item['title']

        counter += count_words(keyword, normalize_string(item['title']))

    print 'Total words counts: %s' % counter
