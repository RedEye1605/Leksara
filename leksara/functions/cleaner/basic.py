"""Basic cleaning functions: remove_tags, case_normal, remove_stopwords, remove_whitespace, remove_emoji, replace_emoji."""

import html
import re
import os
import string
import emoji
from functools import lru_cache

TAG_RE = re.compile(r"<[^>]+>")

def remove_tags(text: str) -> str:
    """Hapus tag HTML dan konversi entitas menjadi karakter biasa.

    - Menghapus tag menggunakan regex sederhana.
    - Mengonversi entitas HTML (&nbsp;, &amp;, &quot;, dsb.) menjadi karakter asli.
    - Mengganti NBSP (\u00A0) menjadi spasi biasa agar mudah dinormalisasi.
    """
    if not isinstance(text, str):
        return text
    
    no_tags = TAG_RE.sub("", text)
    unescaped = html.unescape(no_tags)
    return unescaped.replace("\u00A0", " ")

def case_normal(text: str) -> str:
    """Ubah teks menjadi huruf kecil menggunakan casefold untuk dukungan Unicode."""
    if not isinstance(text, str):
        return text
    return text.casefold()

def remove_stopwords(text):
    """Hapus stopwords Bahasa Indonesia.

    - Menggabungkan daftar stopwords dari NLTK ("indonesian") dan resource lokal `resources/stopwords/id.txt`.
    - Menghapus baik bentuk singkatan (yang tercantum di file lokal) maupun kata lengkap.
    - Tetap mempertahankan tanda baca dan spasi asli.
    """
    if not isinstance(text, str):
        return text

    stopwords_all = _load_id_stopwords()

    # Tokenisasi non-destruktif: pisahkan kata, spasi, dan tanda baca agar bisa direkonstruksi apa adanya
    tokens = re.findall(r"\w+|[^\w\s]+|\s+", text, flags=re.UNICODE)
    kept = []
    for tok in tokens:
        # Hanya evaluasi kata (\w+). Spasi dan tanda baca dipertahankan.
        if tok.strip() and re.fullmatch(r"\w+", tok, flags=re.UNICODE):
            if tok.casefold() in stopwords_all:
                continue  # drop stopword
        kept.append(tok)

    # Gabungkan kembali tanpa mengubah struktur spasi/tanda baca
    return "".join(kept)

def remove_whitespace(text):
    """Normalisasi whitespace: trim dan kompres spasi berlebih menjadi satu spasi."""
    if not isinstance(text, str):
        return text
    # Ganti semua whitespace (termasuk tab/newline) berturut menjadi satu spasi, lalu trim
    return re.sub(r"\s+", " ", text).strip()

def remove_digits(text: str) -> str:
    """menghapus bilangan pada teks"""
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(r'\d+', '', text)

def remove_punctuation(text: str, exclude: str = None) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    if exclude and not isinstance(exclude, str):
        raise TypeError(f"Parameter 'exclude' harus berupa string, tetapi menerima tipe {type(exclude).__name__}")

    ASCII_PUNCTUATION = string.punctuation
    UNICODE_PUNCTUATION = "“”‘’—…"
    punctuation_to_remove = ASCII_PUNCTUATION + UNICODE_PUNCTUATION

    if exclude:
        punctuation_to_remove = ''.join([p for p in punctuation_to_remove if p not in exclude])

    pattern = f"[{re.escape(punctuation_to_remove)}]"
    return re.sub(pattern, '', text)

def remove_emoji(text: str, emoji: str = None):
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    if emoji == "remove":
        return emoji.replace_emoji(text, replace='')
    elif emoji == "mask":
        return emoji.replace_emoji(text, replace='[EMOJI]')
    else:
        return text
    pass

def replace_emoji(text):
    pass


@lru_cache(maxsize=1)
def _load_id_stopwords():
    """Muat stopwords Bahasa Indonesia dari NLTK dan file lokal.

    Mengembalikan set berisi seluruh stopword dalam bentuk casefolded.
    Jika resource NLTK belum terunduh, akan diunduh otomatis (sekali saja).
    """
    stopwords_local = set()

    # Path file lokal: leksara/resources/stopwords/id.txt
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    resource_path = os.path.join(base_dir, "resources", "stopwords", "id.txt")
    if os.path.exists(resource_path):
        with open(resource_path, encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if w and not w.startswith("#"):
                    stopwords_local.add(w.casefold())

    # NLTK Indonesian stopwords
    stopwords_nltk = set()
    try:
        from nltk.corpus import stopwords as nltk_stopwords  # type: ignore
        try:
            stopwords_nltk = set(w.casefold() for w in nltk_stopwords.words("indonesian"))
        except LookupError:
            import nltk  # type: ignore
            nltk.download("stopwords", quiet=True)
            stopwords_nltk = set(w.casefold() for w in nltk_stopwords.words("indonesian"))
    except Exception:
        # Jika NLTK tidak terpasang/tersedia, tetap lanjut dengan daftar lokal saja
        stopwords_nltk = set()

    # Gabungkan, pastikan bentuk casefolded untuk robust Unicode
    return stopwords_nltk | stopwords_local
