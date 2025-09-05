from leksara.pii import replace_phone, replace_email, replace_address, replace_id


def test_replace_pii():
    t = "Hubungi 0812-3456-7890 atau a@b.com di Jl. Mawar No.1 NIK 1234 5678 9012 3456"
    t = replace_phone(t)
    t = replace_email(t)
    t = replace_address(t)
    t = replace_id(t)
    assert "<PHONE>" in t and "<EMAIL>" in t and "<ADDRESS>" in t and "<ID>" in t
