"""Minimal schema checks for RuleBundle files."""
from __future__ import annotations
import yaml

REQUIRED_TOP = {"apiVersion", "kind", "meta", "rules"}
REQUIRED_RULE = {"id", "signature", "module"}


def validate_bundle(text: str) -> None:
    data = yaml.safe_load(text)
    missing = REQUIRED_TOP - set(data)
    if missing:
        raise ValueError(f"Missing top-level keys: {sorted(missing)}")
    for r in data["rules"]:
        rm = REQUIRED_RULE - set(r)
        if rm:
            raise ValueError(f"Rule missing keys: {sorted(rm)}")
