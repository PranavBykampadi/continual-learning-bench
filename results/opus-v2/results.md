# Results: run `opus-v2`

| arm | tickets | CI pass | compliance | hidden-rule compliance | first-try merge | early / mid / late compliance | gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |
|---|---|---|---|---|---|---|---|---|---|---|
| memdir-rich | 40 | 1.00 | 0.94 | 0.88 | 0.80 | 0.92 / 0.91 / 0.98 | +0.35 (+0.25, +0.45) | 86% | 0.01 (n=94) | 0.517 |
| none-rich | 40 | 1.00 | 0.59 | 0.07 | 0.10 | 0.66 / 0.55 / 0.56 | n/a | n/a | 0.45 (n=128) | 0.145 |
| notes-rich | 40 | 1.00 | 0.91 | 0.81 | 0.70 | 0.92 / 0.86 / 0.95 | +0.32 (+0.24, +0.41) | 79% | 0.06 (n=99) | 0.295 |
| oracle-rich | 40 | 0.97 | 0.99 | 1.00 | 0.97 | 1.00 / 0.98 / 1.00 | +0.40 (+0.31, +0.50) | 100% | 0.00 (n=20) | 0.165 |

Hidden rules, which a stateless frontier model follows less than half the time: `idempotent`, `money`, `no_legacy`, `settings`, `sorted`, `tests`.

## Compliance by how many times the agent has met the convention

| arm | 1st exposure | 2nd to 3rd | 4th and later |
|---|---|---|---|
| memdir-rich | 0.36 | 1.00 | 0.99 |
| none-rich | 0.50 | 0.61 | 0.61 |
| notes-rich | 0.43 | 0.96 | 0.95 |
| oracle-rich | 1.00 | 1.00 | 0.99 |

## Rules introduced by a mid-stream change

| arm | `events` in order (1 = followed) | `changelog2` in order (1 = followed) | `sorted` in order (1 = followed) | `idempotent` in order (1 = followed) | `settings` in order (1 = followed) | `docs_api` in order (1 = followed) |
|---|---|---|---|---|---|---|
| memdir-rich | 1111111111111111 | 01111111 | 011111 | 011111 | 011111 | 011111111111 |
| none-rich | 0111011011111110 | 11101111 | 000000 | 000000 | 000000 | 111110110101 |
| notes-rich | 0111111111111111 | 11111111 | 011101 | 011111 | 011111 | 001111111111 |
| oracle-rich | 1111111111111111 | 11111111 | 111111 | 111111 | 111111 | 111111111111 |

![learning curve](curve.svg)
