from .version import __version__
from .core.chain import leksara, ReviewChain, run_pipeline
from .frames.cartboard import CartBoard
from .functions.cleaner.basic import (
    remove_tags, case_normal, remove_stopwords, remove_whitespace,
    remove_punctuation, remove_digits, remove_emoji, replace_emoji
)
from .functions.patterns.pii import (
    remove_phone, replace_phone, remove_address, replace_address,
    remove_email, replace_email, remove_id, replace_id
)
from .functions.review.advanced import (
    replace_rating, shorten_elongation, replace_acronym, remove_acronym,
    normalize_slangs, expand_contraction, word_normalization
)

__all__ = [
    "leksara","ReviewChain", "run_pipeline", "CartBoard",
    "remove_tags", "case_normal", "remove_stopwords", "remove_whitespace",
    "remove_punctuation", "remove_digits", "remove_emoji", "replace_emoji",
    "remove_phone", "replace_phone", "remove_address", "replace_address",
    "remove_email", "replace_email", "remove_id", "replace_id",
    "replace_rating", "shorten_elongation", "replace_acronym", "remove_acronym",
    "normalize_slangs", "expand_contraction", "word_normalization",
]
