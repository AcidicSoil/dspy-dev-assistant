from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
import ast
import libcst as cst
import libcst.matchers as m
import difflib

@dataclass
class Smell:
    type: str
    location: str
    note: str
    function: str | None = None
    param: str | None = None

def _is_mutable_default(node: ast.AST) -> bool:
    return isinstance(node, (ast.List, ast.Dict, ast.Set))

def detect_smells_ast(code: str, path: Path) -> List[Smell]:
    """Detect mutable default args and long functions (simple thresholds)."""
    smells: List[Smell] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        smells.append(Smell(
            type="syntax-error",
            location=f"{path}:{getattr(e, 'lineno', '?')}",
            note=str(e),
        ))
        return smells

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Mutable defaults
            args = list(node.args.defaults or []) + list(node.args.kw_defaults or [])
            # Map defaults to arg names
            arg_names = [a.arg for a in node.args.args[-len(node.args.defaults):]] if node.args.defaults else []
            kw_names = [a.arg for a in node.args.kwonlyargs]
            # For kwonly defaults, positions align with kw_defaults
            for i, d in enumerate(node.args.kw_defaults or []):
                if d is not None and _is_mutable_default(d):
                    smells.append(Smell(
                        type="mutable-default",
                        location=f"{path}:{getattr(node, 'lineno', '?')}",
                        note=f"Parameter '{kw_names[i]}' has a mutable default",
                        function=node.name,
                        param=kw_names[i],
                    ))
            for i, d in enumerate(node.args.defaults or []):
                if _is_mutable_default(d):
                    name = arg_names[i] if i < len(arg_names) else f"arg{i}"
                    smells.append(Smell(
                        type="mutable-default",
                        location=f"{path}:{getattr(node, 'lineno', '?')}",
                        note=f"Parameter '{name}' has a mutable default",
                        function=node.name,
                        param=name,
                    ))
            # Long function
            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", None)
            if start is not None and end is not None:
                length = end - start + 1
                if length >= 25:  # simple threshold
                    smells.append(Smell(
                        type="long-method",
                        location=f"{path}:{start}-{end}",
                        note=f"Function '{node.name}' spans {length} lines (>=25)",
                        function=node.name,
                    ))
    return smells

class MutableDefaultFixer(cst.CSTTransformer):
    def __init__(self, to_fix: Dict[str, str]):
        # fn_name -> set of param names to fix (value type hint: 'list'/'dict'/'set')
        self.to_fix = to_fix
        self._current_fn: str | None = None
        super().__init__()

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self._current_fn = node.name.value

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        fn = self._current_fn or ""
        fix_params = self.to_fix.get(fn)
        if not fix_params:
            return updated_node

        # Build map of param -> kind (list/dict/set)
        target_kinds: dict[str,str] = {}
        # We can't easily know kinds now; assign 'list' as safe default and refine with matching
        # We'll infer by inspecting default value nodes during replacement below.
        # Replace defaults with None, collect guards
        params = updated_node.params

        def replace_default(p: cst.Param) -> tuple[cst.Param, str | None]:
            kind: str | None = None
            if p.default is not None and isinstance(p.default, (cst.List, cst.Dict, cst.Set)):
                if isinstance(p.default, cst.List): kind = "list"
                elif isinstance(p.default, cst.Dict): kind = "dict"
                elif isinstance(p.default, cst.Set): kind = "set"
                p = p.with_changes(default=cst.Name("None"))
            return p, kind

        new_params = []
        changed_for_guards: dict[str,str] = {}
        for p in params.params:
            new_p, k = replace_default(p)
            if k:
                changed_for_guards[new_p.name.value] = k
            new_params.append(new_p)
        new_kwonly = []
        for p in params.kwonly_params:
            new_p, k = replace_default(p)
            if k:
                changed_for_guards[new_p.name.value] = k
            new_kwonly.append(new_p)

        params = params.with_changes(params=new_params, kwonly_params=new_kwonly)

        # Build guard statements: if param is None: param = ...
        guard_body = []
        for name, kind in changed_for_guards.items():
            if kind == "list":
                rhs = cst.List([])
            elif kind == "dict":
                rhs = cst.Dict([])
            else:
                # set needs a call to set()
                rhs = cst.Call(func=cst.Name("set"), args=[])
            guard = cst.If(
                test=cst.Comparison(
                    left=cst.Name(name),
                    comparisons=[cst.ComparisonTarget(operator=cst.Is(), comparator=cst.Name("None"))],
                ),
                body=cst.IndentedBlock(
                    body=[cst.SimpleStatementLine([cst.Assign(targets=[cst.AssignTarget(cst.Name(name))], value=rhs)])]
                ),
                orelse=None,
            )
            guard_body.append(guard)

        new_body = updated_node.body
        if guard_body:
            new_body = cst.IndentedBlock(body=list(guard_body) + list(updated_node.body.body))

        return updated_node.with_changes(params=params, body=new_body)

def generate_mutable_default_patch(code: str, path: Path, smells: List[Smell]) -> str:
    """Return unified diff patch string for mutable default fixes. Empty if no fixes."""
    # Build map function -> param set, but we only know function names here; transformer infers kinds
    to_fix = {}
    for s in smells:
        if s.type == "mutable-default" and s.function and s.param:
            to_fix.setdefault(s.function, set()).add(s.param)

    if not to_fix:
        return ""

    try:
        module = cst.parse_module(code)
    except Exception:
        return ""

    fixer = MutableDefaultFixer({fn: ",".join(params) for fn, params in to_fix.items()})
    new_module = module.visit(fixer)
    new_code = new_module.code

    if new_code == code:
        return ""

    diff = "".join(difflib.unified_diff(
        code.splitlines(keepends=True),
        new_code.splitlines(keepends=True),
        fromfile=str(path),
        tofile=str(path),
    ))
    return diff

def run_rule_based_refactor(path: Path, code: str) -> str:
    """Detect smells and generate a diff patch using local rules only."""
    smells = detect_smells_ast(code, path)
    # Only implement patching for mutable defaults in this scaffold.
    patch = generate_mutable_default_patch(code, path, smells)
    return patch
