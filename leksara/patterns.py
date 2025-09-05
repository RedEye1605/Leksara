from __future__ import annotations

"""Pipeline-friendly callables exposed at top-level: leksara.patterns.

These functions are simple str->str callables to be used in custom pipelines.
"""

from .functions.pii import (
    replace_phone as MASK_PHONE,
    replace_email as MASK_EMAIL,
    replace_address as MASK_ADDRESS,
    replace_id as MASK_ID,
)
from .functions.to_lowercase import to_lowercase as TO_LOWER

__all__ = [
    "MASK_PHONE",
    "MASK_EMAIL",
    "MASK_ADDRESS",
    "MASK_ID",
    "TO_LOWER",
]
