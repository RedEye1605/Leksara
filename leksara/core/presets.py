"""Presets for review pipelines (e.g., ecommerce_review)."""

def ecommerce_review():
    from ..functions.cleaner.basic import (
        remove_tags, case_normal, remove_whitespace, remove_stopwords
    )
    from ..functions.patterns.pii import replace_phone, replace_email
    from ..functions.review.advanced import shorten_elongation
    # urutan: masking/normalisasi dasar → domain tweaks
    return [
        replace_phone, replace_email,
        remove_tags, case_normal, remove_whitespace,
        remove_stopwords, shorten_elongation
    ]

PRESETS = {
    "ecommerce_review": ecommerce_review
}

def get_preset(name):
    if name not in PRESETS:
        raise ValueError(f"Preset '{name}' tidak ditemukan.")
    return PRESETS[name]()
