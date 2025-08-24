import unittest
from project_name.utils import print_message

class TestUtils(unittest.TestCase):
    def test_print_message(self):
        # This is a simple test for print_message
        with self.assertRaises(Exception):  # Assuming print_message doesn't return anything
            print_message("Test")

if __name__ == '__main__':
    unittest.main()
