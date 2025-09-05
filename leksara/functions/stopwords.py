import re
from typing import Iterable, Optional, FrozenSet, Iterable as _Iterable
from importlib.resources import files

DEFAULT_ID_STOPWORDS: FrozenSet[str] = frozenset({
    # Kumpulan minimal; dapat diperluas sesuai kebutuhan
    "yang", "dan", "di", "ke", "dari", "untuk", "pada", "dengan", "ini", "itu",
    "atau", "juga", "karena", "agar", "sehingga", "adalah", "bukan", "tidak",
})

# Precompile pola tokenisasi agar tidak dibuat berulang kali
TOKEN_RE = re.compile(r"\w+|[^\w\s]", flags=re.UNICODE)

def _normalize_token(token: str) -> str:
    return token.casefold()


def load_id_stopwords(extra: Optional[_Iterable[str]] = None) -> FrozenSet[str]:
    """Load a richer Indonesian stopwords set from packaged data and merge with defaults.

    - Returns a frozenset of lowercased tokens.
    - `extra` can be provided to extend the list at runtime.
    """
    try:
        txt = files('leksara.functions.data').joinpath('stopwords_id.txt').read_text(encoding='utf-8')
        file_words = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.lstrip().startswith('#')]
    except Exception:
        file_words = []
    base = set(DEFAULT_ID_STOPWORDS)
    base.update(w.casefold() for w in file_words)
    if extra:
        base.update(w.casefold() for w in extra)
    return frozenset(base)


def remove_stopwords_id(text: str, whitelist: Optional[_Iterable[str]] = None, extra: Optional[_Iterable[str]] = None) -> str:
    """Remove Indonesian stopwords using built-in list + optional extra words.

    This is a thin convenience wrapper around `remove_stopwords` with `words=load_id_stopwords(...)`.
    """
    words = load_id_stopwords(extra=extra)
    return remove_stopwords(text, words=words, whitelist=whitelist)

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
