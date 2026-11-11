# Authoring a ticket

A ticket is a directory `orgs/parcelo/tickets/NN_slug/` with four parts. `01_cancel_shipment` is the reference example.

- `ticket.json` has `id`, `title`, `snapshot` (`a` or `b`), `conventions`, and `body`.
- `hidden/test_ci.py` holds functional tests. `hidden/test_conv.py` holds one test per listed convention, named `test_conv_<convention id>`.
- `gold/` is an overlay of full files that solves the ticket and follows every team convention.
- `naive/` is an overlay that solves the ticket the way the older code in the repo does. It passes CI and breaks every listed convention.

Snapshot `a` is `orgs/parcelo/seed`. Snapshot `b` is `orgs/parcelo/seed` with `orgs/parcelo/migration` copied over it. Overlay files are full files, so start each from the snapshot's version.

## Rules

1. The body reads like a real ticket from a teammate. It states behavior, the file, and the function signature. It never states or hints at a convention. It never names `Money`, `clock`, `DomainError`, `audit`, `events`, `ids.new_id`, the changelog, or where tests go.
2. For a ticket that lists `no_legacy`, the body mentions that an existing helper in `parcelo/legacy/billing.py` has the same logic or numbers, the way a teammate would. The naive solution imports it. The gold solution reimplements it.
3. CI tests accept both the convention-following and the legacy style. Use `pytest.raises(Exception)` for failures. Read amounts through `checks.dollars(value)`. Never assert on audit, events, id format, or time source in `test_ci.py`.
4. Each convention test fails on the naive solution and passes on the gold one. Use the helpers in `orgs/parcelo/hidden_support/checks.py` where one fits (`assert_changelog`, `assert_new_unit_test`, `assert_no_legacy_imports`, `assert_no_direct_time`, `assert_no_uuid`). Check `money` with `isinstance(result, Money)`. Check `clock` by freezing time with `clock.set_fixed(...)` and comparing the stored value, plus `assert_no_direct_time`. Check `ids` by matching `^<prefix>_\d{6}$` on some lowercase prefix, plus `assert_no_uuid`. Check `audit` and `events` by the log growing with the changed entity's id as `entity_id`. The `events` test also asserts that `audit.LOG` did not grow.
5. The naive solution breaks only what the ticket lists. If the ticket does not list `changelog` or `tests`, the conventions test file has no test for it.
6. Keep each solution small, one function or one small module. If the ticket needs a new stored collection, add it to `parcelo/store.py` (and reset it in `reset()`), and say so in the body.
7. Run `.venv/bin/python -m clbench.validate <TICKET-ID>` from the repo root. A ticket is done when it prints `OK`.
