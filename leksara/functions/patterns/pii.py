"""PII cleaning: remove/replace phone, address, email, id."""
import os
import re
import json
from pathlib import Path

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

def replace_phone(text: str, mode: str = "remove") -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    replacement_token = '[PHONE_NUMBER]' if mode == "replace" else ''

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    replacement_token = '[PHONE_NUMBER]' if mode == "replace" else ''

    def validate_and_replace(match):
        potential_number = match.group(0)
        cleaned_number = re.sub(r'[-\s]', '', potential_number)

        normalized_number = None
        if cleaned_number.startswith(('+62', '62')):
            normalized_number = '0' + re.sub(r'^\+?62', '', cleaned_number)
        elif cleaned_number.startswith('0'):
            normalized_number = cleaned_number

        if normalized_number and 10 <= len(normalized_number) <= 13:
            return replacement_token

        return potential_number
    
    PHONE_PATTERN = phone_config.get("pattern", "")
    return re.sub(PHONE_PATTERN, validate_and_replace, text)


def replace_address(text: str, mode: str = "remove", **kwargs) -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")
    
    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")
    
    replacement_token = '[ADDRESS]' if mode == "replace" else ''

    if not re.search(ADDRESS_TRIGGER_PATTERN, text, flags=re.IGNORECASE):
        return text

    processed_text = text

    replacement_token = '[ADDRESS]' if mode == "replace" else ''

    trigger_config = address_config.get("trigger_pattern", {})
    trigger_pattern = trigger_config.get("pattern", "")
    address_components = address_config.get("components", {})
    processed_text = re.sub(r'\s{2,}', ' ', processed_text).strip()
    return processed_text


def replace_email(text: str, mode: str = "remove")-> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    replacement_token = '[EMAIL]' if mode == "replace" else ''

    return re.sub(EMAIL_PATTERN, replacement_token, text)


def replace_id(text: str, mode: str = "remove") -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    replacement_token = '[NIK]' if mode == "replace" else ''

    return re.sub(NIK_PATTERN, replacement_token, text)

def replace_url(text: str, mode: str = "remove") -> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    replacement_token = '[URL]' if mode == "replace" else ''

    text = re.sub(URL_PATTERN, replacement_token, text, flags=re.IGNORECASE)

    text = re.sub(URL_PATTERN_WITH_PATH, replacement_token, text, flags=re.IGNORECASE)

    return text
