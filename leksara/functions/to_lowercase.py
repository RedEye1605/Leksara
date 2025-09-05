def to_lowercase(text: str) -> str:
    """Ubah teks menjadi huruf kecil menggunakan casefold untuk dukungan Unicode."""
    if not isinstance(text, str):
        return text
    return text.casefold()