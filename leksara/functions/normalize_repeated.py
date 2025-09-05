import re

def normalize_repeated(text: str, max_repeat: int = 2) -> str:
    """Kurangi pengulangan karakter berurutan hingga maksimal `max_repeat`.

    Contoh:
    - "mantuuulll" -> "mantuull" (max_repeat=2)
    - "mantuuulll" -> "mantul" (max_repeat=1)

    Catatan:
    - Berlaku untuk semua karakter (huruf, angka, tanda baca) berbasis Unicode.
    - Lemah terhadap gabungan karakter kompleks (grapheme cluster) tapi cukup untuk kasus umum.
    """
    if not isinstance(text, str):
        return text
    if max_repeat < 1:
        raise ValueError("max_repeat harus >= 1")

    # Gantikan run berulang (>= max_repeat+1) menjadi tepat max_repeat
    pattern = re.compile(r"(.)\1{" + str(max_repeat) + r",}")
    return pattern.sub(lambda m: m.group(1) * max_repeat, text)