import pandas as pd
from leksara.cartboard import build_frame, REQUIRED_COLUMNS


def test_build_frame_columns():
    df = build_frame(["halo"], [5])
    assert list(df.columns) == REQUIRED_COLUMNS
    assert df.loc[0, "original_text"] == "halo"
    assert df.loc[0, "rating"] == 5
