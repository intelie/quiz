# -*- coding: utf-8 -*-

import unicodedata
import re


def validate(data):
    if not "items" in data:
        if "error" in data:
            raise RuntimeError(data["error"]["message"])

        raise RuntimeError("No results found with given keyword")


def strip_accents(string):
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
