from __future__ import annotations
import dspy
from agent_rules.components.planning.modules import Planner


def test_planner_runs():
    p = Planner()
    p.predict = lambda **_: dspy.Prediction(plan="Step1: placeholder")  # bypass LM
    out = p(objective="OKR", context="Q3", constraints="none")
    assert hasattr(out, "plan")
