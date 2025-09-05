from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Iterable, Any

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

Step = Callable[[str], str]


@dataclass
class PipelineConfig:
    steps: list[tuple[str, Step]]
    benchmark: bool = False


class ReviewChain:
    def __init__(self, config: PipelineConfig):
        self.config = config

    def run_on_series(self, s: "pd.Series") -> "pd.Series":  # type: ignore[name-defined]
        timings: list[tuple[str, float]] = []
        out = s.astype(str)
        for name, fn in self.config.steps:
            t0 = time.perf_counter()
            out = out.apply(fn)
            if self.config.benchmark:
                timings.append((name, time.perf_counter() - t0))
        if self.config.benchmark:
            out.attrs["benchmark_timings"] = timings
            out.attrs["benchmark_total"] = sum(t for _, t in timings)
        return out

    def run_on_dataframe(self, df: "pd.DataFrame", in_col: str = "original_text", out_col: str = "refined_text") -> "pd.DataFrame":  # type: ignore[name-defined]
        df = df.copy()
        df[out_col] = self.run_on_series(df[in_col])
        return df


def review_chain(steps: list[tuple[str, Step]], benchmark: bool = False) -> ReviewChain:
    """Factory sederhana untuk membuat ReviewChain."""
    return ReviewChain(PipelineConfig(steps=steps, benchmark=benchmark))
