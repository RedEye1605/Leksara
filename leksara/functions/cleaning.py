from __future__ import annotations

from typing import Iterable

import regex as re
try:
    # Alias the emoji library function to avoid shadowing by our own wrapper
    from emoji import replace_emoji as _emoji_replace_emoji  # type: ignore
except Exception:  # pragma: no cover
    # Fallback no-op replacer if emoji is not installed
    def _emoji_replace_emoji(text: str, replace: str = " ") -> str:  # type: ignore[override]
        return text

from .utils.unicode import normalize_text
from .utils.regexes import RE_HTML_TAGS

__all__ = [
    "remove_tags",
    "case_normal",
    "remove_stopwords",
    "remove_whitespace",
    "remove_emoji",
    "replace_emoji",
]


def remove_tags(text: str) -> str:
    return RE_HTML_TAGS.sub(" ", text)


def case_normal(text: str, lower: bool = True) -> str:
    t = normalize_text(text)
    return t.lower() if lower else t


def remove_stopwords(text: str, stopwords: Iterable[str] | None = None) -> str:
    if not stopwords:
        return text
    sw = set(s.strip() for s in stopwords)
    tokens = [tok for tok in re.findall(r"\p{L}+|\d+|\S", text) if tok.lower() not in sw]
    return " ".join(tokens)


def remove_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_emoji(text: str) -> str:
    return _emoji_replace_emoji(text, replace=" ")


def replace_emoji(text: str, replacement: str = "<EMOJI>") -> str:
    return _emoji_replace_emoji(text, replace=replacement)
