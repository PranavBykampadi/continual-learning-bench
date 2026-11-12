# API reference (docs/api.md)
Last edited: 2026-03-23 by Lena

`docs/api.md` is what the support tooling team and the partner integrations team read to find out what they can call. It has been drifting, so from now on:

- When you add a public function (no leading underscore), add one line for it to `docs/api.md`, in the form `- `module.function(args)`: what it does`.
- Skip private helpers.
- If the module has no section in the file yet, add a `## module` heading for it.
- Reviewers: check for this line when you review.

The partner team has been asking about a few functions that exist in the code but not in the file. Everything added before this page was written is still missing, we'll backfill when someone has time.
