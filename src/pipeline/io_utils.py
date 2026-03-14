from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    """Create the directory (and any missing parents) if it does not exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    """Write a dict as UTF-8 JSON to the given path, creating parent dirs if needed."""
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

