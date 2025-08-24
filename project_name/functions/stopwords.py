import re
from typing import Iterable, Optional, FrozenSet

DEFAULT_ID_STOPWORDS: FrozenSet[str] = frozenset({
    # Kumpulan minimal; dapat diperluas sesuai kebutuhan
    "yang", "dan", "di", "ke", "dari", "untuk", "pada", "dengan", "ini", "itu",
    "atau", "juga", "karena", "agar", "sehingga", "adalah", "bukan", "tidak",
})

# Precompile pola tokenisasi agar tidak dibuat berulang kali
TOKEN_RE = re.compile(r"\w+|[^\w\s]", flags=re.UNICODE)

def _normalize_token(token: str) -> str:
    return token.casefold()

def remove_stopwords(text: str, words: Optional[Iterable[str]] = None, whitelist: Optional[Iterable[str]] = None) -> str:
    """Hapus stopword dari string.

    - Gunakan daftar Indonesia bawaan jika `words` tidak diberikan.
    - Usahakan mempertahankan spasi asli saat menghapus token.
    - Pencocokan tidak peka huruf besar/kecil.
    """
    if not isinstance(text, str):
        return text

    stop_set = set(_normalize_token(w) for w in (words or DEFAULT_ID_STOPWORDS))
    white_set = set(_normalize_token(w) for w in (whitelist or []))
    tokens = TOKEN_RE.findall(text)

    kept = []
    for tok in tokens:
        # Only filter word tokens
        if re.match(r"\w+", tok, flags=re.UNICODE):
            norm = _normalize_token(tok)
            if norm in white_set:
                kept.append(tok)
                continue
            if norm in stop_set:
                continue
        kept.append(tok)

    # Gabungkan kembali dengan satu spasi antar token kata
    result = re.sub(r"\s+", " ", "".join(kept)).strip()
    return result
