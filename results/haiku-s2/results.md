# Results: run `haiku-s2`

| arm | tickets | CI pass | compliance | first-try merge | early / mid / late compliance | gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |
|---|---|---|---|---|---|---|---|---|---|
| history-rich | 24 | 0.92 | 0.92 | 0.75 | 0.81 / 0.97 / 0.97 | +0.46 (+0.33, +0.59) | 85% | 0.00 (n=70) | 0.006 |
| none-rich | 24 | 0.96 | 0.46 | 0.04 | 0.54 / 0.38 / 0.45 | n/a | n/a | 0.61 (n=71) | 0.005 |
| notes-rich | 24 | 0.96 | 0.90 | 0.71 | 0.84 / 0.94 / 0.91 | +0.44 (+0.31, +0.57) | 81% | 0.08 (n=51) | 0.009 |
| notes-sparse | 24 | 0.96 | 0.38 | 0.00 | 0.51 / 0.41 / 0.22 | -0.08 (-0.18, +0.03) | -14% | 0.64 (n=76) | 0.009 |
| oracle-rich | 24 | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 / 1.00 | +0.54 (+0.43, +0.66) | 100% | nan (n=0) | 0.006 |
| placebo-rich | 24 | 0.96 | 0.34 | 0.04 | 0.48 / 0.29 / 0.25 | -0.12 (-0.20, -0.05) | -22% | 0.66 (n=80) | 0.004 |

## Compliance by how many times the agent has met the convention

| arm | 1st exposure | 2nd to 3rd | 4th and later |
|---|---|---|---|
| history-rich | 0.44 | 0.89 | 0.99 |
| none-rich | 0.44 | 0.50 | 0.46 |
| notes-rich | 0.33 | 1.00 | 0.94 |
| notes-sparse | 0.56 | 0.39 | 0.37 |
| oracle-rich | 1.00 | 1.00 | 1.00 |
| placebo-rich | 0.44 | 0.33 | 0.34 |

## After the migration (`events` replaces `audit`)

| arm | `events` outcomes in order (1 = followed) |
|---|---|
| history-rich | 0 1 1 1 1 1 1 1 |
| none-rich | 0 0 0 0 0 0 0 0 |
| notes-rich | 0 1 1 1 1 0 1 0 |
| notes-sparse | 0 0 0 0 0 0 0 0 |
| oracle-rich | 1 1 1 1 1 1 1 1 |
| placebo-rich | 0 0 0 0 0 0 0 0 |

![learning curve](curve.svg)
