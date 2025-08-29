import re
import string
#Adit
""" menghapus tanda baca pada teks"""
def remove_punctuation(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(r'[^\w\s]', '', text)

