from __future__ import annotations

from functools import lru_cache
import regex as re


@lru_cache(maxsize=256)
def get_compiled(pattern: str, flags: int = 0) -> re.Pattern:
    return re.compile(pattern, flags)
