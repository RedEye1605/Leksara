from __future__ import annotations

from importlib.resources import files


def load_text(package: str, resource: str) -> str:
    return files(package).joinpath(resource).read_text(encoding="utf-8")


def load_json(package: str, resource: str):
    import json
    return json.loads(load_text(package, resource))
