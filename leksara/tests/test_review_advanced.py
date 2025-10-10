import pytest
import re
from leksara.functions.review.advanced import (
    replace_rating,
    shorten_elongation,
    replace_acronym,
    normalize_slangs,
    expand_contraction,
    word_normalization
)
import leksara.functions.review.advanced as adv  # untuk monkeypatching

@pytest.mark.parametrize("text, expected", [
    ("Hallooooo teman-temannn", "Halloo teman-temann"),
    ("Kerennnn bangettsss", "Kerenn bangettss"),
    ("Waahhh mantap jiwaaa", "Waahh mantap jiwaa"),
    ("Ini teks normal", "Ini teks normal"),
    ("Bagus", "Bagus"),
    ("aaaaa", "aa"),
    ("", ""),
])
def test_shorten_elongation_reduces_repeats_with_default_max(text, expected):
    assert shorten_elongation(text) == expected

@pytest.mark.parametrize("text, max_repeat, expected", [
    ("Mantuuulll", 1, "Mantul"),
    ("Gilaaa benarrr", 1, "Gila benar"),
    ("Tanggapan", 1, "Tangapan"),
    ("Wooooowwwww", 3, "Wooowww"),
    ("Kereeeen", 4, "Kereeeen"), 
])
def test_shorten_elongation_with_custom_max_repeat(text, max_repeat, expected):
    assert shorten_elongation(text, max_repeat=max_repeat) == expected

@pytest.mark.parametrize("invalid_max", [0, -1, -100])
def test_shorten_elongation_invalid_max_repeat_raises_value_error(invalid_max):
    with pytest.raises(ValueError, match="max_repeat must be >= 1"):
        shorten_elongation("tes", max_repeat=invalid_max)

def test_shorten_elongation_type_error_on_non_string():
    with pytest.raises(TypeError):
        shorten_elongation(12345)
        
def test_replace_rating():
    RATING_PLACEHOLDER = "__RATING_"

    def test_replace_rating_out_of_5_any():
        text = "Rating: 4,5/5 mantap"
        out = replace_rating(text)
        assert re.search(r"\d+(\.\d+)?", out)
        assert "4.5" in out or RATING_PLACEHOLDER in out

    def test_replace_rating_out_of_any_scale_normalizes():
        text = "Score: 8/10"
        out = replace_rating(text)
        rating_val = float(re.findall(r"\d+(\.\d+)?", out)[0])
        assert 0 <= rating_val <= 5

    def test_replace_rating_bintang_any_with_word_map():
        text = "kasih lima bintang"
        out = replace_rating(text)
        assert re.search(r"\d+(\.\d+)?", out)
        assert "5" in out or RATING_PLACEHOLDER in out

    def test_replace_rating_number_of_five():
        text = "4 of 5 for design"
        out = replace_rating(text)
        assert "4.0" in out and "of 5" not in out


    def test_replace_rating_rating_word_number():
        text = "rating: 5"
        out = replace_rating(text)
        assert "5" in out or RATING_PLACEHOLDER in out

    def test_replace_rating_stars_word_any():
        text = "3 stars overall"
        out = replace_rating(text)
        assert "3.0" in out and " stars" not in out

    def test_replace_rating_emoji_stars_sequence():
        text = "Kualitasnya ⭐⭐⭐⭐ top!"
        out = replace_rating(text)
        assert "4.0" in out and "⭐⭐⭐⭐" not in out

    def test_replace_rating_emoji_stars_multiplied():
        text = "Keren banget ⭐ x5, mantap!"
        out = replace_rating(text)
        assert "5.0" in out and "⭐ x5"

    def test_replace_rating_blacklist_ignored():
        text = "★"
        out = replace_rating(text)
        assert "★" in out

    def test_replace_rating_multiple_ratings_in_text():
        text = "Film A: 4/5, Film B: 3/5"
        out = replace_rating(text)
        placeholders_count = len(re.findall(RATING_PLACEHOLDER, out))
        assert placeholders_count >= 2 or re.findall(r"\d+(\.\d+)?", out)

    def test_replace_rating_type_error_on_non_string():
        with pytest.raises(TypeError):
            replace_rating(12345)

    def test_replace_rating_returns_original_if_no_pattern_found():
        text = "Tidak ada rating di sini"
        out = replace_rating(text)
        assert out == text

    def test_replace_rating_collapses_whitespace_after_replacement():
        text = "Rating:  4  /5   sangat bagus"
        out = replace_rating(text)
        assert "  " not in out

@pytest.fixture
def slang_env(monkeypatch):
    # controlled dictionary untuk slang
    monkeypatch.setattr(adv, "_SLANGS_DICT", {
        "brb": "be right back",
        "gw": "gue",
        "keren": "bagus",
        "sip": "oke",
        "kw": ["keren", "bagus"]
    }, raising=False)

    # default conflict rules kosong
    monkeypatch.setattr(adv, "_CONFLICT_RULES", {}, raising=False)

    return adv, monkeypatch

def test_replace_basic(slang_env):
    out = normalize_slangs("brb nanti ya")
    assert "be right back" in out
    assert "brb" not in out.lower()

def test_remove_mode_removes_tokens(slang_env):
    out = normalize_slangs("gw, nanti ya", mode="remove")
    assert "gw" not in out.lower()
    assert "nanti" in out

def test_case_insensitive_and_punctuation(slang_env):
    out = normalize_slangs("BRB!!!")
    assert "be right back" in out

def test_multiple_occurrences_and_boundaries(slang_env):
    s = "brb, brb. brb? gw brb"
    out = normalize_slangs(s)
    assert out.lower().count("be right back") == 4
    assert "gue" in out

def test_list_value_uses_first_item(slang_env):
    monkey_adv, mp = slang_env
    out = normalize_slangs("kw banget")
    assert "keren" in out
    assert "bagus" not in out 

def test_conflict_rule_applies_preferred(slang_env):
    monkey_adv, mp = slang_env
    mp.setattr(adv, "_SLANGS_DICT", {"gw": "gue"}, raising=False)

    fake_conflict = {
        "gw": {
            "rules": [
                {
                    "context_pattern": r"\baku\b",
                    "preferred": "saya"
                }
            ]
        }
    }
    mp.setattr(adv, "_CONFLICT_RULES", fake_conflict, raising=False)

    text1 = "gw aku nanti"
    out1 = normalize_slangs(text1)
    assert "saya" in out1

    text2 = "gw dia saja"
    out2 = normalize_slangs(text2)
    assert re.search(r"\bgw\b", out2, re.IGNORECASE)

def test_empty_slangs_returns_original(monkeypatch):
    monkeypatch.setattr(adv, "_SLANGS_DICT", {}, raising=False)
    txt = "brb gw keren"
    out = normalize_slangs(txt)
    assert out == txt

def test_non_string_raises_typeerror():
    with pytest.raises(TypeError):
        normalize_slangs(123)

def test_invalid_mode_raises_valueerror():
    with pytest.raises(ValueError):
        normalize_slangs("brb", mode="delete")

def test_review_advanced():
    pass
