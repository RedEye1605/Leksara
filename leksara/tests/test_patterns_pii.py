import pytest

from leksara.functions.patterns.pii import (
    replace_phone,
    replace_address,
    replace_email,
    replace_id
)


def test_replace_phone():
    PHONE_PLACEHOLDER = "[PHONE_NUMBER]"

    def test_replace_phone_mode_replace_masks_valid_number():
        text = "Hubungi saya di +6281234567890 untuk info lebih lanjut."
        out = replace_phone(text, mode="replace")
        assert PHONE_PLACEHOLDER in out
        assert "+628" not in out and "812" not in out


    def test_replace_phone_mode_remove_deletes_valid_number():
        text = "Nomor saya 081234567890, jangan disebar ya."
        out = replace_phone(text, mode="remove")
        assert "0812" not in out
        assert "jangan disebar" in out


    def test_replace_phone_leaves_invalid_short_numbers():
        text = "Kode akses: 12345."
        out = replace_phone(text, mode="replace")
        assert "12345" in out
        assert PHONE_PLACEHOLDER not in out


    def test_replace_phone_handles_numbers_with_spaces_and_dashes():
        text = "Nomor alternatif: +62 812-3456-7890"
        out = replace_phone(text, mode="replace")
        assert PHONE_PLACEHOLDER in out
        assert "+" not in out and "812" not in out


    def test_replace_phone_normalizes_and_detects_62_prefix():
        text = "Kontak resmi: 6281234567890"
        out = replace_phone(text, mode="replace")
        assert PHONE_PLACEHOLDER in out


    def test_replace_phone_normalizes_and_detects_plus62_prefix():
        text = "Nomor darurat: +6282234567890"
        out = replace_phone(text, mode="replace")
        assert PHONE_PLACEHOLDER in out


    def test_replace_phone_ignores_non_indonesian_like_numbers():
        text = "Hubungi kantor pusat di +11234567890."
        out = replace_phone(text, mode="replace")
        assert "+1" in out
        assert PHONE_PLACEHOLDER not in out


    def test_replace_phone_mode_remove_collapses_whitespace():
        text = "Nomor: 0812 3456 7890   aktif"
        out = replace_phone(text, mode="remove")
        assert "  " not in out
        assert "aktif" in out


    def test_replace_phone_with_multiple_numbers_in_text():
        text = "Kontak A: 081234567890, Kontak B: +628987654321"
        out = replace_phone(text, mode="replace")
        assert out.count(PHONE_PLACEHOLDER) == 2
        assert "0812" not in out and "8987" not in out


    def test_replace_phone_with_parentheses_variation():
        text = "Nomor kantor (+62) 812-3456-7890 aktif"
        out = replace_phone(text, mode="replace")
        assert PHONE_PLACEHOLDER in out


    def test_replace_phone_type_error_on_non_string():
        with pytest.raises(TypeError):
            replace_phone(12345)


    def test_replace_phone_invalid_mode_raises_valueerror():
        with pytest.raises(ValueError):
            replace_phone("081234567890", mode="delete")


    def test_replace_phone_returns_original_if_no_pattern_found():
        text = "Tidak ada nomor di sini."
        out = replace_phone(text, mode="replace")
        assert out == text

def test_patterns_pii():
    pass
