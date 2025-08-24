import unittest
from project_name.utils import unicode_normalize_nfkc, strip_control_chars


class TestUtils(unittest.TestCase):
    def test_unicode_normalize_nfkc(self):
        # Fullwidth -> normal (NFKC)
        self.assertEqual(unicode_normalize_nfkc("ＡＢＣ"), "ABC")

    def test_strip_control_chars(self):
        s = "Hello\u200b\ufeff\nWorld"  # pertahankan newline
        out = strip_control_chars(s)
        self.assertEqual(out, "Hello\nWorld")


if __name__ == '__main__':
    unittest.main()
