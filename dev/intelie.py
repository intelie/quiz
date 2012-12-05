# -*- coding: utf-8 -*-

def validate(data):
    if not "items" in data:
        if "error" in data:
            raise RuntimeError(data["error"]["message"])

        raise RuntimeError("No results found with given keyword")
