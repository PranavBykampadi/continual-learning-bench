# Marlowe & Pine support desk

Marlowe & Pine sells home goods online. This directory is the support desk for one case at a time.

- `customers.json` and `orders.json` hold the account and order data. Look people up there or with `python desk.py show`.
- `macros/` has reply templates the team has used before. Edit them freely for your reply.
- `history/` has a sample of past cases and how they were handled.
- Replies go in `outbox/<case id>.md`, one file per case, plain text.

## desk.py

Run it from this directory. Every action on a case goes through it, and each one is appended to `actions.jsonl`.

    python desk.py show customer <id or email>
    python desk.py show order <order id>
    python desk.py refund <case> <order> <amount>
    python desk.py credit <case> <customer> <amount>
    python desk.py escalate <case> <team> [note]
    python desk.py tag <case> <label>
    python desk.py verify <case> <customer> <order>
    python desk.py set-email <case> <customer> <new email>
    python desk.py close <case>

`refund` pays money back to the card on an order. `credit` adds store credit to the customer's balance. `escalate` hands the case to another team (billing-review, finance-ops, shipping-ops, trust-safety or tier2). `verify` checks that an order belongs to the customer. A closed case cannot be changed.
