# Combined results: `haiku-s1`, `haiku-s2`

Each cell is the mean over runs, with the lowest and highest run in brackets.

| arm | compliance | first-try merge | gain vs stateless | repeat-violation rate | late-third compliance |
|---|---|---|---|---|---|
| history-rich | 0.92 [0.92, 0.92] | 0.79 [0.75, 0.83] | 0.45 [0.43, 0.46] | 0.00 [0.00, 0.00] | 0.97 [0.97, 0.97] |
| none-rich | 0.47 [0.46, 0.48] | 0.04 [0.04, 0.04] | 0.00 [0.00, 0.00] | 0.57 [0.53, 0.61] | 0.41 [0.38, 0.45] |
| none-rich+org | 0.56 [0.53, 0.59] | 0.12 [0.08, 0.17] | 0.09 [0.04, 0.13] | 0.51 [0.44, 0.57] | 0.45 [0.41, 0.50] |
| none-rich+org-directed | 0.74 [0.73, 0.75] | 0.25 [0.21, 0.29] | 0.27 [0.24, 0.29] | 0.29 [0.28, 0.30] | 0.70 [0.67, 0.73] |
| notes-rich | 0.89 [0.88, 0.90] | 0.67 [0.62, 0.71] | 0.41 [0.39, 0.44] | 0.06 [0.04, 0.08] | 0.92 [0.91, 0.94] |
| notes-rich+org-directed | 0.90 [0.89, 0.92] | 0.58 [0.54, 0.62] | 0.43 [0.41, 0.46] | 0.09 [0.06, 0.11] | 0.91 [0.91, 0.91] |
| notes-sparse | 0.50 [0.38, 0.61] | 0.04 [0.00, 0.08] | 0.02 [-0.08, 0.12] | 0.63 [0.61, 0.64] | 0.42 [0.22, 0.62] |
| oracle-rich | 0.99 [0.98, 1.00] | 0.94 [0.88, 1.00] | 0.52 [0.49, 0.54] | 0.00 [0.00, 0.00] | 0.98 [0.97, 1.00] |
| placebo-rich | 0.33 [0.33, 0.34] | 0.02 [0.00, 0.04] | -0.14 [-0.16, -0.12] | 0.69 [0.66, 0.71] | 0.28 [0.25, 0.31] |

## Compliance per rule, all runs pooled

| arm | `audit` | `changelog` | `clock` | `errors` | `events` | `ids` | `money` | `no_legacy` | `tests` |
|---|---|---|---|---|---|---|---|---|---|
| history-rich | 0.89 | 0.93 | 1.00 | 0.94 | 0.88 | 0.83 | 0.91 | 0.83 | 0.92 |
| none-rich | 0.61 | 0.57 | 0.91 | 0.83 | 0.06 | 0.92 | 0.00 | 0.00 | 0.08 |
| none-rich+org | 0.67 | 0.75 | 0.91 | 0.83 | 0.31 | 0.92 | 0.14 | 0.25 | 0.12 |
| none-rich+org-directed | 1.00 | 0.68 | 0.95 | 0.92 | 0.88 | 0.83 | 0.68 | 0.67 | 0.17 |
| notes-rich | 0.94 | 0.93 | 0.95 | 0.97 | 0.75 | 0.83 | 0.73 | 0.75 | 0.92 |
| notes-rich+org-directed | 1.00 | 0.86 | 1.00 | 0.97 | 0.81 | 0.92 | 0.82 | 0.92 | 0.83 |
| notes-sparse | 0.61 | 0.68 | 0.73 | 0.83 | 0.00 | 0.92 | 0.00 | 0.42 | 0.12 |
| oracle-rich | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.92 | 0.95 | 1.00 | 1.00 |
| placebo-rich | 0.44 | 0.11 | 0.77 | 0.75 | 0.06 | 0.58 | 0.00 | 0.00 | 0.08 |

## First time the agent meets each rule, all runs pooled

| arm | followed on first exposure |
|---|---|
| history-rich | 0.39 (n=18) |
| none-rich | 0.50 (n=18) |
| none-rich+org | 0.67 (n=18) |
| none-rich+org-directed | 0.72 (n=18) |
| notes-rich | 0.33 (n=18) |
| notes-rich+org-directed | 0.78 (n=18) |
| notes-sparse | 0.56 (n=18) |
| oracle-rich | 0.94 (n=18) |
| placebo-rich | 0.44 (n=18) |
