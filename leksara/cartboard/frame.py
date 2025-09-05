from __future__ import annotations

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

REQUIRED_COLUMNS = [
    "original_text",
    "refined_text",
    "rating",
    "rating_flag",
    "pii_flag",
    "non_alphabetical_flag",
    "lang_mix_flag",
]


def build_frame(texts: list[str] | "pd.Series", ratings: list[int] | "pd.Series" | None = None) -> "pd.DataFrame":  # type: ignore[name-defined]
    if pd is None:  # pragma: no cover
        raise RuntimeError("pandas is required to build the cartboard frame")
    df = pd.DataFrame({"original_text": list(texts)})
    if ratings is not None:
        df["rating"] = list(ratings)
    else:
        df["rating"] = pd.NA

    df["refined_text"] = pd.Series([None] * len(df), dtype="object")
    df["rating_flag"] = False
    df["pii_flag"] = False
    df["non_alphabetical_flag"] = False
    df["lang_mix_flag"] = False
    return df[REQUIRED_COLUMNS]


def build_frame_from_df(df: "pd.DataFrame", text_col: str = "review_text", rating_col: str | None = None) -> "pd.DataFrame":  # type: ignore[name-defined]
    """Create a standardized cartboard frame from an existing DataFrame.

    - text_col: source column for original_text.
    - rating_col: optional source column for rating.
    """
    if pd is None:  # pragma: no cover
        raise RuntimeError("pandas is required to build the cartboard frame")
    src = df.copy()
    out = pd.DataFrame()
    out["original_text"] = src[text_col].astype(str)
    out["refined_text"] = pd.Series([None] * len(out), dtype="object")
    if rating_col and rating_col in src:
        out["rating"] = src[rating_col]
    else:
        out["rating"] = pd.NA
    out["rating_flag"] = False
    out["pii_flag"] = False
    out["non_alphabetical_flag"] = False
    out["lang_mix_flag"] = False
    return out[REQUIRED_COLUMNS]
