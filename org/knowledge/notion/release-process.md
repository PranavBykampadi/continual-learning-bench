# Release process
Last edited: 2025-09-12 by Marcus

How code gets from main to customers. Ask me (Marcus) if anything here is unclear.

## Cadence

We release weekly on Thursdays at 15:00. The "deploy train" leaves then. Get your change merged by 14:30 or it waits for next week. Hotfixes can go any time with Dana's or my OK.

## Freezes

No releases during freeze windows. Freezes get announced in #releases at least a week ahead. Typical ones: end of year holidays, infra migrations.

## Changelog

Every user-facing change gets a bullet under `## Unreleased` in `CHANGELOG.md`, added in the same PR as the change.

Keep the bullet short and plain, written for a customer, e.g. `- Added gold tier`. Don't put ticket numbers in it, the notes go out to customers more or less as written and they don't care about our tracker. Past tense, starts with a capital.

At release time I move everything under Unreleased into a new version heading and copy it into the release notes email.

## Steps (release manager)

1. Check main is green.
2. Cut the version: move Unreleased to `## x.y.z`, bump the version, tag.
3. Deploy to staging, smoke test the portal (create a shipment, issue an invoice, check the label renders).
4. Deploy to prod.
5. Post in #releases. Send the notes email.

## Rollback

`deploy rollback <version>` from the ops box. Then tell #releases and #incidents what happened.
