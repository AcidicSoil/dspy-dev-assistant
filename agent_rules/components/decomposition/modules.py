from __future__ import annotations
import dspy
from .signatures import DecomposeSignature


class Decomposer(dspy.Module):
    """Single-step decomposer."""
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(DecomposeSignature)

    def forward(self, objective: str) -> dspy.Prediction:
        return self.predict(objective=objective)
