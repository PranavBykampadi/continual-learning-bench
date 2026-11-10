# On-call runbook
Last edited: 2026-02-08 by Farid

You're on call Monday 09:00 to Monday 09:00. Handoff happens in #incidents with a short note.

## Before your week

- Make sure the pager app is on your phone and it actually rings (test page from the settings screen).
- Laptop charged, VPN works, you can get to the ops box.

## When the pager goes off

1. Ack within 10 min.
2. Open a thread in #incidents with :rotating_light: and one line saying what's broken.
3. Mitigate first, investigate later. Restart, roll back, turn it off.
4. If customers are affected, tell Rosa so support can answer the phones.
5. Close the thread with what you did.

## Common pages

**API latency p99 > 1s.** Nine times out of ten it's the reporting job doing a full scan. Kill it from the ops box (`jobs kill reporting`), latency recovers in a minute. File a ticket.

**Carrier API errors (swiftline / northpost).** Check their status page, but don't trust it, it's been green during real outages. We retry label creation 3 times then mark the job failed. When they're back, requeue: `jobs requeue labels --failed --since <time>`.

**DB disk > 80%.** Usually the log table. `db rotate-logs` from the ops box.

**Label printer offline.** Not ours. It's the warehouse's. Ack, forward to the warehouse ops channel, go back to bed.

## Escalation

If you're stuck for more than 30 min, page Tomasz or Dana. Nobody will be mad.

## After

If the incident had customer impact, write a postmortem in Notion within the week. Template is under Engineering > Postmortems.
