# GEMINI.md

## 1) Title & scope

Operational profile for **Gemini-based CLIs/agents** running in the `dspy-dev-assistant` repository. This file documents the confirmed environment, commands, and guardrails required for vendor tools to execute the project’s workflows (refactor, agentic test generation, web-aware verification). It includes **only** features present in local configs and docs. ([GitHub][1])

---

## 2) Project overview & entry points

This project is a **DSPy-powered developer assistant** that exposes a command-line interface **`dspy-dev`** for three flows:

* **Refactor:** detect smells, generate/apply patches.
* **TestGen:** plan/write/review tests toward a coverage target.
* **Verify:** fetch official docs and check code for mismatches; emit a report.

The README shows Python **3.11+** and **Astral `uv`** for environments, with usage like `uv run dspy-dev ...`. Treat `dspy-dev` as the single entry point. ([GitHub][1])

---

## 3) Repository layout map

Root (selected):

```
.
├─ dspy-dev-assistant/         # Package source (CLI + DSPy pipelines/modules)
├─ docs/                       # Project docs
├─ README.md                   # High-level usage & concepts
├─ pyproject.toml              # Project metadata / tool config
├─ requirements.txt            # Pinned deps (when not using uv.lock)
├─ uv.lock                     # uv lockfile
├─ .env.example                # Env var template (no secrets)
├─ .python-version             # Interpreter pin
├─ AGENTS.md / CLAUDE.md / GEMINI.md
└─ settings.json / mockup-scaffold.md
```

All items above are visible at the repository root. ([GitHub][1])

---

## 4) Setup & run commands

> Prefer `uv` to ensure the project virtualenv is used. Commands below are taken from the README. ([GitHub][1])

**Create environment**

```bash
# macOS/Linux/Windows (PowerShell has its own installer in README)
uv venv -p 3.12
# activate:
#   macOS/Linux: source .venv/bin/activate
#   Windows:     .venv\Scripts\activate
uv sync
```

**Run the three flows**

```bash
# 1) Refactor
uv run dspy-dev refactor src/ --dry-run
uv run dspy-dev refactor src/ --rules long-method,duplicate-code --apply

# 2) Agentic Test Generation
uv run dspy-dev testgen src/package --out tests

# 3) Web-Aware Verification
uv run dspy-dev verify src/ --providers openai,requests --report out/verify.md
```

Command shapes and flags are demonstrated in README usage examples. ([GitHub][1])

---

## 5) Test & quality commands

Run locally before PRs:

```bash
uv run pytest -q
uv run ruff check .
uv run mypy src
```

These appear in the project’s dev/PR checklist. ([GitHub][1])

---

## 6) Conventions & style

* **DSPy composition:** Signatures → Modules → Pipelines → Optimization; keep I/O contracts explicit. ([GitHub][1])
* **Safety-first execution:** default to `--dry-run`; apply patches only with `--apply`.
* **Idempotence:** prefer patch files and report artifacts over in-place edits. ([GitHub][1])
* **Commit hygiene:** small, focused changes; include commands used and artifacts (patches/tests/reports).
* **Type-first:** add type hints on public helpers; keep functions small and pure where possible.

---

## 7) Tooling & integrations

Confirmed in-repo:

* **Env & packaging:** Astral **`uv`** (venv + dependency sync). ([GitHub][1])
* **CLI:** **`dspy-dev`** exposes `refactor`, `testgen`, `verify`. ([GitHub][1])
* **Quality:** **pytest**, **ruff**, **mypy**. ([GitHub][1])
* **Verification providers (sample config):** `openai`, `requests`, `stripe` (via `[tool.dspy_dev]` example in README). ([GitHub][1])

> **Gemini-specific integration:** Not configured in this repository. External **gemini-cli** tools should invoke the project via the standard `uv run dspy-dev …` commands shown above and manage model selection outside this repo.

---

## 8) Security & safety guardrails

* **Secrets:** never commit secrets; use **`.env.example`** as a template and keep real values outside VCS. (The template exists at repo root.) ([GitHub][1])
* **Destructive operations:** the refactor flow **does not** modify files unless `--apply` is used; prefer `--dry-run` and patch review first. ([GitHub][1])
* **Verification:** read-only; produces reports and citations without mutating source. ([GitHub][1])
* **Review requirement:** all applied patches and generated tests must be human-reviewed before merge.

---

## 9) Task workflows

### A) Refactor

1. Scope a path or file.
2. Run dry analysis to produce diffs.
3. Apply selected rules with `--apply`.
4. Re-run tests/linters; open a PR with patches.

```bash
uv run dspy-dev refactor path/ --dry-run
uv run dspy-dev refactor path/ --rules long-method --apply
uv run pytest -q && uv run ruff check . && uv run mypy src
```

### B) Agentic Test Generation

1. Analyze a target module/package.
2. Plan cases (happy/edge/error).
3. Write tests to `--out`; iterate toward coverage target.
4. Commit tests with brief rationale.

```bash
uv run dspy-dev testgen src/package --out tests
```

### C) Web-Aware Verification

1. Choose providers (e.g., `openai,requests`).
2. Verify and write a report.
3. Fail CI or open an issue/PR on high-severity mismatches.

```bash
uv run dspy-dev verify src/ --providers openai,requests --report out/verify.md
```

(All flows and examples are taken from README usage.) ([GitHub][1])

---

## 10) Code navigation hints for agents

* **Start** at `dspy-dev-assistant/` for the package code (CLI glue, DSPy pipelines, modules).
* **Search** for DSPy **Signatures** (I/O contracts) and **Modules** (predictors) to map data flow.
* **Locate** pipeline composition to see how outputs feed subsequent steps.
* **Check** `pyproject.toml` for any `[tool.dspy_dev]` settings mirroring README samples (rules, targets, providers). ([GitHub][1])

---

## 11) Testing strategy & definition of done

* **Unit/behavior tests:** cover planners/generators/utilities, including edge/error paths.
* **Generated tests:** acceptable if they pass and increase meaningful coverage; must be readable and focused.
* **Static checks:** `pytest` passing; `ruff`/`mypy` clean locally and in CI (as shown in the README’s dev setup). ([GitHub][1])
* **Coverage target:** use the value configured in `pyproject.toml` if present; README shows an example `testgen.target_coverage = 0.85`. ([GitHub][1])
* **Docs:** update README/examples when adding flags or modules; include reproduction steps in PRs.

---

## 12) Appendix: environment matrix, supported versions, glossary

**Environment matrix (confirmed)**

* **Python:** 3.11+ (examples use 3.12 venv).
* **OS:** macOS / Linux / Windows (README shows platform-specific notes).
* **Package manager:** `uv` for env & dependency sync. ([GitHub][1])

**Supported versions**

* Pin via `.python-version` if present; otherwise follow the README guidance. ([GitHub][1])

**Glossary**

* **Signature:** declarative input→output contract for a step.
* **Module:** DSPy component parameterized by a Signature (e.g., predictor).
* **Pipeline:** composition passing outputs→inputs across steps.
* **Optimization:** evaluation-driven tuning of instructions/few-shots.
* **Verification provider:** docs domain inspected during `verify` (e.g., `openai`, `requests`, `stripe`). ([GitHub][1])

---

*This profile is intentionally vendor-light: Gemini-specific keys/adapters are not defined in-repo; external gemini-cli wrappers should call the documented `dspy-dev` commands and manage model/runtime on their side.* ([GitHub][1])

[1]: https://github.com/AcidicSoil/dspy-dev-assistant "GitHub - AcidicSoil/dspy-dev-assistant"
