import re

def normalize_whitespace(text: str, keep_newline: bool = False) -> str:
    """Menormalkan whitespace pada teks.

    - Pangkas spasi di awal/akhir teks
    - Kompres spasi/tab berulang menjadi satu spasi
    - Jika keep_newline=True, pertahankan baris baru sambil menormalkan spasi di sekitarnya
    """
    if not isinstance(text, str):
        return text

    if keep_newline:
        # Ganti rangkaian whitespace (kecuali newline) menjadi satu spasi
        text = re.sub(r"[^\S\n]+", " ", text)
        # Hapus spasi di sekitar newline
        text = re.sub(r"[ \t\r\f\v]*\n[ \t\r\f\v]*", "\n", text)
        # Pangkas keseluruhan
        return text.strip()

    # Default: kompres semua whitespace (termasuk newline) menjadi satu spasi
    return re.sub(r"\s+", " ", text).strip()
