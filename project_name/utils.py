import re
import unicodedata

def unicode_normalize_nfkc(text: str) -> str:
    """Normalkan teks ke bentuk Unicode NFKC."""
    if not isinstance(text, str):
        return text
    return unicodedata.normalize("NFKC", text)

_CTRL_RE = re.compile(r"[\u0000-\u001F\u007F\u200B\uFEFF]")

def strip_control_chars(text: str) -> str:
    """Hapus karakter kontrol dan zero-width seperti \u200b, \ufeff, serta kode kontrol ASCII."""
    if not isinstance(text, str):
        return text
    return _CTRL_RE.sub("", text)

def print_message(message):
    """Fungsi utilitas untuk mencetak pesan."""
    print(message)
    
def clean_text(text):
    """Bersihkan teks dengan mengubah ke huruf kecil dan menghapus spasi di awal/akhir."""
    if not isinstance(text, str):
        raise ValueError("Input harus berupa string.")
    return text.strip().lower()

def is_empty(value):
    """Cek apakah nilai kosong (None, string kosong, atau 'N/A')."""
    return value in (None, '', 'N/A')
