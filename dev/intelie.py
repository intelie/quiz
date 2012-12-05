# -*- coding: utf-8 -*-

import unicodedata

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
