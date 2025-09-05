from leksara.utils import normalize_text


def test_unicode_normalize():
    assert normalize_text("e\u0301") == "é"
