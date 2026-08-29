from __future__ import annotations
import dspy
from agent_rules.components.planning.modules import Planner
from agent_rules.components.verification.modules import SelfCritic
from agent_rules.components.execution.modules import ToolDecider


class PlanVerifyExecute(dspy.Module):
    """End-to-end pipeline that composes planner, verifier, and tool decider."""
    def __init__(self):
        super().__init__()
        self.planner = Planner()
        self.critic = SelfCritic()
        self.decider = ToolDecider()

    def forward(self, objective: str, context: str, constraints: str, tools_catalog: str) -> dict:
        plan = self.planner(objective=objective, context=context, constraints=constraints).plan
        review = self.critic(candidate=plan, constraints=constraints)
        final_plan = review.corrected or plan
        decision = self.decider(query=final_plan, tools_catalog=tools_catalog)
        return {
            "plan": final_plan,
            "verdict": review.verdict,
            "tool_call": decision.call,
            "expects": decision.expects,
        }
