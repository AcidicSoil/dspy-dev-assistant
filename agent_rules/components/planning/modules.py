from __future__ import annotations
import dspy
from .signatures import PlanSignature


class Planner(dspy.Module):
    """Composable planning module using a single prediction step."""
    def __init__(self, **kwargs):
        super().__init__()
        self.predict = dspy.Predict(PlanSignature)

    def forward(self, objective: str, context: str, constraints: str) -> dspy.Prediction:
        # Non-obvious logic: prepend guardrails from constraints into prompt.
        return self.predict(objective=objective, context=context, constraints=constraints)
