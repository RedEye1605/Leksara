import re
#Adit
def remove_digits(text: str) -> str:
    """menghapus bilangan pada teks"""
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(r'\d+', '', text)

