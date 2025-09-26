"""CartBoard: capture raw reviews and generate initial metadata flags.

Fitur
- Membersihkan teks (hapus email, URL, tanda baca, stopwords) menggunakan utilitas internal Leksara.
- Menghasilkan metadata flags:
    - pii_flag: ada PII (email/telepon/NIK/alamat)
    - non_alphabetical_flag: ada karakter non-alfabet (angka/simbol)
    - lang_mix_flag: heuristik campur bahasa sederhana (tanpa deteksi Bahasa Inggris eksplisit)

Example
-------
>>> from leksara.frames.cartboard import CartBoard
>>> text = "Barangnya mantulll! Email saya: user@example.com. Visit https://shop.id"
>>> board = CartBoard(text, rating=5)
>>> result = board.to_dict()
>>> sorted(result.keys())
['lang_mix_flag', 'non_alphabetical_flag', 'original_text', 'pii_flag', 'rating', 'refined_text']
>>> result['pii_flag']  # email detected
True
>>> result['refined_text']  # cleaned text
'barangnya mantulll  visit'
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import re

# Cleaning utilities from project
from ..functions.cleaner.basic import (
    remove_punctuation,
    remove_stopwords,
    remove_whitespace,
    replace_url,
    case_normal,
    _load_id_stopwords,
)
from ..functions.patterns.pii import (
    replace_email,
    email_config,
    phone_config,
    NIK_config,
    address_config,
)


def _get_id_stopwords_full() -> set:
    """Load full Indonesian stopwords from resources using existing loader."""
    try:
        return _load_id_stopwords() or set()
    except Exception:
        return set()


@dataclass
class CartBoard:
    original_text: str
    rating: Optional[float] = None

    def __init__(self, raw_text: str, rating: Optional[float] = None):
        if not isinstance(raw_text, str):
            raise TypeError(f"raw_text must be str, got {type(raw_text).__name__}")
        self.original_text = raw_text
        self.rating = rating
        self._refined_text = self._clean_text(raw_text)
        self._flags = self._generate_flags(raw_text)

    # --------------- public API ---------------
    @property
    def refined_text(self) -> str:
        return self._refined_text

    @property
    def pii_flag(self) -> bool:
        return self._flags["pii_flag"]

    @property
    def non_alphabetical_flag(self) -> bool:
        return self._flags["non_alphabetical_flag"]

    @property
    def lang_mix_flag(self) -> bool:
        return self._flags["lang_mix_flag"]

    def to_dict(self) -> Dict[str, Optional[object]]:
        return {
            "original_text": self.original_text,
            "refined_text": self.refined_text,
            "rating": self.rating,
            "pii_flag": self.pii_flag,
            "non_alphabetical_flag": self.non_alphabetical_flag,
            "lang_mix_flag": self.lang_mix_flag,
        }

    # --------------- internals ---------------
    def _clean_text(self, text: str) -> str:
        """Pipeline: lower → remove email → remove url → remove punct → stopwords → whitespace.

        Note: We remove PII here because we only need a cleaned preview for triage;
        downstream masking/cleaning still happens in the main pipeline.
        """
        t = text
        t = case_normal(t)
        # Remove emails and URLs
        t = replace_email(t, mode="remove")
        t = replace_url(t, mode="remove")
        # Remove punctuation and stopwords
        t = remove_punctuation(t)
        t = remove_stopwords(t)
        t = remove_whitespace(t)
        return t

    def _generate_flags(self, text: str) -> Dict[str, bool]:
        # PII flag using regex patterns from config (email, phone, NIK, address)
        pii = False
        for cfg in (email_config, phone_config, NIK_config, address_config):
            patt = (cfg or {}).get("pattern") or (cfg.get("trigger_pattern", {}).get("pattern") if cfg else None)
            if patt and re.search(patt, text, flags=re.IGNORECASE):
                pii = True
                break

        # Non-alphabetical flag: contains anything other than letters/space
        non_alpha = bool(re.search(r"[^a-zA-Z\s]", text))

        # Heuristik campur bahasa sederhana berfokus Indonesia:
        # Jika teks mengandung sangat sedikit kata umum Indonesia dibanding total token,
        # kita tandai sebagai campur (indikasi dominasi non-Indonesia). Tidak ada kamus Inggris eksplisit.
        tokens = re.findall(r"[a-zA-Z]+", text.lower())
        if not tokens:
            lang_mix = False
        else:
            id_stop = _get_id_stopwords_full()
            id_hits = sum(1 for tok in tokens if tok in id_stop)
            # Jika proporsi kata umum Indonesia sangat rendah, anggap campur bahasa
            lang_mix = (id_hits / max(1, len(tokens))) < 0.05

        return {
            "pii_flag": pii,
            "non_alphabetical_flag": non_alpha,
            "lang_mix_flag": lang_mix,
        }
