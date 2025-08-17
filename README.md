# DSPy-Powered Developer Assistant

AI-driven utilities to **automate code refactoring**, **generate agentic unit tests**, and **verify code against the latest official docs** via web search—implemented as a composable **DSPy** program (Signatures → Modules → Pipelines → Optimization). This README gives you a quick mental model of the concepts involved and shows how to run the tool.

---

## Why DSPy here? (Concepts you need)

**Big picture:** DSPy lets you *program* LLM behavior with explicit I/O contracts and reusable components—rather than juggling brittle prompts. In FP terms, think **typed arrows** stitched into pipelines:

* **Signatures** — declarative **Inputs → Outputs** contracts (e.g., `source_code -> refactoring_patch`).
* **Modules** — reusable LLM components parameterized by a Signature (e.g., `Predict(Signature)`).
* **Pipelines/Composition** — chain modules so one output feeds the next (detector → planner → fixer → verifier).
* **Optimization** — evaluation-driven compilers that tune instructions/few-shots to improve metrics (patch quality, test coverage, factuality).

This project maps directly onto those ideas:

1. **Refactoring** = detectors + fix planners + patch generators.
2. **Agentic TestGen** = analyzer → test case planner → test writer → self-check.
3. **Web-Aware Verification** = search & retrieve docs → consistency checks → report.

> TL;DR: Treat each step as a small, typed function. Compose them. Let DSPy optimize the details.

---

## Features

### 1) Automated Code Refactoring

Detects and proposes safe refactorings for common smells, then emits a **unified diff patch** ready to apply:

* **Smells detected:** long/large methods, duplicate code, deep nesting, “magic numbers/strings,” mutable defaults, dead code, and parameter bloat.
* **Fix strategies:** function extraction, constant hoisting, loop/conditional flattening, DRY consolidation, safe default fixes, and rename/inline moves.
* **Guardrails:** AST-aware hints, unit-test awareness, patch simulation, and optional `--dry-run`.

### 2) Agentic Unit Test Generation

Analyzes functions/modules and generates tests that cover:

* **Happy paths** (typical inputs),
* **Edge cases** (empty/null, boundary values, large inputs),
* **Error paths** (exceptions, invalid types),
* with **assertions** derived from docstrings, type hints, and observed behavior. A self-check loop critiques and revises tests to raise coverage or clarity.

### 3) Web-Aware Verification

Ensures your code aligns with **current** official docs:

* Searches vendor docs/APIs (e.g., new params, deprecations, breaking changes).
* Extracts authoritative snippets and verifies your usage.
* Emits a **verification report** with sources and suggested fixes.

---

## Architecture (DSPy view)

```markdown
[ Source Code ] ──► [ SmellDetector ] ──► [ FixPlanner ] ──► [ PatchGenerator ]
                                   │                          │
                                   └─────────────► [ TestsReviewer ◄─ TestWriter ◄─ TestPlanner ◄─ CodeAnalyzer ]
                                                                 │
                                   [ WebSearch ] ─► [ DocRetriever ] ─► [ ConsistencyChecker ] ─► [ VerificationReport ]

Optimization loop: evaluate patches/tests/reports → tune module instructions/few-shots → iterate.
```

### Minimal DSPy sketch (illustrative)

```python
# Illustrative only: adapt names to your DSPy version.
import dspy
from dspy import Signature, InputField, OutputField, Predict

class SmellToPatch(Signature):
    """Turn a detected 'smell' and code into a unified diff patch."""
    code: str   = InputField(desc="Original source code")
    smell: str  = InputField(desc="e.g., 'long method', 'mutable default'")
    patch: str  = OutputField(desc="Unified diff to apply")

PatchGen = Predict(SmellToPatch)   # a Module parameterized by the Signature
patcher = PatchGen()
result = patcher(code=open("foo.py").read(), smell="long method")
print(result.patch)
```

You’ll see the pattern:

* **Signatures** make I/O explicit.
* **Modules** implement the step.
* **Pipelines** chain steps and pass outputs along.
* **Optimization** runs evaluation-driven tuning to improve real metrics (e.g., fewer failing tests, higher doc-compliance).

---

## Installation & Setup (Astral **UV**)

> Prereqs: Python **3.11+** and **uv** installed.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

Clone and create an isolated environment:

```bash
git clone https://github.com/your-org/dspy-dev-assistant.git
cd dspy-dev-assistant

uv venv -p 3.12
# Activate:
#   macOS/Linux: source .venv/bin/activate
#   Windows:     .venv\Scripts\activate

uv sync  # installs dependencies from pyproject.toml
```

> Prefer running commands via `uv run ...` so you always use the project’s environment.

---

## Usage

All commands are exposed via the `dspy-dev` CLI.

### 1) Refactor code

```bash
# Analyze and propose patches (no writes)
uv run dspy-dev refactor src/ --dry-run

# Apply patches with selected rules
uv run dspy-dev refactor src/ \
  --rules long-method,duplicate-code,magic-numbers,mutable-defaults \
  --apply

# Limit scope to a file or module
uv run dspy-dev refactor src/package/module.py --apply
```

**Flags (common):**

* `--rules` — comma-separated smell names (default: all).
* `--include/--exclude` — glob filters.
* `--patch-out` — write patches to a directory instead of applying.
* `--format unified|git` — patch format.

### 2) Generate agentic unit tests

```bash
# Generate tests for a package, output to tests/
uv run dspy-dev testgen src/package --out tests

# Focus on a single function or class
uv run dspy-dev testgen src/package/module.py::ClassName::method --out tests

# Raise coverage target and allow revisions
uv run dspy-dev testgen src/package --out tests \
  --target-coverage 0.9 --max-revisions 3
```

**What happens:** analyzer builds a behavior model → planner enumerates scenarios → writer emits tests → reviewer critiques and revises until targets (e.g., coverage) are met.

### 3) Web-aware verification

```bash
# Verify usage against latest docs; emits a report with sources
uv run dspy-dev verify src/ --providers openai,requests --report out/verify.md

# Guard a specific API surface
uv run dspy-dev verify src/package/payments.py --providers stripe --report out/stripe.md

# Fail CI if high-severity mismatches are found
uv run dspy-dev verify src/ --severity high --ci
```

**Under the hood:** runs a retrieval step (search queries per API symbol), fetches doc pages, extracts versioned statements, and checks your code for mismatch/deprecations/breaking changes. Produces a **traceable report** with citations.

---

## Configuration

Add a `pyproject.toml` section to customize rules, test style, and verification providers:

```toml
[tool.dspy_dev]
refactor.rules = ["long-method","duplicate-code","magic-numbers","mutable-defaults"]
testgen.target_coverage = 0.85
verify.providers = ["openai","requests","stripe"]
verify.cache_ttl_hours = 24
```

---

## Extending & Internals (for contributors)

* **Pipelines** are standard DSPy compositions. Each step has a Signature; outputs feed the next step’s inputs.
* **Optimization**: an evaluation harness scores (a) patch applicability & test pass rate, (b) test coverage/clarity, (c) doc-consistency. DSPy compilers tune module instructions/few-shots to improve these metrics.
* **Safety/Idempotence**: refactors are patch-first; `--apply` is explicit. Tests write to separate paths. Verification never mutates source.

---

## Contributing

We welcome issues and PRs! A good first contribution:

* Add a smell detector or a refactoring strategy (with tests).
* Extend TestGen heuristics for a framework (e.g., FastAPI, SQLAlchemy).
* Add a verification provider (docs domain parser + match rules).
* Improve the evaluation harness or metrics.

**Dev setup**

```bash
uv venv -p 3.12 && source .venv/bin/activate
uv sync --all-extras
uv run pytest -q
uv run ruff check .
uv run mypy src
```

**PR checklist**

* Tests pass locally (`pytest`).
* Lint/type checks clean (ruff/mypy).
* Add docs/examples for new flags or modules.
* Keep functions small; prefer pure helpers and explicit data shapes.

---

## Roadmap

* Rich SARIF/CodeLens outputs for editors.
* Inline quick-fix suggestions via LSP.
* More language backends (JS/TS, Go) behind a common interface.
* Deeper doc reasoning (version windows, policy/contract checks).
* CI recipes (GitHub Actions) with cache-aware verification.

---

## Limitations & Ethics

* LLMs can be wrong. Always review patches and tests before merging.
* Web verification depends on retrieval quality and source authority; we prefer official docs and record sources in reports.
* Keep secrets out of prompts and logs. See `docs/SECURITY.md` for guidance.

---

## License

**MIT** (placeholder). See `LICENSE` for details.

---

## See also

* DSPy concepts overview (Signatures → Modules → Pipelines → Optimization).
* Example pipelines and optimization recipes in `examples/`.
* CONTRIBUTING.md for development guidelines.
