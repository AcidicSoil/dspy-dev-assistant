from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Optional
from dataclasses import dataclass
from ..config import Config
from ..utils.patches import Patch, RefactorResult, write_patch, apply_patch
from .modules import DetectSmellsModule, PlanFixModule, GeneratePatchModule
from .rules import run_rule_based_refactor

@dataclass
class RefactorOptions:
    rules: Optional[list[str]] = None
    apply: bool = False
    include_glob: Optional[str] = None
    exclude_glob: Optional[str] = None
    patch_out: Optional[Path] = None
    patch_format: str = "unified"

def iter_files(root: Path, include_glob: str | None, exclude_glob: str | None) -> Iterable[Path]:
    files = root.rglob("*.py") if root.is_dir() else [root]
    for f in files:
        name = str(f)
        if include_glob and not f.match(include_glob): 
            continue
        if exclude_glob and f.match(exclude_glob):
            continue
        yield f

def run_refactor(root: Path, rules: list[str] | None, apply: bool, include_glob: str | None, exclude_glob: str | None, patch_out: Path | None, patch_format: str, config: Config) -> RefactorResult:
    result = RefactorResult(applied=apply)
    detect = DetectSmellsModule()
    plan = PlanFixModule()
    gen = GeneratePatchModule()
    for path in iter_files(root, include_glob, exclude_glob):
        code = path.read_text(encoding="utf-8")
        # Prefer a fast, deterministic rule-based patch first (demo)
        local_diff = run_rule_based_refactor(path, code)
        if local_diff.strip():
            p = Patch(path=path, diff=local_diff)
            result.patches.append(p)
            if patch_out:
                write_patch(p, patch_out)
            if apply:
                apply_patch(p)
            continue
        smells = detect(code=code).smells_json
        plan_text = plan(code=code, smells_json=smells).plan
        diff = gen(code=code, plan=plan_text).patch or ""
        if not diff.strip():
            continue
        p = Patch(path=path, diff=diff)
        result.patches.append(p)
        if patch_out:
            write_patch(p, patch_out)
        if apply:
            apply_patch(p)
    return result
