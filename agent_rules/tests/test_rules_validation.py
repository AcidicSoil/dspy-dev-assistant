from __future__ import annotations
from agent_rules.tools.migration.validate import validate_bundle


def test_schema_ok():
    text = """
apiVersion: dspy.rules/v1
kind: RuleBundle
meta: {name: demo, version: 1.0.0, precedence: 60}
rules:
  - id: r1
    signature: {name: PlanSignature}
    module: {type: planning, impl: Planner}
"""
    validate_bundle(text)
