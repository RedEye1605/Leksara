from __future__ import annotations

from .unicode import unicode_normalize_nfkc
from ..functions.normalize_whitespace import normalize_whitespace
from ..functions.to_lowercase import to_lowercase


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input harus berupa string.")
    # NFKC + lowercase + whitespace normalize
    t = unicode_normalize_nfkc(text)
    return normalize_whitespace(to_lowercase(t))


def is_empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        if value.strip() == "":
            return True
        v = value.strip().casefold()
        return v in {"n/a", "na", "null", "none"}
    return False
