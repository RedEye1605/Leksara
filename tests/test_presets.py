import unittest
from project_name.presets import get_ecommerce_preset

class TestPresets(unittest.TestCase):
    def test_get_ecommerce_preset(self):
        preset = get_ecommerce_preset()
        self.assertTrue(preset["remove_stopwords"])
        self.assertTrue(preset["remove_punctuation"])
        self.assertTrue(preset["normalize_case"])

if __name__ == '__main__':
    unittest.main()
