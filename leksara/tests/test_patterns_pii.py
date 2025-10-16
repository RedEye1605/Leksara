import pytest

from leksara.functions.patterns.pii import (
    replace_phone, replace_address,
    replace_email, replace_id
)

# Constants for placeholders
ADDRESS_PLACEHOLDER = "[ADDRESS]"
PHONE_PLACEHOLDER = "[PHONE]"
EMAIL_PLACEHOLDER = "[EMAIL]"
ID_PLACEHOLDER = "[ID]"

def test_replace_address_mode_replace_masks_full_address():
    text = "Alamatku di Jl. Merdeka No. 12 RT 02 RW 03, Jakarta"
    out = replace_address(text, mode="replace")
    assert "Jl." not in out and "RT" not in out and "Jakarta" not in out
    assert ADDRESS_PLACEHOLDER in out

def test_replace_address_mode_remove_deletes_address_but_keeps_other_text():
    text = "Alamat kantor: Jl. Merdeka No. 12. Silakan datang."
    out = replace_address(text, mode="remove")
    assert "Jl." not in out
    assert "Silakan datang" in out or "Silakan" in out

def test_replace_address_with_component_kwargs_only_runs_selected_component():
    text = "Rumah saya: Jl. Kenanga 7 RT 03 RW 05, Surabaya"
    out = replace_address(text, mode="replace", rtrw=True)
    assert "[ADDRESS]" in out
    assert "RT" not in out and "RW" not in out

def test_replace_address_unknown_kwarg_raises_keyerror():
    with pytest.raises(KeyError):
        replace_address("Jl. Something 10", foobar=True)

def test_replace_address_type_error_on_non_string():
    with pytest.raises(TypeError):
        replace_address(999)

def test_replace_address_returns_original_if_no_trigger():
    text = "This text has no address trigger words."
    out = replace_address(text, mode="replace")
    assert out == text

def test_replace_address_collapses_excess_whitespace_after_removal():
    text = "Alamat: Jl. Kenanga No. 7     RT 05 RW 02    Surabaya"
    out = replace_address(text, mode="remove")
    assert "  " not in out