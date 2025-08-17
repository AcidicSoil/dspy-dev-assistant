from __future__ import annotations
import dspy


class CritiqueSignature(dspy.Signature):
    """Self-critique a candidate output against constraints, returning a corrected version if needed."""
    candidate: str = dspy.InputField()
    constraints: str = dspy.InputField()
    verdict: str = dspy.OutputField(desc="OK/REVISE + rationale")
    corrected: str = dspy.OutputField(desc="Revised candidate if issues found")
