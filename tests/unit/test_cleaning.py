from leksara import utils
from leksara.cleaning import remove_tags, case_normal, remove_whitespace


def test_case_and_whitespace():
    t = "<b>Halo</b>   Dunia\n"
    t = remove_tags(t)
    t = case_normal(t)
    t = remove_whitespace(t)
    assert t == "halo Dunia".lower()
