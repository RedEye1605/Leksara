import html
import re

TAG_RE = re.compile(r"<[^>]+>")

def strip_html(text: str) -> str:
    """Hapus tag HTML dan konversi entitas menjadi karakter biasa.

    - Menghapus tag menggunakan regex sederhana.
    - Mengonversi entitas HTML (&nbsp;, &amp;, &quot;, dsb.) menjadi karakter asli.
    - Mengganti NBSP (\u00A0) menjadi spasi biasa agar mudah dinormalisasi.
    """
    if not isinstance(text, str):
        return text
    # Hapus tag
    no_tags = TAG_RE.sub("", text)
    # Unescape entitas HTML
    unescaped = html.unescape(no_tags)
    # Ganti NBSP dengan spasi biasa
    return unescaped.replace("\u00A0", " ")