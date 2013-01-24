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


class TestTitlesExtractionMethod(unittest.TestCase):

    @patch('requests.get', Mock(return_value=MockedResponse(content=GOOGLE_RESPONSE, status_code=200)))
    def test_returns_correct_and_clean_titles(self):
        expected_titles = [
            u"Bernardo Vieira de Souza – Wikipédia, a enciclopédia livre",
            u"Bernardo Shoes and Sandals - Women&#39;s Leather",
            u"Bernardo Winery | Founded 1889. The oldest continuously operating ...",
            u"BERNARDO FASHIONS",
        ]
        json_dict = make_google_api_request('bernardo')
        titles = get_titles(json_dict)
        self.assertEqual(titles, expected_titles)


class TestLevenstheinDistanceCalc(unittest.TestCase):

    def test_should_return_word_1_len_if_not_word_2(self):
        cost = levenhtein_distance_calc('hey', '')
        self.assertEqual(3, cost)

    def test_should_return_word_2_len_if_not_word_1(self):
        cost = levenhtein_distance_calc('', 'hey')
        self.assertEqual(3, cost)

    def test_calc_cost_correctly(self):
        cost = levenhtein_distance_calc('kitten', 'sitting')
        self.assertEqual(3, cost)
        cost = levenhtein_distance_calc('kitten', 'sittin')
        self.assertEqual(2, cost)


class TestCountWordsOccurrences(unittest.TestCase):

    def test_exactly_word_is_matched_one_time_returns_1(self):
        word = u'bernardo'
        title = u'Python script by bernardo'
        self.assertEqual(1, count_word_occurrences(title, word))

    def test_word_counting_is_not_case_sensitive(self):
        word = u'bernardo'
        title = u'Python script by BERNARDO'
        self.assertEqual(1, count_word_occurrences(title, word))

    def test_should_accept_levenhtein_distances_bellow_2(self):
        word = u'bernardo'
        title = u'Python script by BERNARD or bernar but not berna'
        self.assertEqual(2, count_word_occurrences(title, word))

if __name__ == '__main__':
    unittest.main()
