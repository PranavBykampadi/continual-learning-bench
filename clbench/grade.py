import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from clbench.model import ORG, ROOT, Feedback

IGNORED = {"__pycache__", ".pytest_cache", "_hidden", ".git"}
SNAPSHOT_OVERLAYS = {"a": [], "b": ["migration"]}


def overlay(source, target):
    shutil.copytree(source, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*IGNORED))


_built = {}


def snapshot_dir(name):
    """Each process builds its own copy, so parallel arms never share a directory."""
    if name not in _built:
        target = Path(tempfile.mkdtemp(prefix=f"clb-snapshot-{name}-")) / "parcelo"
        overlay(ORG / "seed", target)
        for layer in SNAPSHOT_OVERLAYS[name]:
            overlay(ORG / layer, target)
        _built[name] = target
    return _built[name]


def new_workspace(snapshot):
    workspace = Path(tempfile.mkdtemp(prefix="clb-")) / "parcelo"
    overlay(snapshot_dir(snapshot), workspace)
    return workspace


def _files(root):
    return {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and not IGNORED & set(p.relative_to(root).parts)
    }


def manifest(workspace, snapshot):
    base = snapshot_dir(snapshot)
    before, after = _files(base), _files(workspace)
    changed = sorted(
        p for p in before & after if not filecmp.cmp(base / p, workspace / p, shallow=False)
    )
    return {"changed": changed, "added": sorted(after - before), "removed": sorted(before - after)}


def diff_text(workspace, snapshot, limit=6000):
    base = snapshot_dir(snapshot)
    out = subprocess.run(
        ["diff", "-ruN", "-x", "__pycache__", "-x", ".pytest_cache", "-x", "_hidden", str(base), str(workspace)],
        capture_output=True, text=True,
    ).stdout
    out = out.replace(str(base) + "/", "a/").replace(str(workspace) + "/", "b/")
    return out[:limit]


def _run_pytest(workspace, target):
    report = workspace / "_hidden" / f"report-{Path(target).name}.xml"
    subprocess.run(
        [sys.executable, "-m", "pytest", target, "-q", "-p", "no:cacheprovider",
         "-o", "addopts=", f"--junitxml={report}"],
        cwd=workspace, capture_output=True, text=True, timeout=300,
    )
    results = {}
    if not report.exists():
        return {f"{target}::collection": "pytest produced no report"}
    for case in ET.parse(report).getroot().iter("testcase"):
        problem = case.find("failure")
        if problem is None:
            problem = case.find("error")
        message = None if problem is None else (problem.get("message") or "failed")[:300]
        results[f"{case.get('classname')}::{case.get('name')}"] = message
    return results


def _convention_of(test_name):
    name = test_name.split("::")[-1]
    if not name.startswith("test_conv_"):
        return None
    return name[len("test_conv_"):].split("__")[0]


def grade(ticket, workspace):
    hidden = workspace / "_hidden"
    if hidden.exists():
        shutil.rmtree(hidden)
    shutil.copytree(ticket.dir / "hidden", hidden)
    for support in (ORG / "hidden_support").iterdir():
        if support.is_file():
            shutil.copy(support, hidden / support.name)
    (hidden / "manifest.json").write_text(json.dumps(manifest(workspace, ticket.snapshot)))

    hidden_results = _run_pytest(workspace, "_hidden")
    repo_results = _run_pytest(workspace, "tests")
    shutil.rmtree(hidden)

    ci_failures, violated = [], set()
    seen = set()
    for name, message in hidden_results.items():
        convention = _convention_of(name)
        if convention is None:
            if message is not None:
                ci_failures.append(f"{name.split('::')[-1]}: {message}")
        else:
            seen.add(convention)
            if message is not None:
                violated.add(convention)
    for name, message in repo_results.items():
        if message is not None:
            ci_failures.append(f"{name}: {message}")
    if not any(_convention_of(n) is None for n in hidden_results):
        ci_failures.append("hidden CI tests did not run")

    if seen - set(ticket.conventions):
        raise ValueError(f"{ticket.id}: convention tests {sorted(seen)} do not match {ticket.conventions}")
    violated |= set(ticket.conventions) - seen
    return Feedback(
        ci_passed=not ci_failures,
        ci_failures=ci_failures,
        passed=sorted(set(ticket.conventions) - violated),
        violated=sorted(violated & set(ticket.conventions)),
    )
