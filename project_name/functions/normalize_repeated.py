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
    # Hanya normalisasi jika pengulangan >= max_repeat+1
    if max_repeat == 1:
        pattern = re.compile(r"(.)\1{" + str(max_repeat+1) + r",}")
    else: 
        pattern = re.compile(r"(.)\1{" + str(max_repeat) + r",}")
    return pattern.sub(lambda m: m.group(1) * max_repeat, text)

if __name__ == "__main__":
    print(normalize_repeated("hello everrryoonneeeee", max_repeat=1))
    # 👉 "pekerjaan mereka itu jelek sekali"  ✅
    
    print(normalize_repeated("hello everrryoonneeeee", max_repeat=2))