from __future__ import annotations
import dspy
from .signatures import ExecuteToolSignature


class ToolDecider(dspy.Module):
    """Routes a query to the best tool; output is serialized JSON for downstream executors."""
    def __init__(self):
        super().__init__()
        self.decide = dspy.Predict(ExecuteToolSignature)

    def forward(self, query: str, tools_catalog: str) -> dspy.Prediction:
        return self.decide(query=query, tools_catalog=tools_catalog)
