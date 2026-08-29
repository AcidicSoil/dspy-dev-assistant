"""Emit YAML RuleBundles and Python stubs based on parsed legacy content."""
from __future__ import annotations
from pathlib import Path
from textwrap import dedent

CATEGORY_HINTS = {
    "safety": ("verification", "SelfCritic"),
    "plan": ("planning", "Planner"),
    "tool": ("execution", "ToolDecider"),
}


def emit_rulebundle(legacy: dict) -> dict:
    bundles = {}
    for name, raw in legacy.items():
        cat, impl = CATEGORY_HINTS.get(_infer_category(raw), ("planning", "Planner"))
        yaml = dedent(f"""
        apiVersion: dspy.rules/v1
        kind: RuleBundle
        meta:
          name: {name}
          description: Migrated from legacy document.
          owner: tbd@company
          version: 1.0.0
          precedence: 60
        imports: []
        rules:
          - id: {name}-auto
            description: Auto-migrated rule from legacy text.
            appliesTo: ["*"]
            signature:
              name: {_sig_for(cat)}
              inputs:
                - name: input
                  type: str
                  desc: Auto-extracted input
              outputs:
                - name: output
                  type: str
                  desc: Auto-extracted output
            module:
              type: {cat}
              impl: {impl}
              config: {{}}
            constraints: []
            tests: []
        """)
        bundles[Path(f"agent-rules/components/{cat}/{name}.yaml")] = yaml
    return bundles


def emit_code_stubs(bundles: dict, out_root: Path) -> None:
    # Ensure the directory structure exists; skip if already present.
    for path in bundles.keys():
        (out_root / path.parent / "signatures.py").parent.mkdir(parents=True, exist_ok=True)


def _infer_category(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["safe", "guard", "ban", "block"]):
        return "safety"
    if any(k in t for k in ["tool", "api", "call"]):
        return "tool"
    return "plan"


def _sig_for(cat: str) -> str:
    return {
        "verification": "CritiqueSignature",
        "planning": "PlanSignature",
        "execution": "ExecuteToolSignature",
    }.get(cat, "PlanSignature")
