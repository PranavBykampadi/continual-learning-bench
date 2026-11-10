import argparse
import json
import random
import shutil
import tempfile

from clbench.agents import claude, make_solver
from clbench.feedback import FEEDBACK_MODES
from clbench.grade import diff_text, grade, new_workspace
from clbench.learners import LEARNERS
from clbench.model import ROOT, Attempt, load_tickets


def ordered(tickets, order, seed):
    if order == "stream":
        return tickets
    shuffled = list(tickets)
    random.Random(seed).shuffle(shuffled)
    return shuffled


def run_arm(run_name, learner, feedback_mode, agent, order="stream", seed=0, limit=None):
    context_of, observe = LEARNERS[learner]
    render = FEEDBACK_MODES[feedback_mode]
    solve = make_solver(agent)
    model = agent.split(":", 1)[1] if agent.startswith("claude:") else None

    def reflect(prompt):
        if model is None:
            return "", 0.0
        text, result = claude(prompt, model, tempfile.mkdtemp(prefix="clb-reflect-"), "", budget_usd=0.5)
        return text, result.cost_usd

    arm_dir = ROOT / "runs" / run_name / f"{learner}-{feedback_mode}"
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
        result = solve(ticket, context, workspace)
        diff = diff_text(workspace, ticket.snapshot)
        feedback = grade(ticket, workspace)
        learn_cost = observe(state, ticket, diff, render(feedback), reflect)
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
            f"[{learner}-{feedback_mode}] {position:02d} {ticket.id} ci={'ok' if feedback.ci_passed else 'FAIL'} "
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
    args = parser.parse_args()
    run_arm(args.run_name, args.learner, args.feedback, args.agent, args.order, args.seed, args.limit)


if __name__ == "__main__":
    main()
