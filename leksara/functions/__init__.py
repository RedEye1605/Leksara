"""Granular ops and legacy shims.

Notes:
- Prefer high-level APIs from `leksara.clean`, `leksara.presets`, and `leksara.review_chain`.
- Modules here are single-responsibility building blocks.
- Some files act as shims and are marked deprecated for removal in a future minor release.
"""
from .normalize_whitespace import normalize_whitespace
from .to_lowercase import to_lowercase
from .strip_html import strip_html
from .normalize_repeated import normalize_repeated
from .remove_punctuation import remove_punctuation
from .remove_digits import remove_digits
from .stopwords import remove_stopwords

__all__ = [
	"normalize_whitespace",
	"to_lowercase",
	"strip_html",
	"normalize_repeated",
	"remove_punctuation",
	"remove_digits",
	"remove_stopwords",
]
