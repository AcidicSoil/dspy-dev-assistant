"""Generate a DSPy usage example tailored to a project type (Python 3.10+)."""
from __future__ import annotations
import textwrap

SUPPORTED = {
    "planning": "PlanSignature + Planner",
    "rag": "Retriever + rewriter + summarizer",
    "tool_use": "ExecuteToolSignature + ToolDecider",
    "self_critique": "CritiqueSignature + SelfCritic",
}


def generate_dspy_example(project_type: str) -> str:
    """Generates a DSPy example usage pattern for the given project type."""
    if not project_type or not isinstance(project_type, str):
        raise ValueError("`project_type` must be a non-empty string.")
    key = project_type.strip().lower()
    if key not in SUPPORTED:
        raise ValueError(f"Unsupported project_type: {project_type}. Supported: {sorted(SUPPORTED)}")

    if key == "planning":
        return textwrap.dedent(
            """
            import dspy
            
            class PlanSignature(dspy.Signature):
                """Produce a step-by-step plan to achieve an objective."""
                objective: str = dspy.InputField()
                context: str = dspy.InputField()
                constraints: str = dspy.InputField()
                plan: str = dspy.OutputField()

            class Planner(dspy.Module):
                def __init__(self):
                    super().__init__()
                    self.predict = dspy.Predict(PlanSignature)
                def forward(self, objective: str, context: str, constraints: str):
                    return self.predict(objective=objective, context=context, constraints=constraints)

            if __name__ == "__main__":
                planner = Planner()
                result = planner(objective="Ship v1", context="team=3, sprint=2w", constraints="no PII")
                print(result.plan)
            """
        )

    if key == "tool_use":
        return textwrap.dedent(
            """
            import json
            import dspy

            class ExecuteToolSignature(dspy.Signature):
                query: str = dspy.InputField()
                tools_catalog: str = dspy.InputField()
                call: str = dspy.OutputField()
                expects: str = dspy.OutputField()

            class ToolDecider(dspy.Module):
                def __init__(self):
                    super().__init__()
                    self.decide = dspy.Predict(ExecuteToolSignature)
                def forward(self, query: str, tools_catalog: str):
                    return self.decide(query=query, tools_catalog=tools_catalog)

            if __name__ == "__main__":
                tools = {"search": {"args": ["q"], "desc": "web search"}}
                decider = ToolDecider()
                out = decider(query="latest CPU news", tools_catalog=json.dumps(tools))
                print(out.call, out.expects)
            """
        )

    if key == "self_critique":
        return textwrap.dedent(
            """
            import dspy

            class CritiqueSignature(dspy.Signature):
                candidate: str = dspy.InputField()
                constraints: str = dspy.InputField()
                verdict: str = dspy.OutputField()
                corrected: str = dspy.OutputField()

            class SelfCritic(dspy.Module):
                def __init__(self):
                    super().__init__()
                    self.judge = dspy.Predict(CritiqueSignature)
                def forward(self, candidate: str, constraints: str):
                    return self.judge(candidate=candidate, constraints=constraints)

            if __name__ == "__main__":
                critic = SelfCritic()
                res = critic(candidate="Step1: ...", constraints="must be numbered")
                print(res.verdict, res.corrected)
            """
        )

    return textwrap.dedent(
        """
        import dspy

        class Retrieve(dspy.Signature):
            query: str = dspy.InputField()
            passage: str = dspy.OutputField()

        class RAGModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.retrieve = dspy.Predict(Retrieve)
            def forward(self, query: str):
                return self.retrieve(query=query)

        if __name__ == "__main__":
            rag = RAGModule()
            print(rag(query="What is DSPy?"))
        """
    )


if __name__ == "__main__":
    print(generate_dspy_example("planning"))
