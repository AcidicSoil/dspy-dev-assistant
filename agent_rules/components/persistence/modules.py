from __future__ import annotations
import dspy
from .signatures import MemoryWriteSignature


class MemoryWriter(dspy.Module):
    """Abstract persistence layer; wrap with concrete backends elsewhere."""
    def __init__(self):
        super().__init__()
        self.write = dspy.Predict(MemoryWriteSignature)

    def forward(self, content: str, tags: str, ttl_days: int) -> dspy.Prediction:
        return self.write(content=content, tags=tags, ttl_days=ttl_days)
