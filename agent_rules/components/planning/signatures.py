from __future__ import annotations
import dspy


class PlanSignature(dspy.Signature):
    """Produce a step-by-step plan to achieve an objective given context and constraints."""
    objective: str = dspy.InputField(desc="High-level goal")
    context: str = dspy.InputField(desc="Relevant facts, tools, and state")
    constraints: str = dspy.InputField(desc="Hard limits and policies")
    plan: str = dspy.OutputField(desc="Ordered, numbered plan")
