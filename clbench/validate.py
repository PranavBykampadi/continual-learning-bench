"""Check every ticket: the gold solution merges, the naive one passes CI but breaks every listed convention."""
import shutil
import sys

from clbench.agents import solve_with_gold
from clbench.grade import grade, new_workspace, overlay
from clbench.model import load_tickets


def check(ticket):
    problems = []
    workspace = new_workspace(ticket.snapshot)
    solve_with_gold(ticket, "", workspace)
    gold = grade(ticket, workspace)
    if not gold.merged:
        problems.append(f"gold not merged: ci={gold.ci_failures} violated={gold.violated}")
    shutil.rmtree(workspace.parent)

    workspace = new_workspace(ticket.snapshot)
    overlay(ticket.dir / "naive", workspace)
    naive = grade(ticket, workspace)
    if not naive.ci_passed:
        problems.append(f"naive fails CI: {naive.ci_failures}")
    if naive.passed:
        problems.append(f"naive is not caught for: {naive.passed}")
    shutil.rmtree(workspace.parent)
    return problems


def main():
    wanted = sys.argv[1:]
    failed = 0
    for ticket in load_tickets():
        if wanted and ticket.id not in wanted:
            continue
        problems = check(ticket)
        failed += bool(problems)
        print(ticket.id, "OK" if not problems else "FAIL")
        for problem in problems:
            print("   ", problem)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
