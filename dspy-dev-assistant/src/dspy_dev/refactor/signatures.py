from __future__ import annotations
import dspy

class DetectSmells(dspy.Signature):
    """Analyze code and list code smells with spans/notes."""
    code: str = dspy.InputField(desc="Source code")
    smells_json: str = dspy.OutputField(desc="JSON list of {type, location, note}")

class PlanFix(dspy.Signature):
    """Given smells and code, draft a refactoring plan."""
    code: str = dspy.InputField()
    smells_json: str = dspy.InputField()
    plan: str = dspy.OutputField(desc="Step-by-step refactoring plan")

class GeneratePatch(dspy.Signature):
    """Emit a unified diff patch implementing the plan."""
    code: str = dspy.InputField()
    plan: str = dspy.InputField()
    patch: str = dspy.OutputField()
