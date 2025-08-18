from __future__ import annotations
import dspy
from .signatures import BuildQueries, CheckConsistency

BuildQueriesModule = dspy.Predict(BuildQueries)
CheckConsistencyModule = dspy.Predict(CheckConsistency)
