"""Very small loader: extracts headings, code blocks, and bullet points from Markdown."""
from __future__ import annotations
from pathlib import Path


def load_rules(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"Path not found: {path}")
    data = {}
    if path.is_dir():
        for p in path.rglob("*.md"):
            data[p.stem] = p.read_text(encoding="utf-8")
    else:
        data[path.stem] = path.read_text(encoding="utf-8")
    return data
