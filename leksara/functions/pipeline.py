from __future__ import annotations

# Backward-compat shim: re-export new implementation
from leksara.review_chain.pipeline import PipelineConfig, ReviewChain  # type: ignore

__all__ = ["PipelineConfig", "ReviewChain"]
