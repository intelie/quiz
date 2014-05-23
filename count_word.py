#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
import json
import sys

def search_word(word):
    """ Search given word on google and return the result as json"""
    
    google_api_key = "AIzaSyB0hnPmSMA_EHOnQJgkp9Bs3JIVAGmUjWs"
    url = "https://www.googleapis.com/customsearch/v1?key="
    parameters = "&cx=017576662512468239146:omuauf_lfve&q="
    query = word
    
    output = urlopen(url + google_api_key + parameters + query)
    
    return json.loads(output.read())


def count_word(word, data):
    """ Count how many times one word appear on line """
    c = 0
    for l in data.split():
        if word.lower() == l.lower():
            c += 1
    return c 
    
    
def levenshtein(string1, string2):
    """ Compare two strings and return the levenshtein diference """
    len_st1 = len(string1)
    len_st2 = len(string2)
    
    if len_st1 == 0:
        return len_st2
    elif len_st2 == 0:
        return len_st1
    
    if string1[len_st1 -1] == string2[len_st2 -1]:
        c = 0
    else:
        c = 1
        
    return min([levenshtein(string1[0:-1], string2) + 1,
               levenshtein(string1, string2[0:-1]) + 1,
               levenshtein(string1[0:-1], string2[0:-1]) + c ])
               

def main():
    # Check if word parameter was passed
    if len(sys.argv) <= 1:
        print("Please give one word as parameter ex: %s linux" % sys.argv[0])
        sys.exit()
        
    word = sys.argv[1]
    
    # Get google search result
    data = search_word(str(word))
    
    # Iterate over the results and count the word on title
    count = 0
    
    for result in data["items"]:
        # Iterete over the words split by space and check the word
        for i in result["title"].split():
            if levenshtein(word, i) <= 2:
                count +=1
    
    # Show the results and the count
    for result in data["items"]:
        print(result["title"])
    print("\n")
    print("%s - Counter: %s" % (word, count))
    
if __name__ == "__main__":
    main() 
        
