from __future__ import annotations

# Backward-compat shim for CartBoard
from leksara.cartboard.frame import build_frame, REQUIRED_COLUMNS  # type: ignore

__all__ = ["build_frame", "REQUIRED_COLUMNS"]
