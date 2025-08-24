import unittest
from project_name.clean import clean_text

class TestClean(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(clean_text("Hello World!"), "hello world!")

if __name__ == '__main__':
    unittest.main()
