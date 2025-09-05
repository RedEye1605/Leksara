import re
import string

_PUNCT_TABLE = str.maketrans({c: " " for c in string.punctuation})

def remove_punctuation(text: str) -> str:
    """Hapus tanda baca dengan mengubahnya menjadi spasi, lalu menormalkan whitespace."""
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    text = text.translate(_PUNCT_TABLE)
    return re.sub(r"\s+", " ", text).strip()
