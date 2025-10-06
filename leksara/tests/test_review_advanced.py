import pytest
from leksara.functions.review.advanced import shorten_elongation

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

def test_review_advanced():
    pass
