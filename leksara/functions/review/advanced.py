"""Advanced review mining: rating, elongation, acronym, slang, contraction, normalization."""

import re
import pandas as pd
import json
import pathlib as Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# buat stemmer sekali saja (hemat waktu)
_factory = StemmerFactory()
_STEMMER = _factory.create_stemmer()

try:
    config_path = Path(__file__).resolve().parent.parent.parent / "resources" / "regex_patterns" / "rating_patterns.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        _RATING_CONFIG = json.load(f)
        rules = _RATING_CONFIG.get('rules', [])
        _SORTED_RULES = sorted(rules, key=lambda r: r.get('priority', 0), reverse=True)

        blacklist = _RATING_CONFIG.get('blacklist', [])
        _BLACKLIST_PATTERNS = [re.compile(item['pattern'], re.IGNORECASE | re.MULTILINE) for item in blacklist]
        _FLAGS = _RATING_CONFIG.get('defaults', {}).get('flags', [])
except Exception as e:
    print(f"Gagal memuat file konfigurasi: {e}")
    _RATING_CONFIG = {}
    _SORTED_RULES = []
    _BLACKLIST_PATTERNS = []
    _FLAGS = []

try:
    dict_path = Path(__file__).resolve().parent.parent.parent / "resources" / "dictionary" / "acronym_dict.json"
    rules_path = Path(__file__).resolve().parent.parent.parent / "resources" / "dictionary" / "dictionary_rules.json"
    with open(dict_path, 'r', encoding='utf-8') as f:
        _ACRONYM_DICT = json.load(f)
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules_data = json.load(f).get("sections", {}).get("acronym", {}).get("conflict_rules", [])
        _CONFLICT_RULES = {rule["token"]: rule for rule in rules_data}
except Exception as e:
    print(f"Gagal memuat file konfigurasi akronim: {e}")
    _ACRONYM_DICT = {}
    _CONFLICT_RULES = {}

def replace_rating(text: str) -> str:
    if not isinstance(text, str) or not text:
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    flag_pattern = 0
    for pattern in _FLAGS:
        flag_object = getattr(re, pattern.upper(), 0)
        flag_pattern |= flag_object

    processed_text = text
    placeholder_map = {}
    counter = [0]

    def make_placeholder(val):
        idx = counter[0]
        counter[0] += 1
        ph = f"__RATING_{idx}__"
        placeholder_map[ph] = val
        return ph

    for rule in _SORTED_RULES:
        initial_pattern = rule.get("trigger_pattern", rule.get("pattern", ""))

        def replacer(match):
            matched_text = match.group(0)

            for bp in _BLACKLIST_PATTERNS:
                if bp.match(matched_text):
                    return matched_text

            raw_value = None
            rule_type = rule.get('type')

            if rule_type == 'extract':
                vg = rule.get('value_group', 0)
                try:
                    raw_value = match.group(vg)
                except IndexError:
                    raw_value = None

            elif rule_type in ['extract_multi', 'extract_or_map']:
                target_match = match
                if "trigger_pattern" in rule:
                    extraction_pattern = rule.get("pattern", "")
                    extraction_match = re.search(extraction_pattern, matched_text, flags=flag_pattern)
                    if not extraction_match:
                        return matched_text
                    target_match = extraction_match

                value_group_list = rule.get('value_groups') or ([rule.get('value_group')] if 'value_group' in rule else [])
                word_group_list = rule.get('word_groups') or ([rule.get('word_group')] if 'word_group' in rule else [])

                for group_idx in value_group_list:
                    if group_idx and group_idx <= len(target_match.groups()) and target_match.group(group_idx):
                        captured_value = target_match.group(group_idx).lower()
                        if re.fullmatch(r'\d+(?:[.,]\d+)?', captured_value):
                            raw_value = captured_value
                            break

                if raw_value is None:
                    for group_idx in word_group_list:
                        if group_idx and group_idx <= len(target_match.groups()) and target_match.group(group_idx):
                            word = target_match.group(group_idx).lower()
                            raw_value = rule.get('word_map', {}).get(word)
                            if raw_value is not None:
                                break

            elif rule_type == 'emoji_or_mult':
                mult_group_idx = rule.get('mult_group')
                if mult_group_idx and mult_group_idx <= len(match.groups()) and match.group(mult_group_idx):
                    raw_value = match.group(mult_group_idx)
                else:
                    count = 0
                    s = match.group(0)
                    for e in rule.get('emojis', []):
                        count += s.count(e)
                    raw_value = count

            if raw_value is None: return matched_text

            str_value = str(raw_value)
            for old, new in rule.get('postprocess', {}).get('replace', {}).items():
                str_value = str_value.replace(old, new)

            try:
                str_value = str_value.replace('½', '.5').replace('1/2', '.5')
                rating = float(str_value)

                if 'scale_denominator_group' in rule:
                    scale_group_idx = rule['scale_denominator_group']
                    scale_str = None
                    try:
                        scale_str = match.group(scale_group_idx)
                    except IndexError:
                        m2 = re.search(rule.get('pattern', ''), matched_text, flags=flag_pattern)
                        if m2:
                            try:
                                scale_str = m2.group(scale_group_idx)
                            except IndexError:
                                scale_str = None

                    if scale_str is not None:
                        scale = float(scale_str.replace(',', '.'))
                        if scale != 5.0 and scale > 0:
                            rating = (rating / scale) * 5.0

                min_val, max_val = rule.get('clamp', [None, None])
                if min_val is not None and rating < min_val:
                    rating = min_val
                if max_val is not None and rating > max_val:
                    rating = max_val


                final_string = str(round(rating, 2))
                ph = make_placeholder(final_string)

                if "trigger_pattern" in rule and rule.get("pattern"):
                    try:
                        new_inner = re.sub(rule.get("pattern", ""), ph, matched_text, count=1, flags=flag_pattern)
                        return new_inner
                    except re.error:
                        leading = re.match(r'^\s*', matched_text).group(0)
                        trailing = re.search(r'\s*$', matched_text).group(0)
                        return f"{leading}{ph}{trailing}"
                
                leading = re.match(r'^\s*', matched_text).group(0)
                trailing = re.search(r'\s*$', matched_text).group(0)
                return f"{leading}{ph}{trailing}"

            except Exception:
                return matched_text
        processed_text = re.sub(initial_pattern, replacer, processed_text, flags=flag_pattern)
    
    for ph, val in placeholder_map.items():
        processed_text = processed_text.replace(ph, val)
    
    processed_text = re.sub(r'\s{2,}', ' ', processed_text).strip()
    return processed_text

def shorten_elongation(text: str, max_repeat: int = 2) -> str:
    """Kurangi pengulangan karakter hingga maksimal `max_repeat` kemunculan.

    Contoh: mantuuulll -> mantul (dengan max_repeat=1 atau 2 sesuai preferensi)
    
    TODO: Implementasi fungsi ini oleh kontributor selanjutnya.
    """
    if max_repeat < 1:
        raise ValueError("max_repeat must be >= 1")

    # Regex: (.)\1{n,} menangkap karakter yang diulang lebih dari n kali
    else:
        pattern = re.compile(r"(.)\1{" + str(max_repeat) + r",}")
        text = pattern.sub(lambda m: m.group(1) * max_repeat, text)

    return text

def replace_acronym(text: str, mode: str = "remove")-> str:
    if not isinstance(text, str):
        raise TypeError(f"Input harus berupa string, tetapi menerima tipe {type(text).__name__}")

    allowed_modes = {"remove", "replace"}
    if mode not in allowed_modes:
        raise ValueError(f"Mode '{mode}' tidak valid. Pilihan yang tersedia adalah {list(allowed_modes)}")

    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in _ACRONYM_DICT.keys()) + r')\b', re.IGNORECASE)

    def replacer(match):
        acronym = match.group(0).lower()
        replacement = None

        if acronym in _CONFLICT_RULES:
            conflict = _CONFLICT_RULES[acronym]
            for rule in conflict.get("rules", []):
                if re.search(rule["context_pattern"], text, re.IGNORECASE):
                    replacement = rule["preferred"]
                    break
            if replacement is None:
                return match.group(0)
        else:
            standard_replacement = _ACRONYM_DICT.get(acronym)
            if isinstance(standard_replacement, list):
                replacement = standard_replacement[0]
            else:
                replacement = standard_replacement

        if mode == "replace":
            return replacement
        elif mode == "remove":
            return ""

    return pattern.sub(replacer, text)


def normalize_slangs(text):
    pass

def expand_contraction(text):
    pass

# Deteksi placeholder whitelist (Private Use Area) agar tidak di-stem
def _is_masked_whitelist_token(token: str) -> bool:
    return any(0xE000 <= ord(ch) <= 0xF8FF for ch in token)

def _is_bracket_token(token: str) -> bool:
    return len(token) >= 2 and token.startswith("[") and token.endswith("]")

def word_normalization(
    text: str,
    *,
    method: str = "stem",
    word_list=None,
    mode: str = "keep",
) -> str:
    """Normalisasi kata dengan stemming/lemmatization.

    Args:
        text: input string
        method: "stem" (default, pakai Sastrawi), "lemma" (future).
        word_list: daftar kata spesial (list[str])
        mode: 
            - "keep": jangan stem kata dalam word_list
            - "only": hanya stem kata dalam word_list
    """
    if not isinstance(text, str):
        return text

    if word_list is None:
        word_list = []

    word_set = {w.lower() for w in word_list}
    words = text.split()
    out = []

    if method == "stem":
        if mode == "keep":
            for w in words:
                # Lindungi placeholder whitelist dan token bracket
                if _is_masked_whitelist_token(w) or _is_bracket_token(w):
                    out.append(w)
                else:
                    out.append(w if w.lower() in word_set else _STEMMER.stem(w))
        elif mode == "only":
            for w in words:
                if _is_masked_whitelist_token(w) or _is_bracket_token(w):
                    out.append(w)
                else:
                    out.append(_STEMMER.stem(w) if w.lower() in word_set else w)
        else:
            raise ValueError("mode harus 'keep' atau 'only'")
    else:
        # kalau nanti ada lemmatizer lain
        out = words

    return " ".join(out)
