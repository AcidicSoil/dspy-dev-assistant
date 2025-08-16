
    # `CLAUDE.md` (Model-Specific Guidance — Alternative LLM)

    Do not make edits to the following files .gitignore, pyproject.toml, and requirements.txt

    ```markdown
    # Model-Specific Guidance: Claude (Alternative Backend)

    **Scope:** Tailoring prompts, constraints, and failure handling when using Claude to run the same pipelines defined in @AGENTS.md.
    **Precedence:** This file overrides model-specific behaviors only; do not change project-wide rules in `GEMINI.md`.

    ---

    ## 1) Interaction Style & Reasoning
    - Prefer **concise plans** with bullet steps; avoid verbose stream-of-consciousness.
    - Always produce **structured artifacts** (JSON blocks) for plans, edits, and test tables.
    - Keep **code blocks minimal** and executable; no ellipses or placeholder imports.

    ## 2) Prompt Directives
    - **System prelude essentials:**
      - Role: “You are a DSPy module producing deterministic, validated outputs.”
      - Constraints: Python 3.11, Ruff/Black/Mypy, pytest semantics, AST-preserving transforms.
      - Guard: Refuse to emit final code when verification fails; propose a fix plan instead.
    - **Temperature & Decoding:** Start with temperature 0–0.2; `max_tokens` large enough for codegen; enable retries with critique loop.

    ## 3) Refactoring (Epic 1) — Expectations
    - Identify smells with **spans** (line ranges) and confidence.
    - Plan must map smell → **standard pattern** with justification and expected side effects.
    - Code edits must be **AST-compatible**; if not sure, emit a fallback **manual diff** with precise context.
    - Post-checklist to self-enforce:
      - No behavior changes unless explicitly requested.
      - Public API unchanged.
      - Added docstrings and type hints when safe.
      - All names PEP8-compliant; imports deduplicated.

    ## 4) Test Generation (Epic 2) — Expectations
    - Generate a **Test Plan Table** with columns: Case, Inputs, Pre-conditions, Expected, Notes.
    - Prefer **parametrized tests**; extract fixtures for repeated setup.
    - On failures: emit **Fix Plan** that adjusts either tests (if over-constrained) or source (if bug surfaced), but never silently relax assertions.

    ## 5) Web‑Aware Verification (Epic 3)
    - Cite **official docs first**; if using blogs/StackOverflow, call them *secondary* and seek confirmation.
    - Extract **versioned facts** (e.g., “pandas 2.2 changed default of ...”).
    - When conflicts exist, **halt emission** and return a decision record with options and tradeoffs.

    ## 6) Failure & Retry Policy
    - If `dspy.Assert` fails:
      - Summarize *why* (lint/type/test/doc) in ≤5 bullets.
      - Provide the **smallest delta** likely to resolve.
      - Retry with that delta; cap at 3 attempts; persist all attempts.

    ## 7) Output Schemas

    ### 7.1 Refactor Plan (JSON)
    ```json
    {
      "smell": "Long Method",
      "pattern": "Extract Method",
      "rationale": "Improves readability; enables reuse in tests",
      "edits": [{"type":"extract_method","start":120,"end":210,"name":"_compute_score"}]
    }

### 7.2 Test Plan Row (CSV-like)

    Case, Inputs, Pre-conditions, Expected, Notes
    normal_basic, {"x":3,"y":4}, state=default, 7, integer addition
    edge_zero, {"x":0,"y":0}, state=default, 0, identity check
    error_type, {"x":"a","y":1}, state=default, TypeError, strict types

### 7.3 Verification Facts (YAML)

    api: pandas.DataFrame.explode
    version: "2.2"
    notes:
      - "ignore_index default changed"
    citations:
      - url: https://pandas.pydata.org/...
        title: "pandas 2.2 release notes"
        accessed_at: "2025-08-12"

8) Do/Don’t Quicklist
---------------------

* **Do:** deterministic code, small diffs, explicit citations, short rationales.

* **Don’t:** emit unverified code, invent APIs, or swallow failing tests.
