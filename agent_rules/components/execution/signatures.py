from __future__ import annotations
import dspy


class ExecuteToolSignature(dspy.Signature):
    """Decide on a tool call and emit structured tool arguments + expected result schema."""
    query: str = dspy.InputField()
    tools_catalog: str = dspy.InputField(desc="JSON schema of available tools")
    call: str = dspy.OutputField(desc="{tool_name: str, args: dict}")
    expects: str = dspy.OutputField(desc="JSON schema of expected result")
