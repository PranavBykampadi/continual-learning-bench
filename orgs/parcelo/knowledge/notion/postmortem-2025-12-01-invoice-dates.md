# Postmortem: invoices dated the wrong day (2025-12-01)
Last edited: 2025-12-04 by Priya

Status: final. Blameless, as always.

## Summary

On the morning of Monday 2025-12-01, support (Rosa) reported that customers on the US west coast were seeing invoices dated the next day. Some invoices also showed a paid date earlier than their issue date. About 300 invoices from the weekend were affected. No money was wrong, only dates.

## Timeline (UTC)

- 2025-11-29 ~23:00: nightly batch on the reporting box issues the weekend invoices.
- 2025-12-01 08:31: Rosa reports the issue in #support.
- 08:40: Farid opens an incident.
- 08:55: Farid notices some timestamps carry a timezone and some don't.
- 09:20: Priya confirms the cause.
- 09:22: mitigated by restarting the batch job with `TZ=UTC`.
- 2025-12-02: affected rows corrected by a one-off script.

## Root cause

We read "now" in at least four different ways across the codebase: `datetime.now()`, `datetime.utcnow()`, `time.time()` in one script, and `clock.now()` in the newer code. The API servers run in UTC so most of these happen to agree there. The reporting box was set to local time (US/Pacific) after the OS reimage in November, so the batch job got naive local times while the API got naive UTC times, and comparing the two put some invoices in the future.

Naive datetimes made it worse. Nothing stopped us from comparing a naive local time with a naive UTC time.

## What went well

- Support caught it within an hour of business start.
- Mitigation was one restart.

## What didn't

- We had no alert for invoices dated in the future.
- The reimage changed the box timezone and nobody knew.
- Tests couldn't have caught it. Code that calls `datetime.now()` directly can't be pinned to a fixed time, so nobody tests the date logic.

## Action items

1. **New code reads the current time only through `clock.now()`** from `parcelo.clock`. No `datetime.now()`, `datetime.utcnow()` or `time.time()` in new code. `clock.now()` returns an aware UTC datetime and can be pinned with `clock.set_fixed(...)`. (owner: everyone, effective now)
2. Set every box to UTC and add a check to the provisioning script. (owner: Farid, done 12-03)
3. Alert on any invoice with an issue date in the future. (owner: Farid)
4. Old call sites stay as they are for now. Convert them when you're already in the file for another reason. (owner: whoever)
