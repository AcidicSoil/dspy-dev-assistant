from __future__ import annotations
from pathlib import Path
from agent_rules.tools.migration.validate import validate_bundle

ROOT = Path("agent-rules")


def main() -> None:
    for y in ROOT.rglob("*.yaml"):
        try:
            validate_bundle(y.read_text(encoding="utf-8"))
        except Exception as exc:
            raise SystemExit(f"Lint failed for {y}: {exc}")
    print("Rule lint passed.")


if __name__ == "__main__":
    main()
