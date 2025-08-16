# DSPy Architecture

## Signatures
- `AnalyzeIssue(issue: str) -> AnalysisSpec`
- `ImplementTask(spec: AnalysisSpec) -> CodePatch`
- `AnalyzeCode(patch: CodePatch) -> CodeReview`
- `RunChecks(repo: str) -> CheckReport`
- `UpdateDocs(change: CodePatch) -> DocUpdate`
- `CommitCode(diff: str) -> CommitMessage`

## Modules
- `AnalyzerModule` – `ChainOfThought` reasoning over `AnalyzeIssue`
- `ImplementerModule` – stepwise planner for `ImplementTask`
- `ReviewModule` – evaluates patches via `AnalyzeCode`
- `CheckModule` – executes test or lint commands and summarizes results
- `DocModule` – ensures `UpdateDocs` follows templates
- `CommitModule` – wraps `CommitCode` with pre‑commit enforcement

## Composition
`AnalyzerModule` → `ImplementerModule` → `ReviewModule` → `CheckModule` → `DocModule` → `CommitModule`

Each module accepts the previous output, enabling composable workflows.

## External Integration
Modules can be backed by Claude, Gemini, or other LMs by swapping the underlying `dspy.Module` implementation. Inputs/outputs remain consistent, supporting cross‑agent compatibility.
