from __future__ import annotations

import regex as re

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore


def detect_flags(text: str) -> dict[str, bool]:
    """Detect metadata flags from a single text.

    - pii_flag: phone/email pattern present.
    - non_alphabetical_flag: contains no letters at all.
    - lang_mix_flag: mix of Latin [A-Za-z] and other letter scripts.
    - rating_flag: rating-like pattern present (e.g., 5/5, ⭐, "bintang 4").
    """
    pii = bool(
        re.search(
            r"(?:\+?62|0)(?:\d[ -]?){8,13}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )
    )
    non_alpha = not bool(re.search(r"\p{L}", text))
    lang_mix = bool(re.search(r"[A-Za-z].*[\p{L}&&[^A-Za-z]]|[\p{L}&&[^A-Za-z]].*[A-Za-z]", text))
    rating_like = bool(
        re.search(
            r"\b[1-5]\s*/\s*5\b|\u2b50|\uFE0F|\u2605|\bbintang\s*[1-5]\b|\brating\b",
            text,
            flags=re.IGNORECASE,
        )
    )
    return {
        "pii_flag": pii,
        "non_alphabetical_flag": non_alpha,
        "lang_mix_flag": lang_mix,
        "rating_flag": rating_like,
    }


def annotate_flags(df: "pd.DataFrame", text_col: str = "original_text") -> "pd.DataFrame":  # type: ignore[name-defined]
    """Compute flags for all rows based on the given text column.

    Adds/updates columns: pii_flag, non_alphabetical_flag, lang_mix_flag, rating_flag.
    Returns a new DataFrame copy.
    """
    if pd is None:  # pragma: no cover
        raise RuntimeError("pandas is required to annotate flags")
    out = df.copy()
    flags_series = out[text_col].astype(str).apply(detect_flags)
    out["pii_flag"] = flags_series.apply(lambda d: d["pii_flag"])  # type: ignore[index]
    out["non_alphabetical_flag"] = flags_series.apply(lambda d: d["non_alphabetical_flag"])  # type: ignore[index]
    out["lang_mix_flag"] = flags_series.apply(lambda d: d["lang_mix_flag"])  # type: ignore[index]
    out["rating_flag"] = flags_series.apply(lambda d: d["rating_flag"])  # type: ignore[index]
    return out
