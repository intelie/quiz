#coding:utf-8
import unittest
from mock import patch, Mock
from urllib import urlencode

from google_title_hit_counter import *
from test_data import GOOGLE_RESPONSE


class MockedResponse():
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

class TestGoogleRequest(unittest.TestCase):

    @patch('requests.get', Mock(return_value=MockedResponse(content=GOOGLE_RESPONSE, status_code=200)))
    def test_request_return_json_dict_correctly(self):
        json_dict = make_google_api_request('search term')

        expected_json_dict = json.loads(GOOGLE_RESPONSE)
        self.assertEqual(expected_json_dict, json_dict)

    @patch('requests.get', Mock(return_value=MockedResponse(content=GOOGLE_RESPONSE, status_code=200)))
    def test_requests_get_method_is_called_correctly(self):
        querystring = urlencode({'v': '1.0', 'q': 'search term'})
        request_url = GOOGLE_SEARCH_API_URL + '?' + querystring

        import requests
        json_dict = make_google_api_request('search term')
        requests.get.assert_called_with(request_url)


if __name__ == '__main__':
    unittest.main()
