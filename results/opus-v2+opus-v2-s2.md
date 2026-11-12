# Combined results: `opus-v2`, `opus-v2-s2`

Each cell is the mean over runs, with the lowest and highest run in brackets.

| arm | compliance | hidden-rule compliance | first-try merge | gain vs stateless | repeat-violation rate | late-third compliance |
|---|---|---|---|---|---|---|
| memdir-rich | 0.94 [0.94, 0.95] | 0.87 [0.86, 0.88] | 0.80 [0.80, 0.80] | 0.35 [0.35, 0.36] | 0.02 [0.01, 0.03] | 0.98 [0.98, 0.98] |
| none-rich | 0.59 [0.59, 0.59] | 0.08 [0.07, 0.09] | 0.10 [0.10, 0.10] | 0.00 [0.00, 0.00] | 0.44 [0.44, 0.45] | 0.55 [0.54, 0.56] |
| notes-rich | 0.91 [0.90, 0.91] | 0.79 [0.78, 0.81] | 0.69 [0.68, 0.70] | 0.32 [0.32, 0.32] | 0.07 [0.06, 0.08] | 0.94 [0.92, 0.95] |
| oracle-rich | 0.99 [0.99, 0.99] | 1.00 [1.00, 1.00] | 0.97 [0.97, 0.97] | 0.40 [0.40, 0.41] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |

Hidden rules, which a stateless frontier model follows less than half the time: `idempotent`, `money`, `no_legacy`, `settings`, `sorted`, `tests`.

## Compliance per rule, all runs pooled

| arm | `audit` | `changelog` | `changelog2` | `clock` | `docs_api` | `errors` | `events` | `idempotent` | `ids` | `money` | `no_legacy` | `settings` | `sorted` | `tests` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| memdir-rich | 1.00 | 0.98 | 0.94 | 1.00 | 0.96 | 1.00 | 0.97 | 0.83 | 0.94 | 0.86 | 0.86 | 0.75 | 0.83 | 0.95 |
| none-rich | 0.89 | 0.90 | 0.75 | 0.93 | 0.71 | 0.88 | 0.72 | 0.08 | 0.94 | 0.00 | 0.14 | 0.00 | 0.00 | 0.16 |
| notes-rich | 1.00 | 0.98 | 0.94 | 1.00 | 0.88 | 1.00 | 0.94 | 0.83 | 0.88 | 0.75 | 0.71 | 0.75 | 0.67 | 0.89 |
| oracle-rich | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## First time the agent meets each rule, all runs pooled

| arm | followed on first exposure |
|---|---|
| memdir-rich | 0.43 (n=28) |
| none-rich | 0.54 (n=28) |
| notes-rich | 0.43 (n=28) |
| oracle-rich | 1.00 (n=28) |
