import re

def normalize_whitespace(text):
    """ Menormalkan spasi dalam teks. """
    return re.sub(r'\s+', ' ', text).strip()
