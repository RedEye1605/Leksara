"""PII cleaning: remove/replace phone, address, email, id."""

import re

def remove_phone(text):
    pass

def replace_phone(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    pattern = r'((?:08|\+628)[-\s\d]{8,15}\d)'
    
    def validate_and_replace(match):
        potential_number = match.group(0)
        
        cleaned_number = re.sub(r'[-\s]', '', potential_number)
        
        if cleaned_number.startswith(('08', '+628')):
            # Cek panjang sisa digitnya
            if 8 <= len(re.sub(r'^(08|\+628)', '', cleaned_number)) <= 11:
                return '[PHONE_NUMBER]'
        
        return potential_number


    return re.sub(pattern, validate_and_replace, text)

def remove_address(text):
    pass

def replace_address(text):
    pass

def remove_email(text):
    pass

def replace_email(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    return re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[EMAIL]', text)

def remove_id(text):
    pass

def replace_id(text):
    pass
