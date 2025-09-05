from leksara.cartboard import build_frame
from leksara.pipeline import PipelineConfig, ReviewChain


def test_pipeline_end_to_end():
    df = build_frame(["Barang OK, harga murah."])
    chain = ReviewChain(PipelineConfig(steps=[("identity", lambda t: t)]))
    out = chain.run_on_dataframe(df)
    assert out.loc[0, "refined_text"] == "Barang OK, harga murah."
