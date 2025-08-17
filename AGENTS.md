# AGENTS.md — dspy-dev-assistant (for **codex**)

> **Scope**: Operating instructions for autonomous agents (codex) working in this repository. Place this file at the repo **root**. If a subfolder (e.g., `dspy-dev-assistant/`) also contains an `AGENTS.md`, that file **overrides** root guidance for work inside that subfolder. Deeper files win on conflicts; agents must merge settings top-down.

---

## 1) Project overview & entry points

* **What this is**: A DSPy-powered developer assistant that automates code **refactoring**, **agentic unit test generation**, and **web-aware verification** of code against the latest official docs via search & retrieval—implemented as composable DSPy pipelines. ([GitHub][1])
* **Primary entry point (CLI)**: `dspy-dev` with subcommands `refactor`, `testgen`, and `verify`. ([GitHub][1])
* **Why DSPy**: Program LLM behavior using **Signatures → Modules → Pipelines → Optimization**, instead of ad-hoc prompts. ([GitHub][1])

---

## 2) Repository layout map

* **Root files/dirs (observed)**:

  * `dspy-dev-assistant/` — project’s main package (module code lives here).
  * `docs/` — documentation (e.g., security notes).
  * `.env.example`, `.python-version`, `.editorconfig`, `.gitignore` — env & editor settings.
  * `pyproject.toml`, `uv.lock`, `requirements.txt` — packaging & deps (UV-managed).
  * `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, `mockup-scaffold.md`, `settings.json`. ([GitHub][1])
* **Where to look first (coding)**: `dspy-dev-assistant/` for CLI wiring and DSPy pipelines; `docs/` for security/policies (see `docs/SECURITY.md`). ([GitHub][1])

---

## 3) Setup & run commands (install, build, start, env)

* **Prereqs**: Python **3.11+** and **UV** (Astral). ([GitHub][1])
* **Create env & install**:

  ```bash
  uv venv -p 3.12
  # activate: .venv/bin/activate  (Windows: .venv\Scripts\activate)
  uv sync
  ```

  Always run tools via `uv run …` to ensure the project venv is used. ([GitHub][1])
* **Environment variables**: Copy `.env.example` → `.env` and fill required keys/secrets (see Security). ([GitHub][1])
* **CLI (usage)**:

  * Refactor (dry-run default):
    `uv run dspy-dev refactor <path> --dry-run`
    Apply patches: `… --apply`
  * Generate tests:
    `uv run dspy-dev testgen <path> --out tests`
  * Web-aware verification:
    `uv run dspy-dev verify <path> --providers openai,requests --report out/report.md` ([GitHub][1])

---

## 4) Test & quality commands

* **Unit tests**: `uv run pytest -q`
* **Lint**: `uv run ruff check .`
* **Type-check**: `uv run mypy src` *(path may differ if sources live under `dspy-dev-assistant/`; prefer package root over `src`)*. ([GitHub][1])
* **CI gate (suggested)**: Run tests, ruff, mypy; fail on any high-severity verification mismatches (`verify --severity high --ci`). ([GitHub][1])

---

## 5) Conventions & style

* **Design**: Small, composable DSPy **Modules** with explicit **Signatures**; wire them into **Pipelines**; use **Optimization** only via the project’s evaluation harness. ([GitHub][1])
* **Patches**: Unified diffs; prefer **dry-run** and write patches to disk unless `--apply` is explicitly passed. ([GitHub][1])
* **Tests**: Table-driven where possible; include happy-path, edge-case, error-path scenarios (mirrors TestGen behavior). ([GitHub][1])
* **Commits/PRs**: Keep changes atomic; update docs when adding flags or modules; ensure evaluation notes accompany optimization changes. ([GitHub][1])

---

## 6) Tooling & integrations (frameworks, CLIs, agents/tools)

* **Language/stack**: Python (DSPy). **Package manager**: UV (`uv.lock`). **CLI**: `dspy-dev`. ([GitHub][1])
* **Verification providers** (examples): `openai`, `requests`, `stripe` (configurable via `pyproject.toml` under `[tool.dspy_dev]`). ([GitHub][1])
* **Allow/Deny & defaults**:

  * Refactor is **non-destructive** by default; `--apply` required to mutate.
  * Tests are emitted to user-selected paths (e.g., `--out tests`).
  * Verification reads code + web docs; it **never mutates** source. ([GitHub][1])

---

## 7) Security & safety guardrails

* **Secrets**: Never commit `.env`. Do not echo secrets in logs or prompts. Load from environment or local `.env`. (See `docs/SECURITY.md`.) ([GitHub][1])
* **Destructive ops**: Only allowed behind explicit flags (e.g., `--apply`). Always support `--dry-run`/patch-out. ([GitHub][1])
* **Web verification**: Prefer official documentation sources; record citations in the verification report. Review outputs before merge. ([GitHub][1])

---

## 8) Task workflows

### A) Add a new **smell detector** or **refactoring strategy**

1. Create module in `dspy-dev-assistant/` implementing a new Signature → Module.
2. Add to the refactor pipeline registry.
3. Add unit tests; run `pytest`, `ruff`, `mypy`.
4. Document new flags/behavior in README; include before/after examples. ([GitHub][1])

### B) Extend **TestGen** for a framework (e.g., FastAPI)

1. Add analyzer hooks (type hints/docstrings parsing).
2. Update planner to enumerate scenarios; ensure reviewer loop can iterate to target coverage.
3. Tests + README examples. ([GitHub][1])

### C) Add a **verification provider**

1. Implement provider (domain parser + match rules).
2. Wire into provider list; expose via `--providers`.
3. Validate on a target file/module; commit sample report under `out/`. ([GitHub][1])

### *(Migrations: Not configured in this repo.)*

---

## 9) Code navigation hints for agents

* **High-level flow** (read top-down):
  `SmellDetector → FixPlanner → PatchGenerator → (TestsReviewer ◄─ TestWriter ◄─ TestPlanner ◄─ CodeAnalyzer) → ConsistencyChecker → VerificationReport`
  The optimization loop evaluates patches/tests/reports, tunes instructions/few-shots, and repeats. Start by locating these components and their Signatures. ([GitHub][1])
* **Good starting files**: CLI entry/wiring (command parser), pipeline assembly, provider registry, and any evaluation harness modules. Use README architecture notes as the map. ([GitHub][1])

---

## 10) Testing strategy & “definition of done”

* **Required**:

  * `uv run pytest -q` passes locally.
  * `uv run ruff check .` clean.
  * `uv run mypy …` **no new** type errors.
  * If feature touches verification: provide a sample **report with citations**.
  * If feature adds flags: **README** updated with examples. ([GitHub][1])
* **Targets (suggested)**: Aim for coverage consistent with project config (e.g., `testgen.target_coverage` if set in `pyproject.toml`). ([GitHub][1])

---

## 11) Appendix: environment matrix, supported versions, glossary

* **Env matrix**

  * Python: see `.python-version`; README examples use **3.12** with **UV**. ([GitHub][1])
  * OS: Linux/macOS/Windows supported via UV venvs. ([GitHub][1])
* **Glossary (DSPy)**

  * **Signature**: Typed I/O contract.
  * **Module**: Reusable LLM component parameterized by a Signature.
  * **Pipeline**: Composition of modules (explicit data flow).
  * **Optimization**: Evaluation-driven routines that refine instructions/few-shots to improve real metrics. ([GitHub][1])

---

## 12) Notes for autonomous discovery/merge (AGENTS.md behavior)

* **Discovery order**: Agent looks for `AGENTS.md` in the **current working dir**; if absent, ascend toward repo root and **merge** with any found file(s). Deeper file wins on conflicts.
* **Subrepo note**: When operating specifically in `dspy-dev-assistant/`, prefer a local `AGENTS.md` there if present; otherwise use **this** root file.
* **Execution safety**:

  * Default to **simulation** modes (`--dry-run`, patch outputs) unless a task explicitly requires mutations.
  * For write operations, create a **feature branch**, open a **PR**, and include verification artifacts. ([GitHub][1])

> **Tip**: The README contains a compact mental model, concrete CLI examples, and contributor checklists—use it as your north star while navigating this codebase. ([GitHub][1])

---

*File location*: place at repository root (`/AGENTS.md`). If you maintain a specialized `AGENTS.md` under `dspy-dev-assistant/`, keep sections and order identical, overriding only what differs locally.

[1]: https://github.com/AcidicSoil/dspy-dev-assistant "GitHub - AcidicSoil/dspy-dev-assistant"
