from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import tomllib
from pathlib import Path

@dataclass
class RefactorConfig:
    rules: List[str] = field(default_factory=lambda: ["long-method","duplicate-code","magic-numbers","mutable-defaults"])

@dataclass
class TestGenConfig:
    target_coverage: float = 0.85

@dataclass
class VerifyConfig:
    providers: List[str] = field(default_factory=list)
    cache_ttl_hours: int = 24

@dataclass
class Config:
    refactor: RefactorConfig = RefactorConfig()
    testgen: TestGenConfig = TestGenConfig()
    verify: VerifyConfig = VerifyConfig()

def load_config(pyproject_path: Path | None = None) -> Config:
    pyproject_path = pyproject_path or Path("pyproject.toml")
    cfg = Config()
    if pyproject_path.exists():
        try:
            data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        section = data.get("tool", {}).get("dspy_dev", {})
        rf = section.get("refactor", {})
        tg = section.get("testgen", {})
        vr = section.get("verify", {})
        if "rules" in rf: cfg.refactor.rules = list(rf["rules"])
        if "target_coverage" in tg: cfg.testgen.target_coverage = float(tg["target_coverage"])
        if "providers" in vr: cfg.verify.providers = list(vr["providers"])
        if "cache_ttl_hours" in vr: cfg.verify.cache_ttl_hours = int(vr["cache_ttl_hours"])
    return cfg
