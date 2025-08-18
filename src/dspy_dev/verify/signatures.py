from __future__ import annotations
import dspy

class BuildQueries(dspy.Signature):
    code: str = dspy.InputField(desc="Source code to verify")
    providers: str = dspy.InputField(desc="Comma-separated provider domains")
    queries_json: str = dspy.OutputField(desc="JSON list of doc search queries with intent")

class CheckConsistency(dspy.Signature):
    code: str = dspy.InputField()
    docs_json: str = dspy.InputField(desc="Retrieved doc snippets with versions")
    report_md: str = dspy.OutputField(desc="Verification report in Markdown")
