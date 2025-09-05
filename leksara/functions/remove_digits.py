import re

_DIGIT_RE = re.compile(r"\d", flags=re.UNICODE)

def remove_digits(text: str) -> str:
    """Hapus semua digit (Unicode) dari teks.

    - Menghapus angka 0-9 dan digit Unicode lain (kategori Nd) menggunakan kelas digit regex.
    - Tidak menyentuh tanda baca atau huruf.
    """
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    return _DIGIT_RE.sub("", text)
