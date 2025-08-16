# Integration Guidelines

DSPy modules (`AnalyzerModule`, `ImplementerModule`, `ReviewModule`, `CheckModule`, `DocModule`, `CommitModule`) are backend‑agnostic. To use different LMs:

- **Claude** – instantiate modules with `dspy.Anthropic()`.
- **Gemini** – instantiate modules with `dspy.OpenAI(model="gemini-pro")`.
- **Other Agents** – provide any `dspy.LM` compatible object.

Modules expose consistent input/output fields, enabling portability across environments.
