from typing import Iterable, List, Union

from .functions.normalize_whitespace import normalize_whitespace
from .functions.to_lowercase import to_lowercase
from .functions.strip_html import strip_html
from .functions.normalize_repeated import normalize_repeated
from .functions.remove_punctuation import remove_punctuation
from .functions.remove_digits import remove_digits
from .functions.stopwords import remove_stopwords
from .utils import unicode_normalize_nfkc, strip_control_chars

StrOrList = Union[str, List[str]]

def _clean_one(
    text: str,
    *,
    strip_html_opt: bool = True,
    remove_punct: bool = True,
    remove_digits_opt: bool = False,
    reduce_repeat: bool = True,
    keep_newline: bool = False,
    remove_stopwords_opt: bool = False,
    max_repeat: int = 2,
) -> str:
    t = text
    # Unicode normalize + strip control
    t = unicode_normalize_nfkc(t)
    t = strip_control_chars(t)
    # Optional: strip HTML
    if strip_html_opt:
        t = strip_html(t)
    # Lowercase
    t = to_lowercase(t)
    # Optional: remove punctuation/digits
    if remove_punct:
        t = remove_punctuation(t)
    if remove_digits_opt:
        t = remove_digits(t)
    # Normalize repeated chars
    if reduce_repeat:
        t = normalize_repeated(t, max_repeat=max_repeat)
    # Whitespace normalization
    t = normalize_whitespace(t, keep_newline=keep_newline)
    # Optional: stopwords
    if remove_stopwords_opt:
        t = remove_stopwords(t)
    return t

def basic_clean(
    data: Union[str, Iterable[str]],
    *,
    strip_html: bool = True,
    remove_punct: bool = True,
    remove_digits: bool = False,
    reduce_repeat: bool = True,
    keep_newline: bool = False,
    remove_stopwords: bool = False,
    max_repeat: int = 2,
) -> StrOrList:
    """Bersihkan string atau iterable string dengan nilai default yang aman.

    Idempoten untuk input yang sudah bersih.
    """
    if isinstance(data, str):
        return _clean_one(
            data,
            strip_html_opt=strip_html,
            remove_punct=remove_punct,
            remove_digits_opt=remove_digits,
            reduce_repeat=reduce_repeat,
            keep_newline=keep_newline,
            remove_stopwords_opt=remove_stopwords,
            max_repeat=max_repeat,
        )
    # Validate iterable of strings
    try:
        items = list(data)  
    except TypeError:
        raise TypeError("data harus berupa string atau iterable berisi string")

    non_str_indices = [i for i, x in enumerate(items) if not isinstance(x, str)]
    if non_str_indices:
        raise TypeError(f"Semua elemen harus string. Indeks non-string: {non_str_indices}")

    return [
        _clean_one(
            x,
            strip_html_opt=strip_html,
            remove_punct=remove_punct,
            remove_digits_opt=remove_digits,
            reduce_repeat=reduce_repeat,
            keep_newline=keep_newline,
            remove_stopwords_opt=remove_stopwords,
            max_repeat=max_repeat,
        )
        for x in items
    ]
