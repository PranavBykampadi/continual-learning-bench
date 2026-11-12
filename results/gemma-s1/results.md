# Results: run `gemma-s1`

| arm | tickets | CI pass | compliance | hidden-rule compliance | first-try merge | early / mid / late compliance | gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |
|---|---|---|---|---|---|---|---|---|---|---|
| none-rich | 40 | 0.88 | 0.09 | 0.12 | 0.00 | 0.12 / 0.08 / 0.07 | n/a | n/a | 0.93 (n=160) | 0.000 |
| notes-rich | 40 | 0.88 | 0.76 | 0.76 | 0.30 | 0.73 / 0.74 / 0.82 | +0.67 (+0.59, +0.75) | 90% | 0.17 (n=162) | 0.000 |
| oracle-rich | 40 | 0.88 | 0.84 | 0.88 | 0.47 | 0.83 / 0.88 / 0.80 | +0.75 (+0.68, +0.81) | 100% | 0.31 (n=70) | 0.000 |

Hidden rules, which a stateless frontier model follows less than half the time: `idempotent`, `money`, `no_legacy`, `settings`, `sorted`, `tests`.

## Compliance by how many times the agent has met the convention

| arm | 1st exposure | 2nd to 3rd | 4th and later |
|---|---|---|---|
| none-rich | 0.21 | 0.07 | 0.08 |
| notes-rich | 0.14 | 0.71 | 0.85 |
| oracle-rich | 0.86 | 0.75 | 0.84 |

## Rules introduced by a mid-stream change

| arm | `events` in order (1 = followed) | `changelog2` in order (1 = followed) | `docs_api` in order (1 = followed) |
|---|---|---|---|
| none-rich | 0000000000000000 | 00000000 | 000000000000 |
| notes-rich | 0111111111111111 | 01100111 | 011001010000 |
| oracle-rich | 1111111111111101 | 11111111 | 001000000001 |

![learning curve](curve.svg)
