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
