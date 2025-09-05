from leksara.miner import shorten_elongation, replace_acronym, normalize_slangs


def test_miner_basics():
    text = "baaaagus COD bgt"
    text = shorten_elongation(text)
    text = replace_acronym(text, {"COD": "bayar di tempat"})
    text = normalize_slangs(text, {"bgt": "banget"})
    assert "bagus" in text and "bayar di tempat" in text and "banget" in text
