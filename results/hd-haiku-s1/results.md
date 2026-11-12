# Results: run `hd-haiku-s1`

| arm | tickets | CI pass | compliance | hidden-rule compliance | first-try merge | early / mid / late compliance | gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |
|---|---|---|---|---|---|---|---|---|---|---|
| memdir-rich | 18 | 0.83 | 0.87 | 0.90 | 0.61 | 0.75 / 0.90 / 0.97 | +0.55 (+0.41, +0.68) | 81% | 0.00 (n=61) | 0.012 |
| none-rich | 18 | 0.72 | 0.32 | 0.21 | 0.06 | 0.25 / 0.37 / 0.34 | n/a | n/a | 0.69 (n=61) | 0.006 |
| notes-rich | 18 | 0.72 | 0.81 | 0.79 | 0.39 | 0.75 / 0.90 / 0.78 | +0.49 (+0.33, +0.65) | 72% | 0.12 (n=56) | 0.009 |
| oracle-rich | 18 | 0.94 | 1.00 | 1.00 | 0.94 | 1.00 / 1.00 / 1.00 | +0.68 (+0.56, +0.79) | 100% | n/a (n=0) | 0.005 |

Hidden rules, which a stateless frontier model follows less than half the time: `escalate`, `escalate_finance`, `no_dates`, `signoff`, `tag`.

## Compliance by how many times the agent has met the convention

| arm | 1st exposure | 2nd to 3rd | 4th and later |
|---|---|---|---|
| memdir-rich | 0.25 | 0.88 | 1.00 |
| none-rich | 0.38 | 0.25 | 0.33 |
| notes-rich | 0.25 | 1.00 | 0.86 |
| oracle-rich | 1.00 | 1.00 | 1.00 |

## Rules introduced by a mid-stream change

| arm | `escalate_finance` in order (1 = followed) |
|---|---|
| memdir-rich | 01111 |
| none-rich | 10100 |
| notes-rich | 01111 |
| oracle-rich | 11111 |

![learning curve](curve.svg)
