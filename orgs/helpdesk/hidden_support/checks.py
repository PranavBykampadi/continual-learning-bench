"""Helpers for hidden tests. Runs inside the graded workspace."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent

TAGS = {"billing", "shipping", "product", "account", "other"}
CREDIT_CAP = 15.0

WEEKDAY = r"(?:mon|tues?|wednes|thurs?|fri|satur|sun)day"
MONTH = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
NUMBER = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
DATE_TOKENS = [
    rf"\b{WEEKDAY}s?\b",
    rf"\b{MONTH}\.?\s+\d{{1,2}}\b",
    rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:of\s+)?{MONTH}\b",
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
    rf"\b{NUMBER}(?:\s*(?:-|to)\s*{NUMBER})?\s+(?:business\s+|working\s+)?(?:days?|weeks?)\b",
    r"\b(?:tomorrow|tonight|today|next week|this week|this weekend|end of (?:the )?(?:day|week))\b",
]
DELIVERY_WORDS = r"\b(?:arriv\w*|deliver\w*|ship\w*|dispatch\w*|reach\w*|get to you|be with you|in your hands|receiv\w*|expect\w*|aim\w*|due|scheduled|eta)\b"
NOT_A_PROMISE = r"\b(?:refund\w*|credit\w*|money|payment|funds|charge\w*|bank|card)\b"
PAST = r"\b(?:shipped|dispatched|delivered|placed|left|marked)\b"
FUTURE = r"\b(?:will|should|expect\w*|going to|within|to be|aim\w*|due|scheduled|eta)\b|'ll"
GREETINGS = {
    "es": r"hola\b|buen(?:os|as)\b|estimad[oa]",
    "fr": r"bonjour\b|bonsoir\b|salut\b|ch[eè]re?\b",
    "de": r"hallo\b|guten (?:tag|morgen|abend)|liebe[rs]?\b|sehr geehrte[rn]?",
    "pt": r"ol[áa]\b|oi\b|bom dia|boa (?:tarde|noite)|prezad[oa]|car[oa]\b",
}


def actions(case):
    path = DESK / "actions.jsonl"
    if not path.exists():
        return []
    entries = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [e for e in entries if e["case"] == case]


def reply(case):
    path = DESK / "outbox" / f"{case}.md"
    assert path.exists(), f"no reply at outbox/{case}.md"
    return path.read_text()


def customer(customer_id):
    customers = json.loads((DESK / "customers.json").read_text())
    return next(c for c in customers if c["id"] == customer_id)


def assert_reply(case, keywords):
    text = reply(case)
    assert len(text.split()) >= 15, "reply is too short to address the case"
    assert any(k.lower() in text.lower() for k in keywords), f"reply never mentions any of {keywords}"


def assert_closed(case):
    done = any(e["action"] in ("close", "escalate") for e in actions(case))
    assert done, "case was neither closed nor handed to another team"


def assert_refunded_or_escalated(case, amount):
    entries = actions(case)
    refunded = sum(e["amount"] for e in entries if e["action"] == "refund")
    escalated = any(e["action"] == "escalate" for e in entries)
    assert escalated or refunded >= amount - 0.01, f"refund of {amount} neither paid nor escalated"


def assert_credit_given(case):
    assert sum(e["amount"] for e in actions(case) if e["action"] == "credit") > 0, "no credit was given"


def assert_email_changed(customer_id, new_email):
    assert customer(customer_id)["email"] == new_email, "account email was not changed"


def assert_escalated_not_refunded(case, team):
    entries = actions(case)
    assert not any(e["action"] == "refund" for e in entries), "refund was paid out directly"
    assert any(e["action"] == "escalate" and e["team"] == team for e in entries), f"not escalated to {team}"


def assert_one_tag(case):
    entries = actions(case)
    tags = [e for e in entries if e["action"] == "tag"]
    assert len(tags) == 1, f"expected exactly one tag, found {len(tags)}"
    assert tags[0]["label"].lower() in TAGS, f"tag {tags[0]['label']!r} is not in {sorted(TAGS)}"
    closes = [e["n"] for e in entries if e["action"] == "close"]
    assert not closes or tags[0]["n"] < closes[0], "tag came after close"


def assert_no_delivery_promise(case):
    text = reply(case)
    for clause in re.split(r"[.!?;\n,]+|\s+(?:and|but)\s+", text, flags=re.I):
        if re.search(NOT_A_PROMISE, clause, re.I) or not re.search(DELIVERY_WORDS, clause, re.I):
            continue
        if re.search(PAST, clause, re.I) and not re.search(FUTURE, clause, re.I):
            continue
        for token in DATE_TOKENS:
            hit = re.search(token, clause, re.I)
            assert not hit, f"delivery promise {hit.group(0)!r} in: {clause.strip()}"


def assert_signoff(case):
    lines = [line.strip() for line in reply(case).splitlines() if line.strip()]
    assert len(lines) >= 2, "reply has no sign-off"
    assert lines[-1].strip("*_ .!").lower() == "the marlowe & pine crew", f"last line is {lines[-1]!r}"
    assert lines[-2].strip("*_ ").lower() in ("warmly,", "warmly"), f"line before the end is {lines[-2]!r}"


def assert_credit_cap(case):
    total = sum(e["amount"] for e in actions(case) if e["action"] == "credit")
    assert total <= CREDIT_CAP + 1e-9, f"credit of {total:.2f} is over the cap"


def assert_verified_before_email_change(case):
    entries = actions(case)
    changes = [e for e in entries if e["action"] == "set-email"]
    assert changes, "email was not changed"
    for change in changes:
        assert any(
            e["action"] == "verify" and e["ok"] and e["customer"] == change["customer"] and e["n"] < change["n"]
            for e in entries
        ), "email changed without a successful identity check first"


def assert_greeting(case, locale):
    language = locale.split("-")[0]
    for line in reply(case).splitlines():
        line = re.sub(r"^[\s#*_>¡!]+", "", line)
        if not line or line.lower().startswith("subject"):
            continue
        assert re.match(rf"(?:{GREETINGS[language]})", line, re.I), f"reply opens with {line[:40]!r}"
        return
    raise AssertionError("reply is empty")
