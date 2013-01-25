import unittest
from solution import levenshtein, count_word, count_word_with_distance, titles


class TestSolution(unittest.TestCase):

    def test_levenshtein(self):
        self.assertEquals(levenshtein('', ''), 0)
        self.assertEquals(levenshtein('a', ''), 1)
        self.assertEquals(levenshtein('', 'a'), 1)
        self.assertEquals(levenshtein('ab', 'b'), 1)
        self.assertEquals(levenshtein('ab', 'bb'), 1)
        self.assertEquals(levenshtein('ab', 'ba'), 2)
        self.assertEquals(levenshtein('word', 'word'), 0)
        self.assertEquals(levenshtein('wibble', 'wobble'), 1)
        self.assertEquals(levenshtein('test', 'toast'), 2)
        self.assertEquals(levenshtein('foo', 'four'), 2)
        self.assertEquals(levenshtein('stone', 'magnet'), 4)
        self.assertEquals(levenshtein('window', 'windmill'), 4)

    def test_count_word(self):
        self.assertEquals(count_word('ab', ['ba']), 0)
        self.assertEquals(count_word('ab', ['ba', 'bc']), 0)
        self.assertEquals(count_word('ab', ['ab', 'ba', 'bc']), 1)
        self.assertEquals(count_word('ab', ['ab', 'ba', 'ab', 'bc']), 2)

    def test_count_word_with_distance(self):
        self.assertEquals(count_word_with_distance('abc', ['xyz', '123']), 0)
        self.assertEquals(count_word_with_distance('abc', ['xyz', 'bbb']), 1)
        self.assertEquals(count_word_with_distance('abc', ['xyz', 'abc', 'abcd', 'bbb', 'bbbb']), 2)

    def test_titles(self):
        len_titles = len([t for t in titles('test', 10)])
        self.assertEquals(len_titles, 10)

if __name__ == '__main__':
    unittest.main()
