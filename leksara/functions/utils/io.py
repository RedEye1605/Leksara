from __future__ import annotations

from importlib import resources
import json
from typing import Iterable


def load_text_lines(package: str | None, resource: str | None = None) -> list[str]:
    """
    Load text lines either from a path-like (if package is a file path) or from
    package resources when using (package, resource).
    
    - If `resource` is None, treat `package` as a filesystem path.
    - If both provided, use importlib.resources.
    """
    if resource is None and package:
        with open(package, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]
    if package and resource:
        with resources.files(package).joinpath(resource).open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]
    return []


def load_json(package: str | None, resource: str | None = None) -> dict:
    if resource is None and package:
        with open(package, "r", encoding="utf-8") as f:
            return json.load(f)
    if package and resource:
        with resources.files(package).joinpath(resource).open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}
