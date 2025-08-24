import unittest
from project_name.clean import basic_clean


class TestClean(unittest.TestCase):
    def test_basic_clean_lowercase(self):
        # Seharusnya mengubah huruf menjadi kecil
        self.assertEqual(basic_clean("Hello World!"), "hello world!")


if __name__ == '__main__':
    unittest.main()
