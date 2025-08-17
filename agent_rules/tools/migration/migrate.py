"""CLI to migrate legacy markdown rules into DSPy RuleBundles + stubs."""
from __future__ import annotations
import argparse
from pathlib import Path
from load_legacy import load_rules
from emit_dspy import emit_rulebundle, emit_code_stubs
from validate import validate_bundle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to legacy-rules/ or doc file")
    parser.add_argument("--out", default="agent-rules", help="Output root")
    args = parser.parse_args()

    legacy = load_rules(Path(args.source))
    bundles = emit_rulebundle(legacy)

    for bundle_path, bundle in bundles.items():
        validate_bundle(bundle)
        bundle_path.parent.mkdir(parents=True, exist_ok=True)
        bundle_path.write_text(bundle)

    emit_code_stubs(bundles, Path(args.out))
    print(f"Migrated {len(bundles)} bundles → {args.out}")


if __name__ == "__main__":
    main()
