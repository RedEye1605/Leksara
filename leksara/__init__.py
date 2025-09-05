from __future__ import annotations

from typing import Callable, Any, Iterable

from .clean import basic_clean
from .presets import get_preset, apply_preset
from .review_chain.pipeline import review_chain
from .cartboard.frame import build_frame
from .cartboard import annotate_flags, build_frame_from_df
from . import review_cleaner, user_brush, review_miner
from . import patterns  # top-level patterns for pipelines

try:  # optional pandas
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

__all__ = [
    "basic_clean",
    "review_chain",
    "get_preset",
    "apply_preset",
    "build_frame",
    "build_frame_from_df",
    "annotate_flags",
    "review_cleaner",
    "user_brush",
    "review_miner",
    "patterns",
    "leksara",
]


def _build_chain_from_pipeline(pipeline: dict):
    """Build a simple ReviewChain from a pipeline dict {'patterns': [...], 'functions': [...]}"""
    steps: list[tuple[str, Callable[[str], str]]] = []
    for i, fn in enumerate((pipeline.get("patterns") or [])):
        name = getattr(fn, "__name__", f"pattern_{i}")
        steps.append((name, fn))
    for j, fn in enumerate((pipeline.get("functions") or [])):
        name = getattr(fn, "__name__", f"function_{j}")
        steps.append((name, fn))
    return review_chain(steps)


def leksara(
    data: Any,
    *,
    pipeline: dict | None = None,
    in_col: str | None = None,
    out_col: str = "refined_text",
):
    """High-level runner for custom pipelines.

    - Accepts pandas.Series, pandas.DataFrame, list/iterable[str], or str.
    - pipeline should be {'patterns': [callables], 'functions': [callables]} where callables are str->str.
    """
    if not pipeline:
        raise ValueError("pipeline is required")
    chain = _build_chain_from_pipeline(pipeline)

    if pd is not None and isinstance(data, pd.Series):  # type: ignore[attr-defined]
        return chain.run_on_series(data)
    if pd is not None and isinstance(data, pd.DataFrame):  # type: ignore[attr-defined]
        col = in_col
        if col is None:
            if "original_text" in data.columns:
                col = "original_text"
            elif "review_text" in data.columns:
                col = "review_text"
            else:
                raise ValueError("in_col must be provided for DataFrame input")
        return chain.run_on_dataframe(data, in_col=col, out_col=out_col)
    if isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
        # pure-Python apply sequence
        f: Callable[[str], str] = lambda x: x
        for _, step in chain.config.steps:  # type: ignore[attr-defined]
            prev = f
            f = (lambda p, s: (lambda x: s(p(x))))(prev, step)
        return [f(str(t)) for t in data]
    if isinstance(data, str):
        out = data
        for _, step in chain.config.steps:
            out = step(out)
        return out
    raise TypeError("Unsupported input type for leksara()")
