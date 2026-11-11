"""Agent backends. A backend is run(prompt, cwd, tools) -> (final text, AgentResult).

`tools` is "" (answer only), "files" (read and edit files in cwd) or "all" (files plus shell).
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from clbench.grade import overlay
from clbench.model import PACK

PROMPT = PACK["intro"] + "\n{context}\n# Ticket {id}: {title}\n\n{body}\n"
CLAUDE_TOOLS = {"": "", "files": "Read,Edit,Write,Glob,Grep", "all": "Read,Edit,Write,Glob,Grep,Bash"}
SHARED_FOLDERS = ("company", "memory")


@dataclass
class AgentResult:
    cost_usd: float = 0.0
    turns: int = 0
    seconds: float = 0.0
    error: str = ""


def _env():
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
    return env


def claude_backend(model):
    def run(prompt, cwd, tools):
        command = [
            "claude", "-p", prompt, "--model", model, "--output-format", "json",
            "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
            "--no-session-persistence", "--permission-mode", "acceptEdits",
            "--max-budget-usd", "1.0" if tools == "all" else "0.5", "--tools", CLAUDE_TOOLS[tools],
        ]
        for name in SHARED_FOLDERS:
            folder = Path(cwd).parent / name
            if folder.exists() and folder != Path(cwd):
                command += ["--add-dir", str(folder)]
        started = time.time()
        try:
            done = subprocess.run(command, cwd=cwd, env=_env(), capture_output=True, text=True, timeout=900)
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
    return run


PROTOCOL = """
You act by replying with exactly one action per message, and nothing after it:
<bash>one shell command, run in the current directory</bash>
<write path="relative/file">full new file content</write>
<done>one-line summary</done>
After each action you get its output. Read files with `cat`. Finish with <done>.
"""
ACTION = re.compile(r"<bash>(.*?)</bash>|<write path=\"([^\"]+)\">(.*?)</write>|<done>(.*?)</done>", re.S)
MAX_STEPS = 30
OUTPUT_LIMIT = 3000
HISTORY_CHARS = 60000


def _trim(messages):
    """Keep the task and the newest turns when the transcript outgrows a small context window."""
    head, tail = messages[:1], messages[1:]
    while len(tail) > 2 and sum(len(m["content"]) for m in head + tail) > HISTORY_CHARS:
        tail = tail[2:]
    return head + tail


def openai_backend(model, base_url):
    """A minimal text-protocol agent for any OpenAI-compatible endpoint, including models without tool calling."""
    def chat(messages):
        body = json.dumps({"model": model, "messages": _trim(messages), "max_tokens": 4000}).encode()
        request = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions", body,
            {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', 'none')}"},
        )
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(response.read())["choices"][0]["message"]["content"] or ""

    def run(prompt, cwd, tools):
        started = time.time()
        messages = [{"role": "user", "content": prompt + (PROTOCOL if tools else "")}]
        text, turns, error = "", 0, ""
        try:
            for turns in range(1, MAX_STEPS + 1):
                text = chat(messages)
                if not tools:
                    break
                action = ACTION.search(text)
                messages.append({"role": "assistant", "content": text[:action.end()] if action else text})
                if action is None:
                    output = "No action found. Reply with one <bash>, <write> or <done> block."
                elif action.group(4) is not None:
                    text = action.group(4)
                    break
                elif action.group(2):
                    target = (Path(cwd) / action.group(2)).resolve()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(action.group(3).lstrip("\n"))
                    output = f"wrote {action.group(2)}"
                else:
                    try:
                        done = subprocess.run(action.group(1), shell=True, cwd=cwd, env=_env(),
                                              capture_output=True, text=True, timeout=120)
                        output = (done.stdout + done.stderr)[-OUTPUT_LIMIT:] or f"(exit {done.returncode}, no output)"
                    except subprocess.TimeoutExpired:
                        output = "command timed out after 120s"
                messages.append({"role": "user", "content": output})
        except Exception as problem:
            error = repr(problem)[:300]
        return text, AgentResult(turns=turns, seconds=time.time() - started, error=error)
    return run


def make_backend(spec):
    """"claude:<model>" or "openai:<model>@<base url>". Scripted agents ("gold", "noop") have no backend."""
    kind, _, rest = spec.partition(":")
    if kind == "claude":
        return claude_backend(rest)
    if kind == "openai":
        model, _, base_url = rest.rpartition("@")
        return openai_backend(model, base_url)
    return None


def solve_with_gold(ticket, context, workspace):
    overlay(ticket.dir / "gold", workspace)
    return AgentResult()


def solve_with_nothing(ticket, context, workspace):
    return AgentResult()


def make_solver(spec):
    backend = make_backend(spec)
    if backend is None:
        return {"gold": solve_with_gold, "noop": solve_with_nothing}[spec]

    def solve(ticket, context, workspace):
        prompt = PROMPT.format(context=context, id=ticket.id, title=ticket.title, body=ticket.body)
        return backend(prompt, workspace, "all")[1]
    return solve
