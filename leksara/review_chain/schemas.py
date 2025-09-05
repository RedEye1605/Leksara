from __future__ import annotations

from typing import TypedDict, Callable


class StepConfig(TypedDict):
    name: str
    fn: Callable[[str], str]
