# -*- coding: utf-8 -*-

import unittest
import json
from intelie import *


class IntelieTestCase(unittest.TestCase):
    def test_validate_should_thrown_an_exception_if_no_result(self):
        json_result = '{"Fake": "Value", "Place": "Holder"}'
        google_result = json.loads(json_result)
        self.assertRaises(RuntimeError, validate, google_result)

        json_result = '{"error": {"message": "Random message!"}}'
        google_result = json.loads(json_result)
        self.assertRaises(RuntimeError, validate, google_result)

    def test_strip_accents(self):
        string = 'Téstê pàrá rêmõvèr âcêntós'
        expected = 'Teste para remover acentos'

        self.assertEquals(strip_accents(string), expected)

    def test_normalize_should_return_a_lowercased_accents_striped_string(self):
        string = 'TéStÊ, PàRá<> !rÊmõVèR. ,âCêNtÓs!'
        expected = 'teste para remover acentos'

        self.assertEquals(normalize_string(string), expected)


if __name__ == "__main__":
    unittest.main()
