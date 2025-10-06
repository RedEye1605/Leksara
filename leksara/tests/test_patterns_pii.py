import re
import pytest
from leksara.functions.patterns.pii import replace_email, replace_address

EMAIL_PLACEHOLDER = "[EMAIL]"
ADDRESS_PLACEHOLDER = "[ADDRESS]"
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", flags=re.IGNORECASE) # email is case insensitive

@pytest.mark.parametrize("text", [
    "Kontak: john.doe@example.com",
    "Send to: jane_smith@sub.domain.co.id, thanks.",
    "multiple: a@b.com and c_d@x.org"
])
def test_replace_email_mode_replace_replaces_all(text):
    out = replace_email(text, mode="replace")
    assert EMAIL_REGEX.search(out) is None, f"Email masih ada di output: {out}"
    assert EMAIL_PLACEHOLDER in out

def test_replace_email_mode_remove_removes_emails():
    text = "Email saya: User@test.com"
    out = replace_email(text, mode="remove")
    assert EMAIL_REGEX.search(out) is None
    assert EMAIL_PLACEHOLDER not in out
    assert out != text

def test_replace_email_type_error_on_non_string():
    with pytest.raises(TypeError):
        replace_email(123)

def test_replace_email_invalid_mode():
    with pytest.raises(ValueError):
        replace_email("a@b.com", mode="invalid_mode")

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
