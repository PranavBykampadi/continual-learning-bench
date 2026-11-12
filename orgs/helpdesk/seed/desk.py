#!/usr/bin/env python3
"""Marlowe & Pine support desk tool. Run it from this directory: python desk.py <command> ..."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEAMS = ("billing-review", "finance-ops", "shipping-ops", "trust-safety", "tier2")

USAGE = """usage: python desk.py <command> ...
  show customer <id or email>
  show order <order id>
  refund <case> <order> <amount>
  credit <case> <customer> <amount>
  escalate <case> <team> [note]
  tag <case> <label>
  verify <case> <customer> <order>
  set-email <case> <customer> <new email>
  close <case>
teams: """ + ", ".join(TEAMS)


def load(name):
    return json.loads((ROOT / name).read_text())


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + "\n")


def log(entry):
    path = ROOT / "actions.jsonl"
    lines = path.read_text().splitlines() if path.exists() else []
    entry = {"n": len(lines) + 1, **entry}
    with path.open("a") as handle:
        handle.write(json.dumps(entry) + "\n")


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def amount_of(text):
    try:
        value = round(float(text.lstrip("$")), 2)
    except ValueError:
        fail(f"bad amount {text!r}")
    if value <= 0:
        fail("amount must be positive")
    return value


def find_customer(customers, key):
    for customer in customers:
        if key in (customer["id"], customer["email"]):
            return customer
    fail(f"no customer {key}")


def find_order(orders, key):
    for order in orders:
        if order["id"] == key:
            return order
    fail(f"no order {key}")


def open_case(cases, case_id):
    record = cases.setdefault(case_id, {"status": "open", "tags": [], "escalated_to": []})
    if record["status"] == "closed":
        fail(f"case {case_id} is closed")
    return record


def show(args):
    if len(args) != 2:
        fail(USAGE)
    kind, key = args
    if kind == "customer":
        print(json.dumps(find_customer(load("customers.json"), key), indent=2))
    elif kind == "order":
        print(json.dumps(find_order(load("orders.json"), key), indent=2))
    else:
        fail(USAGE)


def refund(args):
    if len(args) != 3:
        fail(USAGE)
    case_id, order_id, raw = args
    value = amount_of(raw)
    orders, cases = load("orders.json"), load("cases.json")
    order = find_order(orders, order_id)
    open_case(cases, case_id)
    if value > round(order["total"] - order["refunded"], 2):
        fail(f"{order_id} has only {order['total'] - order['refunded']:.2f} left to refund")
    order["refunded"] = round(order["refunded"] + value, 2)
    save("orders.json", orders)
    save("cases.json", cases)
    log({"case": case_id, "action": "refund", "order": order_id, "amount": value})
    print(f"refunded {value:.2f} on {order_id}")


def credit(args):
    if len(args) != 3:
        fail(USAGE)
    case_id, customer_id, raw = args
    value = amount_of(raw)
    customers, cases = load("customers.json"), load("cases.json")
    customer = find_customer(customers, customer_id)
    open_case(cases, case_id)
    customer["credit_balance"] = round(customer["credit_balance"] + value, 2)
    save("customers.json", customers)
    save("cases.json", cases)
    log({"case": case_id, "action": "credit", "customer": customer["id"], "amount": value})
    print(f"credited {value:.2f} to {customer['id']}")


def escalate(args):
    if len(args) < 2:
        fail(USAGE)
    case_id, team, note = args[0], args[1], " ".join(args[2:])
    if team not in TEAMS:
        fail(f"unknown team {team}. teams: {', '.join(TEAMS)}")
    cases = load("cases.json")
    record = open_case(cases, case_id)
    record["escalated_to"].append(team)
    save("cases.json", cases)
    log({"case": case_id, "action": "escalate", "team": team, "note": note})
    print(f"{case_id} escalated to {team}")


def tag(args):
    if len(args) != 2:
        fail(USAGE)
    case_id, label = args
    cases = load("cases.json")
    record = open_case(cases, case_id)
    record["tags"].append(label)
    save("cases.json", cases)
    log({"case": case_id, "action": "tag", "label": label})
    print(f"tagged {case_id} {label}")


def verify(args):
    if len(args) != 3:
        fail(USAGE)
    case_id, customer_id, order_id = args
    customers, orders, cases = load("customers.json"), load("orders.json"), load("cases.json")
    customer = find_customer(customers, customer_id)
    order = find_order(orders, order_id)
    open_case(cases, case_id)
    ok = order["customer"] == customer["id"]
    save("cases.json", cases)
    log({"case": case_id, "action": "verify", "customer": customer["id"], "order": order_id, "ok": ok})
    print("identity confirmed" if ok else "identity check failed: that order is not on this account")
    sys.exit(0 if ok else 1)


def set_email(args):
    if len(args) != 3:
        fail(USAGE)
    case_id, customer_id, new = args
    if "@" not in new:
        fail(f"bad email {new!r}")
    customers, cases = load("customers.json"), load("cases.json")
    customer = find_customer(customers, customer_id)
    open_case(cases, case_id)
    old = customer["email"]
    customer["email"] = new
    save("customers.json", customers)
    save("cases.json", cases)
    log({"case": case_id, "action": "set-email", "customer": customer["id"], "old": old, "new": new})
    print(f"{customer['id']} email is now {new}")


def close(args):
    if len(args) != 1:
        fail(USAGE)
    case_id = args[0]
    cases = load("cases.json")
    record = open_case(cases, case_id)
    record["status"] = "closed"
    save("cases.json", cases)
    log({"case": case_id, "action": "close"})
    print(f"closed {case_id}")
    if not (ROOT / "outbox" / f"{case_id}.md").exists():
        print(f"note: no reply found at outbox/{case_id}.md")


COMMANDS = {
    "show": show, "refund": refund, "credit": credit, "escalate": escalate, "tag": tag,
    "verify": verify, "set-email": set_email, "close": close,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(USAGE)
        sys.exit(2)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
