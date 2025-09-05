"""Deprecated module. Import from `leksara.presets` instead."""
from __future__ import annotations
import warnings as _warnings

from leksara.presets import *  # re-export

_warnings.warn(
	"leksara.functions.presets is deprecated; use leksara.presets",
	DeprecationWarning,
	stacklevel=2,
)
