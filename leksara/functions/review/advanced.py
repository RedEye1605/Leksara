"""Advanced review mining: rating, elongation, acronym, slang, contraction, normalization."""

import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# buat stemmer sekali saja (hemat waktu)
_factory = StemmerFactory()
_STEMMER = _factory.create_stemmer()

def replace_rating(text):
    pass

def shorten_elongation(text: str, max_repeat: int = 2) -> str:
    """Kurangi pengulangan karakter hingga maksimal `max_repeat` kemunculan.

    Contoh: mantuuulll -> mantul (dengan max_repeat=1 atau 2 sesuai preferensi)
    
    TODO: Implementasi fungsi ini oleh kontributor selanjutnya.
    """
    if max_repeat < 1:
        raise ValueError("max_repeat must be >= 1")

    # Regex: (.)\1{n,} menangkap karakter yang diulang lebih dari n kali
    if max_repeat == 1:
        # Khusus akhir kata: 2+ pengulangan -> 1
        # (.)\1+ artinya ada minimal 1 pengulangan setelah char pertama -> total ≥2
        text = re.sub(r"(.)\1+\b", r"\1", text)

        # Umum (bukan akhir kata): 3+ pengulangan -> 1
        text = re.sub(r"(.)\1{2,}", r"\1", text)
    else:
        # Umum untuk max_repeat >= 2
        pattern = re.compile(r"(.)\1{" + str(max_repeat) + r",}")
        text = pattern.sub(lambda m: m.group(1) * max_repeat, text)

    return text

def replace_acronym(text):
    pass

def remove_acronym(text):
    pass

def normalize_slangs(text):
    pass

def expand_contraction(text):
    pass

def word_normalization(
    text: str,
    *,
    method: str = "stem",
    word_list=None,
    mode: str = "keep",
) -> str:
    """Normalisasi kata dengan stemming/lemmatization.

    Args:
        text: input string
        method: "stem" (default, pakai Sastrawi), "lemma" (future).
        word_list: daftar kata spesial (list[str])
        mode: 
            - "keep": jangan stem kata dalam word_list
            - "only": hanya stem kata dalam word_list
    """
    if not isinstance(text, str):
        return text

    if word_list is None:
        word_list = []

    word_set = {w.lower() for w in word_list}
    words = text.split()
    out = []

    if method == "stem":
        if mode == "keep":
            for w in words:
                out.append(w if w.lower() in word_set else _STEMMER.stem(w))
        elif mode == "only":
            for w in words:
                out.append(_STEMMER.stem(w) if w.lower() in word_set else w)
        else:
            raise ValueError("mode harus 'keep' atau 'only'")
    else:
        # kalau nanti ada lemmatizer lain
        out = words

    return " ".join(out)

