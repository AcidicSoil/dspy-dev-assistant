from __future__ import annotations
import dspy


class MemoryWriteSignature(dspy.Signature):
    """Persist a summary or artifact to long-term memory with tags and retention policy."""
    content: str = dspy.InputField()
    tags: str = dspy.InputField(desc="comma-separated")
    ttl_days: int = dspy.InputField()
    receipt: str = dspy.OutputField(desc="Storage URI or ID")
