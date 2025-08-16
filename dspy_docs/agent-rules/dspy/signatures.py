"""DSPy signatures for core agent capabilities."""

import dspy


class AnalyzeIssue(dspy.Signature):
    """Summarize a GitHub issue and propose an implementation plan."""
    issue = dspy.InputField(desc="raw issue description")
    spec = dspy.OutputField(desc="structured analysis with summary, approach, plan, tests")


class ImplementTask(dspy.Signature):
    """Generate code changes based on an analysis spec."""
    spec = dspy.InputField(desc="analysis specification")
    patch = dspy.OutputField(desc="proposed code patch and file list")


class RunChecks(dspy.Signature):
    """Execute tests or linters and summarize results."""
    repo = dspy.InputField(desc="path to repository")
    report = dspy.OutputField(desc="pass/fail outcome and logs")


class CommitCode(dspy.Signature):
    """Compose a conventional commit message for a diff."""
    diff = dspy.InputField(desc="git diff to commit")
    message = dspy.OutputField(desc="emoji-prefixed conventional commit message")


class UpdateDocs(dspy.Signature):
    """Produce documentation updates for the code patch."""
    patch = dspy.InputField(desc="implemented code patch")
    docs = dspy.OutputField(desc="documentation additions or changes")
