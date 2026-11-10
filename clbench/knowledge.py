"""The company's written knowledge (Slack, Notion, old pull requests) as it stood on the day of a ticket.

One ticket happens per day. A document is visible at a ticket only if it is dated before that day.
"""
import json
import sys
from collections import defaultdict
from datetime import date, timedelta

from clbench.model import ORG, load_conventions, load_tickets

KNOWLEDGE = ORG / "knowledge"
STREAM_START = date(2026, 3, 2)
MIGRATION_POSITION = 14

NOTE = (
    "\nThe company's Slack export, Notion pages and past pull request discussions are in `../company/` "
    "(read-only). The export was taken this morning.\n"
)


def ticket_date(position):
    return STREAM_START + timedelta(days=position)


def _header_date(path, prefix):
    line = path.read_text().splitlines()[1]
    if not line.startswith(prefix):
        raise ValueError(f"{path}: line 2 must start with '{prefix}'")
    return date.fromisoformat(line[len(prefix):].split()[0])


def documents():
    """Yield (relative output path, date, text) for every piece of the knowledge base."""
    for line in (KNOWLEDGE / "slack.jsonl").read_text().splitlines():
        if line.strip():
            m = json.loads(line)
            text = f"[{m['date']} {m['time']}] {m['author']}: {m['text']}"
            yield f"slack/{m['channel']}.txt", date.fromisoformat(m["date"]), text
    for page in sorted((KNOWLEDGE / "notion").glob("*.md")):
        yield f"notion/{page.name}", _header_date(page, "Last edited: "), page.read_text()
    for thread in sorted((KNOWLEDGE / "pulls").glob("*.md")):
        yield f"pulls/{thread.name}", _header_date(thread, "Merged: "), thread.read_text()


def materialize(target, position):
    today = ticket_date(position)
    files = defaultdict(list)
    for path, dated, text in documents():
        if dated < today:
            files[path].append(text)
    for path, parts in files.items():
        out = target / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(parts) + "\n")


def _source_text(file):
    if file == "slack.jsonl":
        return [(date.fromisoformat(json.loads(l)["date"]), json.loads(l)["text"])
                for l in (KNOWLEDGE / file).read_text().splitlines() if l.strip()]
    path = KNOWLEDGE / file
    prefix = "Last edited: " if file.startswith("notion/") else "Merged: "
    return [(_header_date(path, prefix), path.read_text())]


def validate():
    """Check that the evidence map is true of the files and matches the experimental design."""
    evidence = json.loads((KNOWLEDGE / "evidence.json").read_text())
    problems = []
    first_seen = {}
    for position, ticket in enumerate(load_tickets()):
        for convention in ticket.conventions:
            first_seen.setdefault(convention, position)

    for convention in load_conventions():
        items = evidence.get(convention, [])
        dated = []
        for item in items:
            hits = [d for d, text in _source_text(item["file"]) if item["needle"] in text]
            if not hits:
                problems.append(f"{convention}: needle not found in {item['file']}: {item['needle']!r}")
                continue
            dated.append((min(hits), item["kind"]))
        correct = [d for d, kind in dated if kind == "correct"]
        if convention == "tests":
            if items:
                problems.append("tests: must have no evidence")
            continue
        if not correct or min(correct) >= ticket_date(first_seen[convention]):
            problems.append(f"{convention}: no correct evidence visible at its first ticket")
        if convention == "events" and min(correct) < ticket_date(MIGRATION_POSITION) - timedelta(days=1):
            problems.append("events: announced before the migration")

    everything = "\n".join(text for _, _, text in documents())
    for d, text in ((d, t) for _, d, t in documents()):
        if "events.emit" in text and d < ticket_date(MIGRATION_POSITION) - timedelta(days=1):
            problems.append(f"events.emit mentioned on {d}, before the migration")
    for ticket in load_tickets():
        if ticket.id in everything:
            problems.append(f"knowledge base mentions ticket {ticket.id}")
    for marker in ("tests/unit", "frozen"):
        if marker in everything:
            problems.append(f"knowledge base contains '{marker}', which leaks the tests rule")
    return problems


if __name__ == "__main__":
    found = validate()
    print("\n".join(found) if found else "knowledge base OK")
    sys.exit(1 if found else 0)
