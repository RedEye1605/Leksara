import re
from typing import Iterable, Optional, Set

DEFAULT_ID_STOPWORDS: Set[str] = set()

def _normalize_token(token: str) -> str:
    """Normalisasi token (mis. ke huruf kecil) sebelum pembandingan.

    TODO: Implementasi fungsi ini oleh kontributor selanjutnya.
    """
    raise NotImplementedError("_normalize_token belum diimplementasikan.")

def remove_stopwords(text: str, words: Optional[Iterable[str]] = None) -> str:
    """Hapus stopword dari string (opsional).

    TODO: Implementasi fungsi ini oleh kontributor selanjutnya.
    """
    raise NotImplementedError("remove_stopwords belum diimplementasikan.")
