import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from clbench.grade import overlay

PROMPT = """You are a software engineer at a company, working in the `parcelo` service repository in the current directory.
Complete the ticket below by editing the code. You get one attempt. When you stop, your change goes to CI and code review.
You can run the existing tests with `python -m pytest -q`. Work only inside this directory.
{context}
# Ticket {id}: {title}

{body}
"""


@dataclass
class AgentResult:
    cost_usd: float = 0.0
    turns: int = 0
    seconds: float = 0.0
    error: str = ""


def claude(prompt, model, cwd, tools, budget_usd):
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
    command = [
        "claude", "-p", prompt, "--model", model, "--output-format", "json",
        "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
        "--no-session-persistence", "--permission-mode", "acceptEdits",
        "--max-budget-usd", str(budget_usd), "--tools", tools,
    ]
    started = time.time()
    try:
        done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=900)
        raw = json.loads(done.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as problem:
        return "", AgentResult(seconds=time.time() - started, error=repr(problem)[:300])
    result = AgentResult(
        cost_usd=raw.get("total_cost_usd") or 0.0,
        turns=raw.get("num_turns") or 0,
        seconds=time.time() - started,
        error=str(raw.get("result"))[:300] if raw.get("is_error") else "",
    )
    return str(raw.get("result") or ""), result


def solve_with_claude(model):
    def solve(ticket, context, workspace):
        prompt = PROMPT.format(context=context, id=ticket.id, title=ticket.title, body=ticket.body)
        _, result = claude(prompt, model, workspace, "Read,Edit,Write,Glob,Grep,Bash", budget_usd=1.0)
        return result
    return solve


def solve_with_gold(ticket, context, workspace):
    overlay(ticket.dir / "gold", workspace)
    return AgentResult()


def solve_with_nothing(ticket, context, workspace):
    return AgentResult()


def make_solver(spec):
    if spec.startswith("claude:"):
        return solve_with_claude(spec.split(":", 1)[1])
    return {"gold": solve_with_gold, "noop": solve_with_nothing}[spec]
