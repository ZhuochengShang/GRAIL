from __future__ import annotations

import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def to_uri(path_str: str) -> str:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", path_str or ""):
        return path_str
    return Path(path_str).expanduser().resolve().as_uri()
