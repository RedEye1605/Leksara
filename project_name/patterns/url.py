import re
import string
#Adit
""" pattern url"""
def url_masking(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    pattern = r'((?:https?|ftp)://|www\.)[\w\.-]+(/\S*)?'
    
    return re.sub(pattern, '[URL]', text)
    

