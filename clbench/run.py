import argparse
import json
import random
import shutil
import tempfile

from clbench.agents import make_backend, make_solver
from clbench.feedback import FEEDBACK_MODES
from clbench.grade import diff_text, grade, new_workspace
from clbench.knowledge import ARM_SUFFIX, KNOWLEDGE_MODES, materialize
from clbench.learners import LEARNERS
from clbench.model import ROOT, Attempt, load_tickets


def ordered(tickets, order, seed):
    if order == "stream":
        return tickets
    shuffled = list(tickets)
    random.Random(seed).shuffle(shuffled)
    return shuffled


MEMORY_FILE_LIMIT = 20000
MEMORY_FILES = 40


def write_tree(folder, files):
    for name, text in files.items():
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text(text)
    folder.mkdir(parents=True, exist_ok=True)


def read_tree(folder):
    """The agent's memory folder as {relative path: text}. Capped so memory cannot grow without bound."""
    files = {}
    for path in sorted(p for p in folder.rglob("*") if p.is_file())[:MEMORY_FILES]:
        try:
            files[str(path.relative_to(folder))] = path.read_text()[:MEMORY_FILE_LIMIT]
        except UnicodeDecodeError:
            continue
    return files


def run_arm(run_name, learner, feedback_mode, agent, order="stream", seed=0, limit=None, knowledge="none"):
    context_of, observe = LEARNERS[learner]
    render = FEEDBACK_MODES[feedback_mode]
    solve = make_solver(agent)
    backend = make_backend(agent)
    memory = None

    def reflect(prompt, tools=""):
        """One extra model call after feedback. With tools, it runs inside the agent's memory folder."""
        if backend is None:
            return "", 0.0
        text, result = backend(prompt, memory if tools else tempfile.mkdtemp(prefix="clb-reflect-"), tools)
        return text, result.cost_usd

    arm = f"{learner}-{feedback_mode}" + ARM_SUFFIX[knowledge]
    arm_dir = ROOT / "runs" / run_name / arm
    arm_dir.mkdir(parents=True, exist_ok=True)
    log, state_file = arm_dir / "attempts.jsonl", arm_dir / "state.json"
    done = len(log.read_text().splitlines()) if log.exists() else 0
    state = json.loads(state_file.read_text()) if state_file.exists() else {}

    tickets = ordered(load_tickets(), order, seed)[:limit]
    for position, ticket in enumerate(tickets):
        if position < done:
            continue
        context = context_of(state, ticket)
        workspace = new_workspace(ticket.snapshot)
        if KNOWLEDGE_MODES[knowledge]:
            materialize(workspace.parent / "company", position)
            context = KNOWLEDGE_MODES[knowledge] + context
        memory = workspace.parent / "memory"
        if "files" in state:
            write_tree(memory, state["files"])
        result = solve(ticket, context, workspace)
        diff = diff_text(workspace, ticket.snapshot)
        feedback = grade(ticket, workspace)
        learn_cost = observe(state, ticket, diff, render(feedback, ticket), reflect)
        if "files" in state:
            state["files"] = read_tree(memory)
        attempt = Attempt(
            position=position, ticket_id=ticket.id, feedback=feedback, cost_usd=result.cost_usd,
            turns=result.turns, seconds=round(result.seconds, 1), context_chars=len(context),
            learn_cost_usd=learn_cost, error=result.error,
        )
        (arm_dir / f"{position:02d}-{ticket.id}.diff").write_text(diff)
        state_file.write_text(json.dumps(state, indent=1))
        with log.open("a") as handle:
            handle.write(attempt.to_json() + "\n")
        shutil.rmtree(workspace.parent, ignore_errors=True)
        print(
            f"[{arm}] {position:02d} {ticket.id} ci={'ok' if feedback.ci_passed else 'FAIL'} "
            f"violated={feedback.violated} cost=${result.cost_usd + learn_cost:.3f}",
            flush=True,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--learner", choices=LEARNERS, required=True)
    parser.add_argument("--feedback", choices=FEEDBACK_MODES, default="rich")
    parser.add_argument("--agent", default="claude:haiku")
    parser.add_argument("--order", choices=["stream", "shuffled"], default="stream")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--knowledge", choices=KNOWLEDGE_MODES, default="none",
                        help="give the agent the company Slack, Notion and PR history")
    args = parser.parse_args()
    run_arm(args.run_name, args.learner, args.feedback, args.agent, args.order, args.seed, args.limit, args.knowledge)


if __name__ == "__main__":
    main()
