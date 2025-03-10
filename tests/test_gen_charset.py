import unittest
from src import gen_charset


class TestGenCharset(unittest.TestCase):
    def test_number_match(self):
        self.assertEqual(gen_charset("\d"), "0123456789")

    def test_letter_match(self):
        self.assertEqual(gen_charset("[a-z]"), "abcdefghijklmnopqrstuvwxyz")

    def test_frequency_sorted(self):
        self.assertEqual(gen_charset(
            "[a-z]", frequency_sorted=True), "etaoinshrdlcumwfgypbvkjxqz")

    def test_no_match(self):
        with self.assertRaises(ValueError):
            gen_charset("")


if __name__ == "__main__":
    unittest.main()
