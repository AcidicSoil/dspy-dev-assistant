from __future__ import annotations
import dspy
from .signatures import AnalyzeTarget, PlanTests, WriteTests

AnalyzeTargetModule = dspy.Predict(AnalyzeTarget)
PlanTestsModule = dspy.Predict(PlanTests)
WriteTestsModule = dspy.Predict(WriteTests)
