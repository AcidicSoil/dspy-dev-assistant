# DSPy Rulebook

This rulebook consolidates the essential practices from the legacy agent guidelines and expresses them in DSPy-friendly terms.

## Precedence Hierarchy
- **Global** – organization-wide defaults from repository root.
- **Project** – rules in this `agent-rules/dspy` directory.
- **Sub-directory** – component specific guidance stored next to code.

## Core Development Practices
- **Issue Analysis** – produce structured specs with summary, problem statement, technical approach, implementation and test plans.
- **Task Implementation** – evaluate strategies, consider trade‑offs, and outline clear implementation steps.
- **Commit Quality** – use conventional commits with emojis and run checks by default. Keep commits atomic and descriptive.
- **Documentation** – update or create docs alongside code changes. Follow standardized templates and avoid duplication.
- **Code Analysis** – leverage knowledge graphs, quality evaluation, performance and security review before finalizing changes.
- **Continuous Improvement** – evolve rules through pattern recognition, error analysis, and feedback loops.

## Conflict Resolution
When overlapping guidance existed (e.g., multiple commit conventions), the more specific project rule took precedence. The DSPy version merges them into a single conventional commit policy.

## Directory Structure
- `dspy/` – active DSPy‑aligned rules and modules
- `legacy-rules/` – original unrefactored rule sets

See `TRACEABILITY.md` for mappings from legacy rules to their DSPy equivalents.

Refer to `architecture.md` for module boundaries and `signatures.py` for formal DSPy signatures.
