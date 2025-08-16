
# `GEMINI.md` (Project Root Context)

    Do not make edits to the following files .gitignore, pyproject.toml, and requirements.txt

    # DSPy‑Powered Developer Assistant — Project Context (Root)

    **Scope:** Project-wide defaults and non-negotiables.
    **Precedence:** global > project root (this file) > sub-directory.
    **Imports:** @AGENTS.md

    ---

    ## 1) Project Title & Description
    **DSPy‑Powered Developer Assistant** — a suite of AI tools that automate Python refactoring, generate agentic unit tests, and verify code against the latest docs using web search. Targets **high reliability**, **maintainability**, and **CLI-first usability**.

    ## 2) General Instructions
    - **North Star:** Reduce developer toil, improve code quality and test coverage. Favor correctness and maintainability over cleverness.
    - **DSPy First:** Structure capabilities as DSPy modules with explicit Signatures, `dspy.Assert` checks, and retry/self-correction.
    - **CLI-first UX:** Every major function is invokable via clear CLI commands with helpful `--help`, exit codes, and machine-readable logs.
    - **Deterministic by Default:** Prefer reproducible runs (seeded sampling, stable prompts, pinned deps).
    - **Safety & Verification:** Never output refactors or tests without validation (lint → type → unit tests). Block promotion if checks fail.
    - **Modular Architecture:** Separate concerns: analysis, planning, codegen, execution, verification, reporting.

    ## 3) Coding Style & Conventions
    - **Language:** Python 3.11+.
    - **Formatting:** Black (line length 100), isort, Ruff for linting.
    - **Typing:** `from __future__ import annotations`; `mypy --strict` on core modules.
    - **Structure:**

/src
/core # shared utils: io, fs, logging, subprocess, web, dspy wrappers
/refactor # Epic 1 modules, plans, transforms, validators
/testsynth # Epic 2 planners, generators, runners, reporters
/verify # Epic 3 web tools, doc parsers, citation store
/cli # click/typer commands mapping to modules
/tests # pytest suites for our system

    - **Naming:** packages `lower_snake`, classes `PascalCase`, functions/vars `snake_case`.
    - **Errors:** Use domain errors (`RefactorError`, `TestSynthesisError`, `VerificationError`) with actionable messages.
    - **Logs:** Structured JSON logs at INFO; timestamps + task ids; DEBUG includes prompts (redact secrets).
    - **Config:** `pyproject.toml` for tools; `.env` for secrets; never commit secrets.

    ## 4) Component- / File-Specific Guidance
    - **Epic 1 (Refactoring):**
    - Identify smells (long method, dup code, deep nesting, magic numbers, mutable default args).
    - Plan → transform → validate (AST-preserving where possible). Run `ruff --fix`, `mypy`, and quick smoke tests.
    - Always produce a *diff view* and a *rationale* section.
    - **Epic 2 (Agentic Unit Tests):**
    - Read source, analyze signatures/branches, generate a test plan table (normal, edge, error cases).
    - Emit pytest with fixtures and parametrization; avoid brittle mocks unless necessary.
    - Auto-write to `tests/test_<module>__<func>.py`; run pytest; parse results; propose retries/fixes.
    - **Epic 3 (Web‑Aware Verification):**
    - Use web tool to fetch **official docs** first; capture citations with URL+title+access date.
    - Extract API versions and breaking changes; integrate into prompt context; refuse to emit code if conflicts unresolved.

    ## 5) Tooling & Workflow
    - **Make / Scripts (examples):**
    - `make setup` → create venv, install deps
    - `make check` → ruff + mypy + pytest -q
    - `make refactor FILE=src/foo.py:Class.func`
    - `make testsynth TARGET=src/foo.py:func`
    - `make verify TOPIC="pandas df explode"`
    - **CI gates:** run `make check`; block on any failure; upload artifacts (diffs, reports, coverage).
    - **Observability:** store run reports at `.runs/<timestamp>/<task>/`.

    ## 6) Dependency Management Policies
    - **Allowed core:** dspy, click/typer, pytest, requests/httpx, beautifulsoup4/selectolax, lxml, pydantic, ruff, mypy, black, isort, rich, uv/poetry/pip-tools (choose one).
    - **AST/Refactor:** libcst or redbaron (choose one and justify), rope optional.
    - **Web automation:** playwright optional for tricky docs; default to HTTP fetch + parse.
    - **Adding deps:** open PR with: rationale, size, security notes, maintenance risk, removal plan.

    ## 7) Performance & Reliability Targets
    - Single refactor suggestion < 5s (post-compile warm runs).
    - Core pipelines include `dspy.Assert` guards + bounded retries.
    - Success metrics tracked: task completion rate, pass rates, coverage delta, user NPS.

    ## 8) Testing Rules
    - Test public APIs; golden tests for planners; in-the-loop tests for agents (mock HTTP where possible).
    - Coverage goal: +30% vs baseline per PRD. Fail CI if coverage regresses on critical packages.
    - Property-based tests for refactor transforms that preserve behavior.

    ## 9) Imports
    @AGENTS.md
