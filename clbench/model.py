import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# One organization pack is active per process. Pick it with CLBENCH_ORG.
ORG = ROOT / "orgs" / os.environ.get("CLBENCH_ORG", "parcelo")
PACK = json.loads((ORG / "pack.json").read_text())


@dataclass(frozen=True)
class Convention:
    id: str
    rule: str
    review_comment: str
    snapshots: tuple


@dataclass(frozen=True)
class Ticket:
    id: str
    title: str
    body: str
    snapshot: str
    conventions: tuple
    dir: Path


@dataclass
class Feedback:
    ci_passed: bool
    ci_failures: list
    passed: list
    violated: list

    @property
    def compliance(self):
        total = len(self.passed) + len(self.violated)
        return len(self.passed) / total if total else 1.0

    @property
    def merged(self):
        return self.ci_passed and not self.violated


@dataclass
class Attempt:
    position: int
    ticket_id: str
    feedback: Feedback
    cost_usd: float = 0.0
    turns: int = 0
    seconds: float = 0.0
    context_chars: int = 0
    learn_cost_usd: float = 0.0
    error: str = ""

    def to_json(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, line):
        raw = json.loads(line)
        raw["feedback"] = Feedback(**raw["feedback"])
        return cls(**raw)


def load_conventions():
    raw = json.loads((ORG / "conventions.json").read_text())
    return {
        c["id"]: Convention(c["id"], c["rule"], c["review_comment"], tuple(c["snapshots"]))
        for c in raw
    }


def load_tickets():
    known = load_conventions()
    tickets = []
    for path in sorted((ORG / "tickets").iterdir()):
        if not (path / "ticket.json").exists():
            continue
        raw = json.loads((path / "ticket.json").read_text())
        for cid in raw["conventions"]:
            if raw["snapshot"] not in known[cid].snapshots:
                raise ValueError(f"{raw['id']}: {cid} is not active in snapshot {raw['snapshot']}")
        tickets.append(
            Ticket(raw["id"], raw["title"], raw["body"], raw["snapshot"], tuple(raw["conventions"]), path)
        )
    return tickets
