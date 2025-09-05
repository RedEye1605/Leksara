import re
import string
#Adit
""" pattern email"""
def email_masking(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    return re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[EMAIL]', text)


