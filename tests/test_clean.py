import unittest
from project_name.clean import basic_clean

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None  # type: ignore


class TestClean(unittest.TestCase):
    def test_basic_clean_lowercase(self):
        # Seharusnya mengubah huruf menjadi kecil (jika sudah diimplementasikan)
        try:
            self.assertEqual(basic_clean("Hello World!"), "hello world!")
        except NotImplementedError:
            self.skipTest("basic_clean masih template (NotImplemented)")

    def test_basic_clean_idempotent_str(self):
        # Idempoten: membersihkan dua kali hasilnya sama
        txt = "Hello World!"
        try:
            once = basic_clean(txt)
            twice = basic_clean(once)
            self.assertEqual(once, twice)
        except NotImplementedError:
            self.skipTest("basic_clean masih template (NotImplemented)")

    def test_basic_clean_list_skip_none_and_cast(self):
        data = ["Hello", None, 123, "  "]
        try:
            out = basic_clean(data)
            self.assertIsInstance(out, list)
            # None di-skip, 123 di-cast
            self.assertGreaterEqual(len(out), 2)
        except NotImplementedError:
            self.skipTest("basic_clean masih template (NotImplemented)")

    def test_basic_clean_series_support(self):
        if pd is None:
            self.skipTest("pandas tidak tersedia")
        s = pd.Series(["Hello", None, "World"])  # type: ignore
        try:
            out = basic_clean(s)
            # Keluaran Series
            self.assertTrue(hasattr(out, "iloc"))
            self.assertEqual(len(out), 3)  # panjang & index dipertahankan
            self.assertTrue(pd.isna(out.iloc[1]))
        except NotImplementedError:
            self.skipTest("basic_clean masih template (NotImplemented)")

    def test_html_and_entities(self):
        try:
            self.assertEqual(basic_clean("<p>Hello&nbsp;&amp;\nWorld</p>", keep_newline=False), "hello & world")
        except NotImplementedError:
            self.skipTest("fungsi masih template (NotImplemented)")

    def test_control_and_zero_width(self):
        try:
            txt = "Hello\u200b\ufeff World"
            self.assertEqual(basic_clean(txt), "hello world")
        except NotImplementedError:
            self.skipTest("fungsi masih template (NotImplemented)")

    def test_repeated_and_options(self):
        try:
            txt = "Siaaappp!!! 2025"
            out = basic_clean(txt, reduce_repeat=True, max_repeat=2, remove_digits=True, remove_punct=True)
            # "Siaaappp!!!" -> "si aapp" -> normalisasi spasi
            self.assertIn("si", out)
            self.assertNotRegex(out, r"\d")
            self.assertNotRegex(out, r"[!?.]")
        except NotImplementedError:
            self.skipTest("fungsi masih template (NotImplemented)")

    def test_mapping_guard(self):
        # Memastikan dict/Mapping ditolak
        with self.assertRaises(TypeError):
            basic_clean({"a": 1})  # type: ignore[arg-type]

    def test_max_repeat_validation(self):
        # max_repeat harus >= 1
        with self.assertRaises(ValueError):
            basic_clean("aaaaa", max_repeat=0)

    def test_series_whitespace_only_normalized(self):
        if pd is None:
            self.skipTest("pandas tidak tersedia")
        s = pd.Series([" ", "\t\t", None])  # type: ignore
        try:
            out = basic_clean(s)
            self.assertEqual(out.iloc[0], "")
            self.assertEqual(out.iloc[1], "")
            self.assertTrue(pd.isna(out.iloc[2]))
            self.assertEqual(list(out.index), list(s.index))  # index sama
        except NotImplementedError:
            self.skipTest("fungsi masih template (NotImplemented)")

    def test_keep_newline_true(self):
        # Saat keep_newline=True, newline dipertahankan tapi spasi dinormalisasi
        txt = "Hello\nWorld"
        try:
            out = basic_clean(txt, keep_newline=True)
            self.assertIn("\n", out)
        except NotImplementedError:
            self.skipTest("fungsi masih template (NotImplemented)")


if __name__ == '__main__':
    unittest.main()
