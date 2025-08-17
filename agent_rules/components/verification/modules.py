from __future__ import annotations
import dspy
from .signatures import CritiqueSignature


class SelfCritic(dspy.Module):
    """Lightweight verifier that emits a verdict and optional correction."""
    def __init__(self):
        super().__init__()
        self.judge = dspy.Predict(CritiqueSignature)

    def forward(self, candidate: str, constraints: str) -> dspy.Prediction:
        return self.judge(candidate=candidate, constraints=constraints)
