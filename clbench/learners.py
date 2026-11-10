"""Learners decide what the agent knows at each ticket and how feedback changes that.

A learner is state (a JSON-serialisable dict) plus two functions:
context(state, ticket) -> text placed in the agent prompt
observe(state, ticket, diff, feedback_text, reflect) -> learning cost in USD
"""
from clbench.model import load_conventions

NOTES_LIMIT = 3000

REFLECT = """You are a software engineer keeping private working notes about a codebase and team you work with.
You just finished a ticket and received CI and code review feedback. Update your notes so that you do better on FUTURE,
DIFFERENT tickets in this repository. Keep what is still true, fix what turned out wrong, drop what is ticket-specific.
Keep the notes under {limit} characters. Reply with the full updated notes only, no preamble.

## Current notes
{notes}

## Ticket {id}: {title}
{body}

## Your change
{diff}

## Feedback
{feedback}
"""


def _no_context(state, ticket):
    return ""


def _no_observe(state, ticket, diff, feedback_text, reflect):
    return 0.0


def _oracle_context(state, ticket):
    rules = [c.rule for c in load_conventions().values() if ticket.snapshot in c.snapshots]
    return "\n## Team engineering handbook\n" + "\n".join(f"- {r}" for r in rules) + "\n"


def _history_context(state, ticket):
    if not state.get("entries"):
        return ""
    return "\n## Feedback you received on earlier tickets in this repository\n" + "\n".join(state["entries"]) + "\n"


def _history_observe(state, ticket, diff, feedback_text, reflect):
    state.setdefault("entries", []).append(f"### {ticket.id}: {ticket.title}\n{feedback_text}\n")
    return 0.0


def _notes_context(state, ticket):
    if not state.get("notes"):
        return ""
    return "\n## Your notes from earlier work in this repository\n" + state["notes"] + "\n"


def _notes_observe(state, ticket, diff, feedback_text, reflect):
    prompt = REFLECT.format(
        limit=NOTES_LIMIT, notes=state.get("notes") or "(empty)", id=ticket.id,
        title=ticket.title, body=ticket.body, diff=diff, feedback=feedback_text,
    )
    notes, cost = reflect(prompt)
    if notes.strip():
        state["notes"] = notes.strip()[:NOTES_LIMIT]
    return cost


PLACEBO = """
## Your notes from earlier work in this repository
- The service is called parcelo. It has customers, shipments, rates, invoices and reports.
- Run the tests with `python -m pytest -q`. They finish in under a second.
- Zones are local, national and international. Customer tiers are standard and gold.
- The in-memory store lives in `parcelo/store.py` and is shared through `db`.
- Read the ticket twice before starting and keep the change small.
- Function names use snake_case. Modules are grouped by business area.
"""


def _placebo_context(state, ticket):
    return PLACEBO


LEARNERS = {
    "placebo": (_placebo_context, _no_observe),
    "none": (_no_context, _no_observe),
    "oracle": (_oracle_context, _no_observe),
    "history": (_history_context, _history_observe),
    "notes": (_notes_context, _notes_observe),
}
