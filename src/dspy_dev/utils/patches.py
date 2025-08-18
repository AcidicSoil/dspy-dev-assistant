from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

@dataclass
class Patch:
    path: Path
    diff: str

@dataclass
class RefactorResult:
    patches: List[Patch] = field(default_factory=list)
    applied: bool = False

    def summary(self) -> str:
        n = len(self.patches)
        action = "applied" if self.applied else "proposed"
        return f"[Refactor] {n} patch(es) {action}."

def write_patch(patch: Patch, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (patch.path.name + ".patch")
    out_file.write_text(patch.diff, encoding="utf-8")

def apply_patch(patch: Patch) -> None:
    # Placeholder: in a real implementation, use 'patch' or parse unified diff.
    # Here we simply append a comment to indicate a change (safe no-op).
    if patch.path.exists():
        original = patch.path.read_text(encoding="utf-8")
        patched = original + "\n# [dspy-dev] patched (placeholder)\n"
        patch.path.write_text(patched, encoding="utf-8")
