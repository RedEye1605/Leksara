from typing import Iterable, List, Union, overload
from collections.abc import Mapping
try:  # Opsional: dukungan pandas.Series jika tersedia
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from .functions.normalize_whitespace import normalize_whitespace
from .functions.to_lowercase import to_lowercase
from .functions.strip_html import strip_html
from .functions.normalize_repeated import normalize_repeated
from .functions.remove_punctuation import remove_punctuation
from .functions.remove_digits import remove_digits
from .functions.stopwords import remove_stopwords
from .utils import unicode_normalize_nfkc, strip_control_chars

# Alias tipe keluaran: string, list string, atau pandas.Series (jika tersedia)
if pd is not None:
    SeriesType = pd.Series  # type: ignore[attr-defined]
else:  # Fallback placeholder agar anotasi tidak memaksa impor pandas
    class SeriesType:  # type: ignore
        pass

StrListOrSeries = Union[str, List[str], SeriesType]

# Overloads untuk meningkatkan akurasi tipe di IDE/type checker
@overload
def basic_clean(
    data: str,
    *,
    enable_strip_html: bool = ...,
    remove_punct: bool = ...,
    remove_digits: bool = ...,
    reduce_repeat: bool = ...,
    keep_newline: bool = ...,
    remove_stopwords: bool = ...,
    max_repeat: int = ...,
) -> str: ...

@overload
def basic_clean(
    data: SeriesType,  # type: ignore[valid-type]
    *,
    enable_strip_html: bool = ...,
    remove_punct: bool = ...,
    remove_digits: bool = ...,
    reduce_repeat: bool = ...,
    keep_newline: bool = ...,
    remove_stopwords: bool = ...,
    max_repeat: int = ...,
) -> SeriesType: ...  # type: ignore[valid-type]

@overload
def basic_clean(
    data: Iterable[str],
    *,
    enable_strip_html: bool = ...,
    remove_punct: bool = ...,
    remove_digits: bool = ...,
    reduce_repeat: bool = ...,
    keep_newline: bool = ...,
    remove_stopwords: bool = ...,
    max_repeat: int = ...,
) -> List[str]: ...

def _clean_one(
    text: str,
    *,
    enable_strip_html_opt: bool = True,
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
    if enable_strip_html_opt:
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
    data: Union[str, Iterable[str], SeriesType],  # type: ignore[valid-type]
    *,
    enable_strip_html: bool = True,
    remove_punct: bool = False,
    remove_digits: bool = False,
    reduce_repeat: bool = True,
    keep_newline: bool = False,
    remove_stopwords: bool = False,
    max_repeat: int = 2,
) -> StrListOrSeries:
    """Bersihkan string, iterable string (menghasilkan list), atau pandas.Series.

    Parameter:
    - enable_strip_html: hapus tag HTML dan unescape entitas (default: True)
    - remove_punct: hapus tanda baca (default: False)
    - remove_digits: hapus digit (default: False)
    - reduce_repeat: batasi karakter berulang (default: True)
    - keep_newline: pertahankan newline saat normalisasi spasi (default: False)
    - remove_stopwords: hapus stopword bahasa Indonesia (default: False)
    - max_repeat: batas karakter berulang saat reduce_repeat (default: 2)

    Catatan:
    - Idempoten untuk input yang sudah bersih.
    - Untuk iterable: None dan string kosong akan di-skip; elemen lain di-cast ke str.
        - Untuk Series: index & panjang dipertahankan; NaN dibiarkan apa adanya,
            string berisi hanya whitespace akan dinormalisasi menjadi "" (string kosong).

    Validasi & Error:
    - ValueError jika max_repeat < 1.
    - TypeError jika data bertipe Mapping/dict.

    Contoh:
    >>> basic_clean("<b>Hello&nbsp;World!</b>")
    'hello world!'
    >>> basic_clean(["A", None, "B"])  # iterable -> list
    ['a', 'b']
    """
    # Validasi parameter
    if max_repeat < 1:
        raise ValueError("max_repeat harus >= 1")

    if isinstance(data, str):
        return _clean_one(
            data,
            enable_strip_html_opt=enable_strip_html,
            remove_punct=remove_punct,
            remove_digits_opt=remove_digits,
            reduce_repeat=reduce_repeat,
            keep_newline=keep_newline,
            remove_stopwords_opt=remove_stopwords,
            max_repeat=max_repeat,
        )

    # Dukungan pandas.Series (opsional)
    if pd is not None and isinstance(data, pd.Series):  # type: ignore[attr-defined]
        # Pertahankan index & panjang: jangan dropna, cukup lewati pembersihan untuk NaN/""
        def _series_clean(x):
            if pd.isna(x):  # type: ignore[attr-defined]
                return x
            if isinstance(x, str) and x.strip() == "":
                # Samakan kebijakan dengan iterable: whitespace-only -> ""
                return ""
            return _clean_one(
                str(x),
                enable_strip_html_opt=enable_strip_html,
                remove_punct=remove_punct,
                remove_digits_opt=remove_digits,
                reduce_repeat=reduce_repeat,
                keep_newline=keep_newline,
                remove_stopwords_opt=remove_stopwords,
                max_repeat=max_repeat,
            )
        return data.apply(_series_clean)
    # Iterable lain: lemaskan input - skip None, cast selain None ke str
    # Tolak Mapping/dict agar tidak tanpa sengaja memproses key
    if isinstance(data, Mapping):
        raise TypeError("data tidak boleh berupa Mapping/dict; gunakan list/iterable string atau pandas.Series")
    try:
        items = list(data)  
    except TypeError:
        raise TypeError("data harus berupa string, iterable string, atau pandas.Series")

    out: List[str] = []
    for x in items:
        if x is None:
            continue
        sx = str(x)
        if sx.strip() == "":
            continue
        out.append(
            _clean_one(
                sx,
                enable_strip_html_opt=enable_strip_html,
                remove_punct=remove_punct,
                remove_digits_opt=remove_digits,
                reduce_repeat=reduce_repeat,
                keep_newline=keep_newline,
                remove_stopwords_opt=remove_stopwords,
                max_repeat=max_repeat,
            )
        )
    return out
