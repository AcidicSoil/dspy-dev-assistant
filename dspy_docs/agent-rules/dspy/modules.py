"""DSPy modules orchestrating LM strategies for each signature."""

import dspy
from .signatures import AnalyzeIssue, ImplementTask, RunChecks, CommitCode, UpdateDocs


class AnalyzerModule(dspy.Module):
    def __init__(self, lm=None):
        self.cot = dspy.ChainOfThought(AnalyzeIssue, lm=lm)

    def forward(self, issue: str):
        return self.cot(issue=issue)


class ImplementerModule(dspy.Module):
    def __init__(self, lm=None):
        self.cot = dspy.ChainOfThought(ImplementTask, lm=lm)

    def forward(self, spec):
        return self.cot(spec=spec)


class CheckModule(dspy.Module):
    def __init__(self, lm=None):
        self.literal = dspy.Literal(RunChecks, lm=lm)

    def forward(self, repo: str):
        return self.literal(repo=repo)


class CommitModule(dspy.Module):
    def __init__(self, lm=None):
        self.cot = dspy.ChainOfThought(CommitCode, lm=lm)

    def forward(self, diff: str):
        return self.cot(diff=diff)


class DocModule(dspy.Module):
    def __init__(self, lm=None):
        self.cot = dspy.ChainOfThought(UpdateDocs, lm=lm)

    def forward(self, patch):
        return self.cot(patch=patch)
