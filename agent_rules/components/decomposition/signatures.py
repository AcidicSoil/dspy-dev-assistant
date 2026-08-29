from __future__ import annotations
import dspy


class DecomposeSignature(dspy.Signature):
    """Break a complex objective into smaller tasks."""
    objective: str = dspy.InputField(desc="High-level goal")
    steps: str = dspy.OutputField(desc="Bullet list of sub-tasks")
