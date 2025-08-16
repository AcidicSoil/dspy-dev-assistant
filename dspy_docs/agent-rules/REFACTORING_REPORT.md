# Refactoring Report

## Major Changes
- Renamed `dspy/RULEBOOK.md` to `dspy/DSPY_RULES.md` and clarified rule precedence.
- Added `AnalyzeCode` signature and `ReviewModule` for comprehensive code analysis.
- Expanded `architecture.md` and `modules.py` to include the new module and updated pipeline ordering.
- Introduced `TRACEABILITY.md` mapping legacy `.mdc` rules to DSPy signatures and modules.

## Conflict Resolution
- Unified multiple commit conventions into a single conventional commit policy.
- Consolidated scattered documentation rules under `UpdateDocs` and `DocModule`.

## Deprecated Practices
- Legacy `.mdc` rule files are preserved in `legacy-rules/` but superseded by DSPy modules.

## New Rules
- Code analysis now requires explicit quality, performance, and security review before merge.
- Rule hierarchy enforced: global → project → sub-directory.
