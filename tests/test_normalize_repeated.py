import unittest
from project_name.functions.normalize_repeated import normalize_repeated

class TestNormalizeRepeated(unittest.TestCase):
    def test_max_repeat_validation(self):
        with self.assertRaises(ValueError):
            normalize_repeated("aaaa", max_repeat=0)

    def test_end_word_double_char_removed(self):
        # "pekerjaann" -> "pekerjaan"
        self.assertEqual(normalize_repeated("pekerjaann", max_repeat=1), "pekerjaan")

    def test_end_word_many_char_removed(self):
        # "sekaliiii" -> "sekali"
        self.assertEqual(normalize_repeated("sekaliiii", max_repeat=1), "sekali")

    def test_middle_word_repeated(self):
        # "jeeelek" -> "jelek"
        self.assertEqual(normalize_repeated("jeeelek", max_repeat=1), "jelek")

    def test_middle_word_repeated_2(self):
        # "baguuuuus" -> "bagus"
        self.assertEqual(normalize_repeated("baguuuuus", max_repeat=1), "bagus")

    def test_combo_word(self):
        # "mantaaappp" -> "mantap"
        self.assertEqual(normalize_repeated("mantaaappp", max_repeat=1), "mantap")

    def test_max_repeat_2_behavior(self):
        # "mantaaapppp" -> "mantaapp"
        self.assertEqual(normalize_repeated("mantaaapppp", max_repeat=2), "mantaapp")

    def test_max_repeat_2_huruf(self):
        # "hiiiii" -> "hii"
        self.assertEqual(normalize_repeated("hiiiii", max_repeat=2), "hii")

    def test_sentence_case(self):
        txt = "peeeekerjaann mereka itu jeeelllleeeeekkk sekaliiiiiiiiii"
        out = normalize_repeated(txt, max_repeat=1)
        # Pastikan kata "peeeekerjaann" jadi "pekerjaan"
        self.assertIn("pekerjaan", out)
        # Pastikan kata akhir "sekaliiiiiiiiii" jadi "sekali"
        self.assertIn("sekali", out)
        # Tidak boleh ada sisa "iiii"
        self.assertNotIn("iiii", out)

if __name__ == '__main__':
    unittest.main()
