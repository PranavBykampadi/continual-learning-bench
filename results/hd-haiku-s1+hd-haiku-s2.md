# Combined results: `hd-haiku-s1`, `hd-haiku-s2`

Each cell is the mean over runs, with the lowest and highest run in brackets.

| arm | compliance | hidden-rule compliance | first-try merge | gain vs stateless | repeat-violation rate | late-third compliance |
|---|---|---|---|---|---|---|
| memdir-rich | 0.87 [0.87, 0.87] | 0.90 [0.90, 0.90] | 0.64 [0.61, 0.67] | 0.56 [0.55, 0.56] | 0.00 [0.00, 0.00] | 0.98 [0.97, 1.00] |
| none-rich | 0.31 [0.31, 0.32] | 0.20 [0.19, 0.21] | 0.03 [0.00, 0.06] | 0.00 [0.00, 0.00] | 0.72 [0.69, 0.76] | 0.31 [0.27, 0.34] |
| notes-rich | 0.79 [0.76, 0.81] | 0.78 [0.77, 0.79] | 0.33 [0.28, 0.39] | 0.47 [0.45, 0.49] | 0.14 [0.12, 0.15] | 0.76 [0.73, 0.78] |
| oracle-rich | 0.97 [0.94, 1.00] | 0.98 [0.96, 1.00] | 0.92 [0.89, 0.94] | 0.66 [0.64, 0.68] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |

Hidden rules, which a stateless frontier model follows less than half the time: `escalate`, `escalate_finance`, `no_dates`, `signoff`, `tag`.

## Compliance per rule, all runs pooled

| arm | `credit_cap` | `escalate` | `escalate_finance` | `greeting` | `identity` | `no_dates` | `signoff` | `tag` |
|---|---|---|---|---|---|---|---|---|
| memdir-rich | 0.80 | 0.80 | 0.80 | 0.90 | 0.83 | 0.83 | 0.94 | 0.94 |
| none-rich | 0.80 | 0.20 | 0.30 | 0.25 | 0.92 | 0.00 | 0.06 | 0.39 |
| notes-rich | 1.00 | 0.80 | 0.80 | 0.75 | 0.92 | 0.58 | 0.75 | 0.86 |
| oracle-rich | 1.00 | 1.00 | 1.00 | 0.95 | 0.92 | 1.00 | 0.97 | 0.97 |

## First time the agent meets each rule, all runs pooled

| arm | followed on first exposure |
|---|---|
| memdir-rich | 0.19 (n=16) |
| none-rich | 0.38 (n=16) |
| notes-rich | 0.25 (n=16) |
| oracle-rich | 1.00 (n=16) |
