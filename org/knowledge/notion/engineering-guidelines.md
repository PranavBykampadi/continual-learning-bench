# Engineering guidelines
Last edited: 2025-10-06 by Dana

Living doc. If something here is wrong, fix it or ping me.

## Code style

- Line length 100. The formatter config in the repo has it, set your editor to match.
- Type hints on all public functions. Private helpers are up to you.
- Docstrings: Google style (`Args:` / `Returns:` / `Raises:`). One summary line minimum.
- Prefer f-strings over `%` formatting and `.format()`.
- Use the `logging` module, not `print()`. Get a module logger with `logging.getLogger(__name__)`.
- Imports sorted, stdlib first. Don't do `from x import *`.

## State changes

Every state change must call `audit.record(action, entity_id, ...)` right after the change, with the id of the thing you changed. Compliance pulls their monthly report from the audit log, so if a mutation isn't in there it didn't happen as far as they're concerned.

Action names look like `shipment.created`, `invoice.paid`. Entity first, then what happened.

## Pull requests

- Keep PRs small. If it's over ~400 lines, split it or warn your reviewer.
- Put the ticket id in the PR title.
- One approval to merge. Two if you touched billing.
- Don't merge on a red CI run "because it's flaky". Rerun it, and if it's actually flaky tell #eng.

## Branches

`<your-name>/<ticket>-short-description`. Delete after merge.

## Reviews

Try to get to review requests within one working day. Nits are nits, mark them as such so the author knows what's blocking.
