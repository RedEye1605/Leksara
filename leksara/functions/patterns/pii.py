"""PII cleaning: remove/replace phone, address, email, id."""

import re

ADDRESS_COMPONENT_PATTERNS = {
    "street": r'\b(?:Jl\.?|Jalan|Gg\.?|Gang)\s+[A-Z0-9][A-Za-z0-9 ./-]*',
    "house_number": r'\b(?:No\.?|No|Nomor|Nomer|Nmr|#)\s*\w+\b',
    "rt_rw": r'\bRT\s*\d{1,2}\s*RW\s*\d{1,2}\b',
    "kelurahan": r'\bKel(?:urahan)?\.?\s+[A-Za-z][A-Za-z ./-]*\b',
    "kecamatan": r'\bKec(?:amatan)?\.?\s+[A-Za-z][A-Za-z ./-]*\b',
    "city": r'\b(?:Kab(?:upaten)?|Kota)\.?\s+[A-Za-z][A-Za-z ./-]*\b',
    "province": r'\bProv(?:insi)?\.?\s+[A-Za-z][A-Za-z ./-]*\b',
    "zip_code": r'\b\d{5}\b'
}

NIK_PATTERN = r"(?<!\d)(1[1-9]|21|[37][1-6]|5[1-3]|6[1-5]|[89][12])\d{2}\d{2}([04][1-9]|[1256][0-9]|[37][01])(0[1-9]|1[0-2])\d{2}\d{4}(?!\d)"
PHONE_PATTERN = r'((?:\+62|62|0)(?:\d{2,3}[- ]?){2,4}\d{2,4}\b)'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
ADDRESS_TRIGGER_PATTERN = r'\b(Jl\.?|Jalan|Gg\.?|Gang|RT|RW|Kel(?:urahan)?\.?|Kec(?:amatan)?\.?|Kab(?:upaten)?\.?|Kota|Prov(?:insi)?\.?|No\.?|Nomor)\b'

URL_PATTERN = r'((?:https?|ftp)://|www\.)[\w.-]+(/[\w./?=&%#:-]*)?'
POPULAR_TLDS = ['com', 'id', 'co.id', 'go.id', 'ac.id', 'net', 'org', 'xyz', 'info', 'io']
tlds_pattern_part = "|".join(POPULAR_TLDS)
URL_PATTERN_WITH_PATH = fr'\b[a-zA-Z0-9-]+\.(?:{tlds_pattern_part})\b(/[\w./?=&%#:-]*)?'

def remove_phone(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    def validate_and_replace(match):
        potential_number = match.group(0)
        cleaned_number = re.sub(r'[-\s]', '', potential_number)

        normalized_number = None
        if cleaned_number.startswith(('+62', '62')):
            normalized_number = '0' + re.sub(r'^\+?62', '', cleaned_number)
        elif cleaned_number.startswith('0'):
            normalized_number = cleaned_number

        if normalized_number and 10 <= len(normalized_number) <= 13:
            return ''

        return potential_number

    return re.sub(PHONE_PATTERN, validate_and_replace, text)

def replace_phone(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    def validate_and_replace(match):
        potential_number = match.group(0)
        cleaned_number = re.sub(r'[-\s]', '', potential_number)

        normalized_number = None
        if cleaned_number.startswith(('+62', '62')):
            normalized_number = '0' + re.sub(r'^\+?62', '', cleaned_number)
        elif cleaned_number.startswith('0'):
            normalized_number = cleaned_number

        if normalized_number and 10 <= len(normalized_number) <= 13:
            return '[PHONE_NUMBER]'

        return potential_number

    return re.sub(PHONE_PATTERN, validate_and_replace, text)


def remove_address(text: str, **kwargs) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    if not re.search(ADDRESS_TRIGGER_PATTERN, text, flags=re.IGNORECASE):
        return text
    
    replacement_token = ''
    processed_text = text

    patterns_to_run = []
    
    if not kwargs:
        patterns_to_run = ADDRESS_COMPONENT_PATTERNS.values()
    
    else:
        for component, pattern in ADDRESS_COMPONENT_PATTERNS.items():
            if kwargs.get(component, False):
                patterns_to_run.append(pattern)

    for pattern in patterns_to_run:
        processed_text = re.sub(pattern, replacement_token, processed_text, flags=re.IGNORECASE)

    processed_text = re.sub(r'\s{2,}', ' ', processed_text).strip()
    return processed_text
    

def replace_address(text: str, **kwargs) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    if not re.search(ADDRESS_TRIGGER_PATTERN, text, flags=re.IGNORECASE):
        return text
    
    replacement_token = '[ADDRESS]'
    processed_text = text

    patterns_to_run = []
    
    if not kwargs:
        patterns_to_run = ADDRESS_COMPONENT_PATTERNS.values()
    
    else:
        for component, pattern in ADDRESS_COMPONENT_PATTERNS.items():
            if kwargs.get(component, False):
                patterns_to_run.append(pattern)

    for pattern in patterns_to_run:
        processed_text = re.sub(pattern, replacement_token, processed_text, flags=re.IGNORECASE)
        
    processed_text = re.sub(r'\s{2,}', ' ', processed_text).strip()
    return processed_text

def remove_email(text: str)-> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(EMAIL_PATTERN, '', text)

def replace_email(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    

    return re.sub(EMAIL_PATTERN, '[EMAIL]', text)

def remove_id(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(NIK_PATTERN, '', text)

def replace_id(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    return re.sub(NIK_PATTERN, '[NIK]', text)

def remove_url(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    text = re.sub(URL_PATTERN, '', text, flags=re.IGNORECASE)
    
    text = re.sub(URL_PATTERN_WITH_PATH, '', text, flags=re.IGNORECASE)
    
    return text

def replace_url(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    text = re.sub(URL_PATTERN, '[URL]', text, flags=re.IGNORECASE)
    
    text = re.sub(URL_PATTERN_WITH_PATH, '[URL]', text, flags=re.IGNORECASE)
    
    return text
