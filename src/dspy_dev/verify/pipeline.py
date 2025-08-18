from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..config import Config
from .modules import BuildQueriesModule, CheckConsistencyModule


@dataclass
class VerifyResult:
    report_path: Path | None
    has_high_severity: bool = False
    def summary(self) -> str:
        return f"[Verify] report={'written to ' + str(self.report_path) if self.report_path else 'stdout'}; high_severity={self.has_high_severity}"

def run_verify(path: str, providers: list[str], severity: str, report_path: str | None, config: Config) -> VerifyResult:
    target = Path(path)
    if target.is_dir():
        code = "\n\n".join(p.read_text(encoding='utf-8') for p in target.rglob("*.py"))
    else:
        code = target.read_text(encoding="utf-8")
    build = BuildQueriesModule()
    check = CheckConsistencyModule()

    queries_json = build(code=code, providers=",".join(providers)).queries_json
    # NOTE: Retrieval is out of scope for offline scaffold. In real code, search here and build docs_json.
    docs_json = "[]"
    report_md = check(code=code, docs_json=docs_json).report_md or "# Verification Report\n\n_No issues detected in scaffold._\n"

    report_file = Path(report_path) if report_path else None
    if report_file:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report_md, encoding="utf-8")
    return VerifyResult(report_path=report_file, has_high_severity=False)
