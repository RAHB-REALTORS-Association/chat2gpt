import unittest
from main import num_tokens_from_string

class TestNumTokensFromString(unittest.TestCase):

    def test_short_string(self):
        self.assertEqual(num_tokens_from_string("Hello world"), 3)


    def test_long_string(self):
        long_string = " ".join(["word" for _ in range(1000)])
        self.assertEqual(num_tokens_from_string(long_string), 1000)


    def test_empty_string(self):
        self.assertEqual(num_tokens_from_string(""), 0)


    def test_special_characters(self):
        self.assertEqual(num_tokens_from_string("Hello, world!"), 4)


if __name__ == '__main__':
    unittest.main()