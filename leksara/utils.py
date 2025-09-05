"""Deprecated shim for legacy imports.

Use `from leksara import utils` or `from leksara.utils import ...` instead of importing from this module path.
This shim will be removed in a future release.
"""
from __future__ import annotations

import warnings as _warnings
from .utils import (  # type: ignore F401 (re-export)
    normalize_text,
    unicode_normalize_nfkc,
    strip_control_chars,
    load_text,
    load_json,
    get_compiled,
    clean_text,
    is_empty,
)

__all__ = [
    "normalize_text",
    "unicode_normalize_nfkc",
    "strip_control_chars",
    "load_text",
    "load_json",
    "get_compiled",
    "clean_text",
    "is_empty",
]

_warnings.warn(
    "leksara.utils (module) is deprecated; use 'from leksara.utils import ...' (package) instead.",
    DeprecationWarning,
    stacklevel=2,
)
