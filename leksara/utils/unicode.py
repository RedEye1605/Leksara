from __future__ import annotations

import re
import unicodedata as ud


def normalize_text(text: str, form: str = "NFKC") -> str:
    return ud.normalize(form, text)


def unicode_normalize_nfkc(text: str) -> str:
    """Normalize Unicode ke bentuk NFKC."""
    if not isinstance(text, str):
        return text
    return ud.normalize("NFKC", text)


_CTRL_RE = re.compile(r"[\u0000-\u0009\u000B-\u001F\u007F\u0080-\u009F\u200B\u200C\u200D\u2060\uFEFF]")


def strip_control_chars(text: str) -> str:
    """Hapus karakter kontrol dan zero-width umum (kecuali newline)."""
    if not isinstance(text, str):
        return text
    return _CTRL_RE.sub("", text)
