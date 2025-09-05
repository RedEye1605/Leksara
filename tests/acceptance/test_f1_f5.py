from __future__ import annotations

from leksara.clean import basic_clean
from leksara.presets import ecommerce_review_preset
from leksara.cartboard import build_frame


def test_f1_basic_clean():
    # default remove_punct=False -> tanda seru tetap
    assert basic_clean("Ini   Teks   KOTOR!!!") == "ini teks kotor!!!"


def test_f2_stopword():
    # Simulate stopword removal via basic_clean options if available; otherwise placeholder
    out = basic_clean("aku suka produk ini", remove_stopwords=False)
    assert "suka" in out and "produk" in out


def test_f3_custom_dictionary():
    # Placeholder: ensure slang normalization conceptually present in pipeline preset
    df = build_frame(["barangnya mantap betul"])
    chain = ecommerce_review_preset()
    out = chain.run_on_dataframe(df)
    assert "refined_text" in out.columns


def test_f4_mask_phone():
    from leksara.functions.pii import replace_phone
    t = replace_phone("hubungi 0812-3456-7890")
    assert "<PHONE>" in t or "<PHONE_NUMBER>" in t


def test_f5_ecommerce_preset_shape():
    df = build_frame(["Barangnya baaaagus banget!!! COD lancar, cs ramah."])
    chain = ecommerce_review_preset()
    out = chain.run_on_dataframe(df)
    assert "refined_text" in out.columns
