import re
#Althaf
def normalize_repeated(text: str, max_repeat: int = 2) -> str:
    """Kurangi pengulangan karakter hingga maksimal `max_repeat` kemunculan.

    Contoh: mantuuulll -> mantul (dengan max_repeat=1 atau 2 sesuai preferensi)
    
    TODO: Implementasi fungsi ini oleh kontributor selanjutnya.
    """
    if max_repeat < 1:
        raise ValueError("max_repeat must be >= 1")

    # Regex: (.)\1{n,} menangkap karakter yang diulang lebih dari n kali
    if max_repeat == 1:
        # Khusus akhir kata: 2+ pengulangan -> 1
        # (.)\1+ artinya ada minimal 1 pengulangan setelah char pertama -> total ≥2
        text = re.sub(r"(.)\1+\b", r"\1", text)

        # Umum (bukan akhir kata): 3+ pengulangan -> 1
        text = re.sub(r"(.)\1{2,}", r"\1", text)
    else:
        # Umum untuk max_repeat >= 2
        pattern = re.compile(r"(.)\1{" + str(max_repeat) + r",}")
        text = pattern.sub(lambda m: m.group(1) * max_repeat, text)

    return text