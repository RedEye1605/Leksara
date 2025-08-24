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
        t = normalize_repeated(t, max_repeat=2)
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
        )
    # Assume iterable of strings
    return [
        _clean_one(
            x,
            strip_html_opt=strip_html,
            remove_punct=remove_punct,
            remove_digits_opt=remove_digits,
            reduce_repeat=reduce_repeat,
            keep_newline=keep_newline,
            remove_stopwords_opt=remove_stopwords,
        )
        for x in data
    ]

def clean_data(text):
    """Legacy: hapus None/kosong dari list. Dipertahankan untuk kompatibilitas ke belakang."""
    print("Starting data cleaning process...")
    if not isinstance(text, list):
        raise ValueError("Input harus berupa list.")
    cleaned_data = [x for x in text if x not in (None, '', 'N/A')]
    print(f"Cleaned data: {cleaned_data}")
    return cleaned_data

if __name__ == "__main__":
    # Quick smoke test
    sample = [
        "<p>Halo&nbsp;dunia!</p>",
        "Mantuuulll \u200b Sekali!!! 123",
    ]
    print(basic_clean(sample))
def clean_text(text):
    """ Fungsi pembersihan teks dasar. """
    return text.lower()
