from __future__ import annotations
import dspy
from .signatures import DetectSmells, PlanFix, GeneratePatch

DetectSmellsModule = dspy.Predict(DetectSmells)
PlanFixModule = dspy.Predict(PlanFix)
GeneratePatchModule = dspy.Predict(GeneratePatch)
