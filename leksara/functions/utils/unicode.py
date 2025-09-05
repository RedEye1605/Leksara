from __future__ import annotations

import unicodedata as ud


def normalize_text(text: str, form: str = "NFKC") -> str:
    return ud.normalize(form, text)
