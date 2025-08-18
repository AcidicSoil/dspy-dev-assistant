from __future__ import annotations
import dspy

class AnalyzeTarget(dspy.Signature):
    target: str = dspy.InputField(desc="Package/module/object path")
    analysis: str = dspy.OutputField(desc="Key functions, behaviors, contracts")

class PlanTests(dspy.Signature):
    analysis: str = dspy.InputField()
    plan_json: str = dspy.OutputField(desc="JSON of test cases: normal, edge, error")

class WriteTests(dspy.Signature):
    target: str = dspy.InputField()
    plan_json: str = dspy.InputField()
    tests_code: str = dspy.OutputField(desc="pytest-compatible tests")
