from __future__ import annotations

from typing import Mapping, Iterable

import regex as re
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # type: ignore
except Exception:  # pragma: no cover
    class _DummyStemmer:
        def stem(self, t: str) -> str:
            return t

    class StemmerFactory:  # type: ignore
        def create_stemmer(self):
            return _DummyStemmer()

from .utils.regexes import RE_ELONGATION

_factory = StemmerFactory()
_STEMMER = _factory.create_stemmer()

__all__ = [
    "replace_rating",
    "shorten_elongation",
    "replace_acronym",
    "remove_acronym",
    "normalize_slangs",
    "expand_contraction",
    "normalize_word",
]


def replace_rating(text: str, mapping: Mapping[str, str] | None = None) -> str:
    mapping = mapping or {
        "bintang 5": "rating_5",
        "bintang 4": "rating_4",
        "bintang 3": "rating_3",
        "bintang 2": "rating_2",
        "bintang 1": "rating_1",
    }
    for k, v in mapping.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text, flags=re.IGNORECASE)
    return text


def shorten_elongation(text: str) -> str:
    # Kurangi run huruf berulang menjadi satu huruf (contoh: baaaagus -> bagus)
    return RE_ELONGATION.sub(lambda m: m.group(1), text)


def replace_acronym(text: str, acronyms: Mapping[str, str]) -> str:
    for k, v in acronyms.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text, flags=re.IGNORECASE)
    return text


def remove_acronym(text: str, acronyms: Iterable[str]) -> str:
    for k in acronyms:
        text = re.sub(rf"\b{re.escape(k)}\b", " ", text, flags=re.IGNORECASE)
    return text


def normalize_slangs(text: str, slang_map: Mapping[str, str]) -> str:
    for k, v in slang_map.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text, flags=re.IGNORECASE)
    return text


def expand_contraction(text: str, contractions: Mapping[str, str]) -> str:
    for k, v in contractions.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text, flags=re.IGNORECASE)
    return text


def normalize_word(text: str, whitelist: set[str] | None = None) -> str:
    tokens = re.findall(r"\p{L}+|\d+|\S", text)
    wl = whitelist or set()
    norm = [t if t in wl else _STEMMER.stem(t) for t in tokens]
    return " ".join(norm)
