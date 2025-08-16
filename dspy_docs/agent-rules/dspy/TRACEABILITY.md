# Legacy to DSPy Traceability

| Legacy Rule | DSPy Signature | Module |
| --- | --- | --- |
| project/analyze-issue.mdc | AnalyzeIssue | AnalyzerModule |
| project/implement-task.mdc | ImplementTask | ImplementerModule |
| project/code-analysis.mdc | AnalyzeCode | ReviewModule |
| project/check.mdc | RunChecks | CheckModule |
| project/commit.mdc, project/commit-fast.mdc | CommitCode | CommitModule |
| project/update-docs.mdc, project/create-docs.mdc, project/add-to-changelog.mdc | UpdateDocs | DocModule |
| project/bug-fix.mdc | AnalyzeIssue → ImplementTask → ReviewModule → CheckModule → DocModule → CommitModule |
| project/continuous-improvement.mdc | AnalyzeCode & UpdateDocs | ReviewModule & DocModule |
| global/github-issue-creation.mdc | AnalyzeIssue | AnalyzerModule |
| global/mcp-peekaboo-setup.mdc, global/mcp-sync-rule.md | RunChecks & UpdateDocs | CheckModule & DocModule |

Legacy files are retained for reference but the DSPy modules above now govern active development.
