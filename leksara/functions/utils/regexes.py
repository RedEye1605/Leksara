from __future__ import annotations

import regex as re

# Common patterns
RE_HTML_TAGS = re.compile(r"<[^>]+>")
RE_PHONE = re.compile(r"\b(?:\+?62|0)(?:\d[ -]?){8,13}\b")
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Very rough address patterns for Indonesian contexts (street, RT/RW, etc.)
# Address: match from Jalan markers up to optional No.<num>, and stop before NIK/ID or punctuation/end
RE_ADDRESS = re.compile(
	r"\b(?:Jl\.?|Jalan|Gg\.?|Gang|RT\s?\d{1,2}/RW\s?\d{1,2}|No\.?\s?\d+)\b.*?(?:\bNo\.?\s?\d+\b)?(?=\s+\bNIK\b|$|[,;\n])",
	re.IGNORECASE,
)
# NIK/KTP: 16 digits, sometimes spaced
RE_KTP = re.compile(r"\b(?:\d[ -]?){16}\b")
# Elongation like cooool -> cool (collapse to single letter)
RE_ELONGATION = re.compile(r"(\p{L})\1+")
