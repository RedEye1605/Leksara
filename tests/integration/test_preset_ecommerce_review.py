from leksara.cartboard import build_frame
from leksara.presets import ecommerce_review_preset


def test_preset_end_to_end():
    df = build_frame(["Barangnya baaaagus banget!!! COD lancar, cs ramah."])
    chain = ecommerce_review_preset()
    out = chain.run_on_dataframe(df)
    assert "refined_text" in out.columns
