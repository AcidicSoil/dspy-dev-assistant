# DSPy Architecture

## Signatures
- `AnalyzeIssue(issue: str) -> AnalysisSpec`
- `ImplementTask(spec: AnalysisSpec) -> CodePatch`
- `CommitCode(diff: str) -> CommitMessage`
- `UpdateDocs(change: CodePatch) -> DocUpdate`
- `RunChecks(repo: str) -> CheckReport`

## Modules
- `AnalyzerModule` – `ChainOfThought` reasoning over `AnalyzeIssue`
- `ImplementerModule` – stepwise planner for `ImplementTask`
- `CommitModule` – wraps `CommitCode` with pre‑commit enforcement
- `DocModule` – ensures `UpdateDocs` follows templates
- `CheckModule` – executes test or lint commands and summarizes results

## Composition
`AnalyzerModule` → `ImplementerModule` → `CheckModule` → `CommitModule` → `DocModule`

Each module accepts the previous output, enabling composable workflows.

## External Integration
Modules can be backed by Claude, Gemini, or other LMs by swapping the underlying `dspy.Module` implementation. Inputs/outputs remain consistent, supporting cross‑agent compatibility.
