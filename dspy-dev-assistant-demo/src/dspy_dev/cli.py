from __future__ import annotations
import sys
import pathlib
import typer
from rich import print
from .config import load_config
from .refactor.pipeline import run_refactor
from .testgen.pipeline import run_testgen
from .verify.pipeline import run_verify

app = typer.Typer(help="DSPy-powered developer assistant CLI")

@app.command()
def refactor(
    path: str = typer.Argument(..., help="File or directory to analyze"),
    rules: str = typer.Option(None, help="Comma-separated rules. Default: all"),
    apply: bool = typer.Option(False, "--apply", help="Apply patches instead of dry run"),
    include: str | None = typer.Option(None, help="Glob include filter"),
    exclude: str | None = typer.Option(None, help="Glob exclude filter"),
    patch_out: str | None = typer.Option(None, help="Directory to write patches"),
    patch_format: str = typer.Option("unified", help="Patch format: unified|git"),
):
    cfg = load_config()
    target = pathlib.Path(path)
    if not target.exists():
        typer.secho(f"Path not found: {target}", fg=typer.colors.RED)
        raise typer.Exit(code=2)
    rule_list = [r.strip() for r in rules.split(",")] if rules else None
    result = run_refactor(
        root=target,
        rules=rule_list,
        apply=apply,
        include_glob=include,
        exclude_glob=exclude,
        patch_out=pathlib.Path(patch_out) if patch_out else None,
        patch_format=patch_format,
        config=cfg,
    )
    print(result.summary())

@app.command()
def testgen(
    target: str = typer.Argument(..., help="Package/module or object path"),
    out: str = typer.Option("tests", help="Where to write tests"),
    target_coverage: float = typer.Option(0.85, help="Target coverage 0..1"),
    max_revisions: int = typer.Option(2, help="Self-review iterations"),
):
    cfg = load_config()
    res = run_testgen(target=target, out_dir=out, target_coverage=target_coverage, max_revisions=max_revisions, config=cfg)
    print(res.summary())

@app.command()
def verify(
    path: str = typer.Argument(..., help="File/dir to verify against docs"),
    providers: str = typer.Option(None, help="Comma-separated providers (e.g., stripe,openai)"),
    severity: str = typer.Option("medium", help="low|medium|high"),
    report: str | None = typer.Option(None, help="Report output path (e.g., out/verify.md)"),
    ci: bool = typer.Option(False, help="Exit non-zero on high severity issues"),
):
    cfg = load_config()
    prov_list = [p.strip() for p in providers.split(",")] if providers else cfg.verify.providers if cfg.verify.providers else []
    res = run_verify(path, providers=prov_list, severity=severity, report_path=report, config=cfg)
    print(res.summary())
    if ci and res.has_high_severity:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
