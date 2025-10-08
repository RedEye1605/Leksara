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

def test_review_advanced():
    pass
