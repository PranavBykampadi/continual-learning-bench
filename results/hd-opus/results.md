# Results: run `hd-opus`

| arm | tickets | CI pass | compliance | hidden-rule compliance | first-try merge | early / mid / late compliance | gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |
|---|---|---|---|---|---|---|---|---|---|---|
| memdir-rich | 18 | 1.00 | 0.89 | 0.90 | 0.78 | 0.72 / 0.94 / 1.00 | +0.64 (+0.51, +0.77) | 85% | 0.00 (n=60) | 0.293 |
| none-rich | 18 | 0.94 | 0.24 | 0.12 | 0.00 | 0.34 / 0.16 / 0.23 | n/a | n/a | 0.81 (n=59) | 0.144 |
| notes-rich | 18 | 0.94 | 0.83 | 0.83 | 0.56 | 0.75 / 0.77 / 0.97 | +0.59 (+0.47, +0.71) | 78% | 0.07 (n=59) | 0.177 |
| oracle-rich | 18 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 / 1.00 | +0.76 (+0.66, +0.85) | 100% | n/a (n=0) | 0.098 |

Hidden rules, which a stateless frontier model follows less than half the time: `escalate`, `escalate_finance`, `no_dates`, `signoff`, `tag`.

## Compliance by how many times the agent has met the convention

| arm | 1st exposure | 2nd to 3rd | 4th and later |
|---|---|---|---|
| memdir-rich | 0.12 | 1.00 | 1.00 |
| none-rich | 0.25 | 0.38 | 0.20 |
| notes-rich | 0.25 | 0.94 | 0.92 |
| oracle-rich | 1.00 | 1.00 | 1.00 |

## Rules introduced by a mid-stream change

| arm | `escalate_finance` in order (1 = followed) |
|---|---|
| memdir-rich | 01111 |
| none-rich | 00000 |
| notes-rich | 01111 |
| oracle-rich | 11111 |

![learning curve](curve.svg)
