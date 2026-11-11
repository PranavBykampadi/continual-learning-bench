"""Helpers for hidden convention tests. Runs inside the graded workspace."""
import ast
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MANIFEST = json.loads((HERE / "manifest.json").read_text())
CHANGED = MANIFEST["changed"]
ADDED = MANIFEST["added"]


def _function(path, name):
    tree = ast.parse((REPO / path).read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    raise AssertionError(f"{name} not found in {path}")


def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def calls_in(path, name):
    return [_dotted(n.func) for n in ast.walk(_function(path, name)) if isinstance(n, ast.Call)]


def assert_no_direct_time(path, name):
    bad = [c for c in calls_in(path, name) if c.split(".")[-1] in ("utcnow", "today", "time")
           or c.endswith("datetime.now") or c == "now"]
    assert not bad, f"direct time calls in {name}: {bad}"


def assert_no_uuid(path, name):
    bad = [c for c in calls_in(path, name) if "uuid" in c]
    assert not bad, f"uuid used in {name}: {bad}"


def assert_changelog(ticket_id):
    text = (REPO / "CHANGELOG.md").read_text()
    match = re.search(r"## Unreleased\n(.*?)(\n## |\Z)", text, re.S)
    assert match, "no Unreleased section"
    bullets = [line for line in match.group(1).splitlines() if line.strip().startswith("-")]
    assert any(line.rstrip().endswith(f"({ticket_id})") for line in bullets), (
        f"no Unreleased bullet ending with ({ticket_id})"
    )


def assert_new_unit_test():
    new = [p for p in ADDED if p.startswith("tests/unit/") and Path(p).name.startswith("test_")]
    assert new, "no new test file under tests/unit/"
    frozen = [p for p in CHANGED + ADDED if p.startswith("tests/") and not p.startswith("tests/unit/")]
    assert not frozen, f"top-level tests touched: {frozen}"


def assert_no_legacy_imports():
    for path in CHANGED + ADDED:
        if not path.endswith(".py") or path.startswith("parcelo/legacy/"):
            continue
        tree = ast.parse((REPO / path).read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.ImportFrom):
                names = [node.module or ""] + [f"{node.module}.{a.name}" for a in node.names]
            elif isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            assert not any("parcelo.legacy" in n for n in names), f"{path} imports parcelo.legacy"


def dollars(value):
    """CI helper: read an amount as a float whether the code returned Money or a number."""
    return value.cents / 100 if hasattr(value, "cents") else float(value)
