# Combined results: `hd-opus`, `hd-opus-s2`

Each cell is the mean over runs, with the lowest and highest run in brackets.

| arm | compliance | hidden-rule compliance | first-try merge | gain vs stateless | repeat-violation rate | late-third compliance |
|---|---|---|---|---|---|---|
| memdir-rich | 0.89 [0.89, 0.89] | 0.90 [0.90, 0.90] | 0.78 [0.78, 0.78] | 0.63 [0.61, 0.64] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| none-rich | 0.26 [0.24, 0.28] | 0.12 [0.12, 0.13] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.79 [0.77, 0.81] | 0.27 [0.23, 0.31] |
| notes-rich | 0.80 [0.78, 0.83] | 0.79 [0.75, 0.83] | 0.47 [0.39, 0.56] | 0.54 [0.50, 0.59] | 0.10 [0.07, 0.13] | 0.90 [0.84, 0.97] |
| oracle-rich | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.74 [0.72, 0.76] | n/a | 1.00 [1.00, 1.00] |

Hidden rules, which a stateless frontier model follows less than half the time: `escalate`, `escalate_finance`, `no_dates`, `signoff`, `tag`.

## Compliance per rule, all runs pooled

| arm | `credit_cap` | `escalate` | `escalate_finance` | `greeting` | `identity` | `no_dates` | `signoff` | `tag` |
|---|---|---|---|---|---|---|---|---|
| memdir-rich | 0.80 | 0.80 | 0.80 | 0.90 | 1.00 | 0.83 | 0.94 | 0.94 |
| none-rich | 0.40 | 0.00 | 0.00 | 0.45 | 1.00 | 0.00 | 0.00 | 0.36 |
| notes-rich | 0.80 | 0.80 | 0.80 | 0.90 | 1.00 | 0.58 | 0.72 | 0.92 |
| oracle-rich | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## First time the agent meets each rule, all runs pooled

| arm | followed on first exposure |
|---|---|
| memdir-rich | 0.12 (n=16) |
| none-rich | 0.19 (n=16) |
| notes-rich | 0.19 (n=16) |
| oracle-rich | 1.00 (n=16) |
