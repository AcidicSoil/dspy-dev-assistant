
`AGENTS.md` (Agent Orchestration & Tools)
-----------------------------------------

    # Agents, Pipelines, and Tools

    Do not make edits to the following files .gitignore, pyproject.toml, and requirements.txt

    **Scope:** How we compose DSPy modules, tools, and checks to fulfill Epics 1–3.

    ---

    ## 1) DSPy Conventions
    - **Signatures:** Explicit inputs/outputs; include constraints (e.g., “return valid Python 3.11”).
    - **Guards:** `dspy.Assert` after each critical step (analysis present, compile OK, tests pass).
    - **Retries:** Bounded (≤3) with stateful hints (why previous attempt failed).
    - **Artifacts:** Every step yields a structured artifact (JSON) saved under `.runs/`.

    ## 2) Core Tools (abstractions)
    - **FilesystemTool**
      - `read_file(path) -> str`
      - `write_file(path, content, mode="x")` (refuse overwrite unless `--force`)
      - `list_symbols(path) -> [Function|Class]`
    - **PythonCheckTool**
      - `lint(path|code)`
      - `typecheck(paths...)`
      - `exec_snippet(code, timeout)`
    - **PytestRunner**
      - `run(paths..., markers=None) -> {passed, failed, report}`
      - `parse_failures(report) -> [Failure]`
    - **WebSearchTool**
      - `search(query, k=5)`
      - `fetch(url) -> text/html`
      - `extract_api_facts(html|url) -> {version, examples, notes, citations}`
    - **ASTTransformTool**
      - high-level transforms built on **libcst** (preferred) or **redbaron**

    ## 3) Pipelines by Epic

    ### Epic 1 — Automated Code Refactoring
    **Modules:**
    - `RefactorSmellDetector`: inputs (code|path), outputs list of smells ranked with spans.
    - `RefactorPlanner`: map smell → standard pattern (Extract Method, Inline Temp, Guard Clauses, Decompose Conditional, Replace Magic Number).
    - `RefactorApplier`: produce transformed code via AST, plus human-readable diff.
    - `RefactorValidator`: run `ruff --fix`, `mypy`, quick import/exec, optional smoke tests.

    **Contract (pseudo):**
    ```python
    @dataclass
    class RefactorPlan:
        smell: str; pattern: str; rationale: str; edits: list[Edit]

    plan = RefactorPlanner(code, smells).run()
    dspy.Assert(len(plan.edits) > 0, "Planner produced no edits")

    new_code = RefactorApplier(code, plan).apply()
    dspy.Assert(is_valid_python(new_code), "Invalid syntax after refactor")

    validate(new_code)  # ruff + mypy + exec

### Epic 2 — Agentic Unit Test Generation

**Modules:**

* `TestReader`: load module, parse signatures/branches (AST & static inspect).

* `TestPlanGenerator`: table covering **normal / edge / error**; includes fixtures/mocks.

* `PytestEmitter`: generates parametrized tests, clear names, asserts with messages.

* `TestFileWriter`: writes `tests/test_<module>__<func>.py` (idempotent by marker).

* `TestExecutor`: runs pytest, captures & interprets failures, proposes fixes.

**Contract:**

    plan = TestPlanGenerator(symbol).run()
    dspy.Assert(plan.coverage_targets.met_minimum(), "Insufficient plan coverage")

    path = TestFileWriter(plan).write()
    results = TestExecutor(path).run()
    dspy.Assert(results.failed == 0, f"Tests failing: {results.failed}")

### Epic 3 — Web‑Aware Code Verification

**Modules:**

* `DocSearch`: prioritize official docs; fall back to reputable sources.

* `DocSynthesizer`: extract API version, required args, changed defaults, deprecations.

* `VerifiedCodegen`: conditions code emission on doc facts; embeds **citations**.

* `VerificationReport`: structured proof with links & timestamp.

**Contract:**

    hits = DocSearch(query, prefer_official=True).topk(5)
    facts = DocSynthesizer(hits).extract()
    dspy.Assert(facts.has_sources(), "No credible docs found")

    code = VerifiedCodegen(task, facts).emit()
    dspy.Assert(passes_static_checks(code), "Code fails static checks")

4) CLI Contracts (Typer/Click)
------------------------------

* `devassist refactor <path[:symbol]> [--force] [--json]`

* `devassist testsynth <path[:symbol]> [--json] [--rerun-on-fail]`

* `devassist verify --topic "library feature" [--emit-code] [--json]`

Each command:

* Prints human summary + `--json` machine output.

* Writes artifacts to `.runs/<ts>/<command>/`.

5) Prompt/Context Assembly Rules

--------------------------------

* **System prelude:** purpose, safety, deterministic style, refusal policy for unverified code.

* **Context blocks:** (a) task description, (b) code excerpt (≤200 lines window), (c) constraints (style, version), (d) test or doc facts, (e) example I/O.

* **Critic pass:** a second agent critiques output; only then emit.

* **Redactions:** strip secrets, tokens, emails, internal URLs from context.

6) Quality Gates & Metrics

--------------------------

* Must emit **diff + rationale** on refactors.

* Test runs must show **coverage delta** when feasible.

* Store **citations** for any web-backed suggestion (URL, title, accessed\_at).

* Telemetry: success rate, time-to-result, retries, flake rate.

7) Extension Points

-------------------

* Optimizers: MIPROv2/BootstrapFinetune behind flags.

* IDE: VS Code extension consumes CLI JSON.

* Multi-language: introduce language adapters under `/src/lang/*`.

    ---
