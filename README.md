# continual-learning-bench

A benchmark that asks one question: when an agent is deployed inside one organization, how much does it improve from the feedback that organization already produces?

The agent works through a stream of tasks at a simulated company. After each task it gets what a new hire gets: a pass or fail on the work, and a reviewer's comments. The company has rules that nobody handed the agent. The benchmark scores how fast the agent stops breaking them, and how well it keeps up when a rule changes.

It ships with two companies, a coding team and a customer support desk, on one harness. Any model that speaks the Claude CLI or an OpenAI-compatible API can run.

Status: working prototype. 1,376 agent attempts across three models. Opus and Gemma have one run per arm, so read their numbers as a first measurement.

## Results in one table

Share of the company's rules the agent followed, over the whole stream.

| company | arm | Gemma 31B | Haiku | Opus |
|---|---|---|---|---|
| coding team, 40 tickets | no memory | 0.09 | 0.38 | 0.59 |
| | notes from review | 0.76 | 0.89 | 0.91 |
| | agent-owned memory folder | not run | 0.91 | 0.94 |
| | told every rule | 0.84 | 0.99 | 0.99 |
| support desk, 18 cases | no memory | not run | 0.31 | 0.24 |
| | notes from review | not run | 0.79 | 0.83 |
| | agent-owned memory folder | not run | 0.87 | 0.89 |
| | told every rule | not run | 0.97 | 1.00 |

Haiku cells are the mean of two runs. Opus and Gemma cells are one run.

What this shows:

- **A stronger model does not remove the need to learn.** With no memory, Opus follows more rules than Haiku on the coding team because it reads more of them off the existing code. On the six rules the code does not reveal, Opus scores 0.07 and Haiku 0.10. On the support desk Opus with no memory scores below Haiku.
- **Learning from review closes most of the gap, for every model.** Notes take Gemma from 0.09 to 0.76, Haiku from 0.38 to 0.89, and Opus from 0.59 to 0.91.
- **The same pattern holds outside code.** The support desk runs on the unchanged harness and shows the same spread from no memory to told-everything.
- **An agent that organizes its own memory does at least as well as fixed-format notes.** The memory-folder arm beats notes in all four model and company pairs where both ran. On first-try fully correct work the gap is larger: 0.64 against 0.33 for Haiku on the support desk, 0.80 against 0.70 for Opus on the coding team.

## Why this benchmark

Published continual-learning benchmarks for coding agents replay public GitHub issues and score them with gold tests. Three things are missing from the ones we looked at:

- The learning signal is never deployment feedback. No benchmark we found gives the agent a pass or fail and review comments and holds the gold checks back for scoring.
- None test rules that exist only inside one organization. Public repos are in the training data, so a public-repo benchmark cannot tell "learned on the job" from "already knew".
- None compare how much an agent learns as the feedback gets worse. A real organization mostly produces "merged" or "not merged", and its reviewers miss things.

## How it works

### One step of the stream

1. The harness copies the company's workspace to a fresh temporary directory.
2. The learner supplies context. The context goes into the prompt above the task.
3. The agent does the task. It can read and edit files and run the project's own commands. It gets one attempt.
4. The grader runs hidden checks: a functional check, and one check per rule the task exercises.
5. The feedback mode turns the grade into text, and the learner updates its state from that text.

The agent never sees the hidden checks, the rule list, or the gold solution.

### Organization packs

A company is a directory under `orgs/`. `CLBENCH_ORG=<name>` selects it (default `parcelo`). A pack holds:

- `pack.json`: the workspace name, the snapshots, the agent's role, and the intro paragraph of the prompt.
- `seed/` and one overlay directory per mid-stream change.
- `conventions.json`: the rules. Each has the handbook sentence the oracle arm sees, the comment a reviewer writes when it is broken, the snapshots it applies to, and whether it is hidden.
- `tickets/NN_slug/`: the task text, hidden functional checks, hidden rule checks, a gold solution that follows every rule, and a naive solution done the old way.
- `hidden_support/`: helpers for the hidden checks.
- `knowledge/` (optional): the company's Slack, Notion and pull request history.

`python -m clbench.validate` is the gate for new content. For every task the gold solution must pass everything, and the naive solution must pass the functional check and fail every listed rule. A rule check the naive solution cannot fail is a bug, and the validator reports it.

A rule is marked **hidden** when a frontier model with no memory follows it less than half the time. Hidden rules take learning. The others can be read off the workspace. The report scores hidden rules separately so "reads carefully" is not counted as "learned".

### `parcelo`: a coding team

A small shipping service written for this benchmark, so no model has seen it. Older modules use floats for money, `datetime.now()`, `uuid`, `ValueError` and `print`. One newer module follows the team's current rules. 40 tickets, 14 rules, two mid-stream changes.

| rule | what it says | hidden |
|---|---|---|
| `money` | currency is `Money`, never a float | yes |
| `tests` | new tests go in a new file under `tests/unit/` | yes |
| `no_legacy` | never import `parcelo.legacy` | yes |
| `sorted` | functions that return a list of entities sort it by id | yes |
| `idempotent` | repeating a state change on an entity already in that state returns it unchanged | yes |
| `settings` | thresholds and rates are constants in `parcelo/settings.py` | yes |
| `clock` | read time through `clock.now()` | no |
| `errors` | raise `DomainError` with a registered code | no |
| `ids` | ids come from `ids.new_id(prefix)` | no |
| `docs_api` | every new public function gets a line in `docs/api.md` | no |
| `audit` | every state change calls `audit.record` (tickets 1 to 14) | no |
| `events` | every state change calls `events.emit`, and `audit.record` is banned (from ticket 15) | no |
| `changelog` | one bullet under `## Unreleased` ending with the ticket id (tickets 1 to 32) | no |
| `changelog2` | the bullet starts with the ticket id in brackets (from ticket 33) | no |

The written record is 260 Slack messages, 10 Notion pages and 6 pull request threads. Most of it is deploys, on-call and lunch. Each rule is planted differently: stated clearly, stated on a stale page, argued over by two people, announced the evening before a change, or written nowhere (`tests`, `sorted`, `idempotent`). One ticket happens per day, and the agent's `../company/` folder holds only what was dated before that day. `python -m clbench.knowledge` checks the planted evidence against `knowledge/evidence.json`.

### `helpdesk`: a customer support desk

Marlowe & Pine, an online home-goods retailer. The agent resolves one customer case per task: it looks up the customer and order, acts through a `desk.py` command-line tool that logs every action, and writes a reply. The workspace has reply templates and past cases handled the old way. 18 cases, 8 rules, one policy change.

| rule | what it says | hidden |
|---|---|---|
| `escalate` | refunds above $75 go to `billing-review`, never paid directly (cases 1 to 9) | yes |
| `escalate_finance` | refunds above $40 go to `finance-ops` (from case 10) | yes |
| `tag` | every case gets exactly one tag from a fixed set | yes |
| `no_dates` | replies never say when a parcel will arrive | yes |
| `signoff` | replies end with a fixed two-line sign-off | yes |
| `credit_cap` | goodwill credit is capped at $15 per case | no |
| `identity` | verify the customer before changing an account email | no |
| `greeting` | greet customers in their account's language | no |

This pack has no knowledge folder yet.

### Learners

`clbench/learners.py` defines a learner as a state dict and two functions, `context` and `observe`.

| arm | what carries over between tasks |
|---|---|
| `none` | nothing. The stateless baseline. |
| `placebo` | a fixed block of true facts that contains no rule. Controls for "any extra context helps". |
| `history` | the raw feedback text from every earlier task. |
| `notes` | notes the agent rewrites after each task from its diff and the feedback. Capped at 3000 characters. |
| `memdir` | a folder the agent owns. It can read and write it during the task, and gets a turn to update it after feedback. The harness does not look inside. |
| `oracle` | the team handbook. The ceiling. |

`memdir` is the slot for a lab's own memory system: the agent gets durable storage and the raw feedback, and the rest is up to it. A weight-update learner fits the same two functions. This repo has not run one.

### Feedback modes

- `rich`: pass or fail, failing check names, and the reviewer's comment for each broken rule.
- `lenient`: the same reviewer, but they miss about half of the broken rules. An approval no longer proves the work was right.
- `sparse`: pass or fail and "changes requested" or "approved". No explanation.

### Company knowledge

`--knowledge available` tells the agent the `../company/` folder exists. `--knowledge directed` also tells it to search the folder before it starts. Arms that use the folder carry `+org` or `+org-directed` in their name.

### Agents

- `claude:<model>` runs the headless `claude` CLI with user settings, plugins and memory switched off. Shell access is limited to an allowlist (Python, pytest, and read-only tools such as `ls` and `grep`).
- `openai:<model>@<base url>` runs a small built-in agent loop against any OpenAI-compatible endpoint. It uses a plain-text action protocol, so it works with models that have no tool calling. It runs whatever shell command the model writes, inside the temporary workspace.
- `gold` and `noop` run without a model.

### Metrics

`python -m clbench.report <run> [<run> ...]` writes `results/<run>/results.md`, a learning curve, and a combined table when given several runs.

- **Compliance**: share of the task's listed rules that the work follows.
- **Hidden-rule compliance**: the same, on hidden rules only.
- **First-try merge**: functional check passed and no rule broken.
- **Gain vs stateless**: mean per-task compliance minus the `none` arm on the same task, with a paired bootstrap 95% interval over tasks.
- **Oracle gap closed**: that gain divided by the oracle's gain.
- **Repeat-violation rate**: after a reviewer has explained a rule once, how often the agent breaks it again.
- **Compliance by exposure**: first time the agent meets a rule, second and third, fourth and later.
- **Rules introduced by a change**: the outcomes in order for each rule that arrived mid-stream.
- **Cost per task**: solve cost plus learning cost, as reported by the CLI.

## Run it

```
uv venv .venv && uv pip install --python .venv/bin/python pytest
.venv/bin/python -m clbench.validate
./run_all.sh my-run claude:haiku
./run_org.sh my-run claude:haiku
.venv/bin/python -m clbench.report my-run
```

`run_all.sh` starts eight arms in parallel and `run_org.sh` starts the three company-knowledge arms. Both need the `claude` CLI on your path and logged in. Each arm appends to `runs/<run>/<arm>/attempts.jsonl` and resumes from there if you rerun it.

One arm, another company, or an open model:

```
CLBENCH_ORG=helpdesk .venv/bin/python -m clbench.run --run-name hd --learner memdir --agent claude:haiku
.venv/bin/python -m clbench.run --run-name gemma --learner notes --agent "openai:google/gemma-4-31B-it@http://localhost:5151/v1"
```

## Detailed results

Per-run tables and curves are in `results/`. The runs are `haiku-v2-s1` and `haiku-v2-s2` (11 arms each), `opus-v2` (4 arms), `gemma-s1` (3 arms), `hd-haiku-s1` and `hd-haiku-s2` (4 arms each), and `hd-opus` (4 arms).

### Coding team, Haiku, two runs per arm

Each cell is the mean of two runs with the lower and higher run in brackets.

| arm | compliance | hidden-rule compliance | first-try merge | repeat-violation rate |
|---|---|---|---|---|
| `none` | 0.38 [0.37, 0.38] | 0.10 [0.10, 0.10] | 0.00 [0.00, 0.00] | 0.67 [0.66, 0.67] |
| `placebo` | 0.26 [0.25, 0.28] | 0.07 [0.07, 0.07] | 0.00 [0.00, 0.00] | 0.75 [0.74, 0.76] |
| `notes`, sparse feedback | 0.49 [0.45, 0.53] | 0.18 [0.14, 0.22] | 0.05 [0.03, 0.07] | 0.55 [0.54, 0.57] |
| `notes`, lenient feedback | 0.82 [0.81, 0.82] | 0.63 [0.62, 0.64] | 0.49 [0.45, 0.53] | 0.18 [0.15, 0.21] |
| `notes`, rich feedback | 0.89 [0.88, 0.89] | 0.82 [0.81, 0.83] | 0.57 [0.57, 0.57] | 0.06 [0.06, 0.07] |
| `memdir`, rich feedback | 0.91 [0.89, 0.94] | 0.86 [0.83, 0.90] | 0.74 [0.65, 0.82] | 0.03 [0.00, 0.05] |
| `history`, rich feedback | 0.92 [0.91, 0.93] | 0.90 [0.90, 0.90] | 0.75 [0.72, 0.78] | 0.01 [0.00, 0.01] |
| `oracle` | 0.99 [0.99, 0.99] | 0.98 [0.98, 0.98] | 0.95 [0.93, 0.97] | 0.00 [0.00, 0.00] |
| `none` + company folder | 0.45 [0.45, 0.46] | 0.22 [0.21, 0.22] | 0.10 [0.10, 0.10] | 0.61 [0.59, 0.63] |
| `none` + told to search it | 0.69 [0.67, 0.72] | 0.37 [0.36, 0.38] | 0.23 [0.23, 0.23] | 0.34 [0.32, 0.37] |
| `notes` + told to search it | 0.90 [0.90, 0.90] | 0.81 [0.81, 0.81] | 0.64 [0.62, 0.65] | 0.08 [0.08, 0.08] |

![learning curve](results/haiku-v2-s1/curve.svg)

- **The explanation is what teaches.** With only "approved" or "changes requested", notes gain 0.11 over stateless. With the reviewer's comment they gain 0.51.
- **A reviewer who misses half the problems costs most on hidden rules.** Overall compliance drops from 0.89 to 0.82. Hidden-rule compliance drops from 0.82 to 0.63.
- **Written knowledge only helps for rules someone wrote down.** With directed search and no memory, the agent follows `settings` (discussed in Slack) 67% of the time and `sorted` (written nowhere) 0% of the time.
- **Access is not use.** With the folder only mentioned, compliance moved from 0.38 to 0.45. Told to search first, the same agent reached 0.69.
- **The placebo arm scored below stateless in both runs.** Extra context that carries no rules did not help. Why it hurt is not established.

### Coding team, Opus and Gemma, one run per arm

| model | arm | compliance | hidden-rule compliance | first-try merge | $ per ticket |
|---|---|---|---|---|---|
| Opus | `none` | 0.59 | 0.07 | 0.10 | 0.15 |
| Opus | `notes` | 0.91 | 0.81 | 0.70 | 0.30 |
| Opus | `memdir` | 0.94 | 0.88 | 0.80 | 0.52 |
| Opus | `oracle` | 0.99 | 1.00 | 0.97 | 0.17 |
| Gemma 31B | `none` | 0.09 | 0.12 | 0.00 | local GPU |
| Gemma 31B | `notes` | 0.76 | 0.76 | 0.30 | local GPU |
| Gemma 31B | `oracle` | 0.84 | 0.88 | 0.47 | local GPU |

- **Stateless Opus never followed four of the six hidden rules.** It scored 0 of 14 on `money` and 0 of 6 on each of `sorted`, `idempotent` and `settings`.
- **Opus reads both mid-stream changes from the code.** With no memory it followed `events` on 12 of 16 tries and the new changelog format on 7 of 8. Haiku with no memory followed them on 2 of 32 and 0 of 16 across its two runs. A rule change that a frontier model cannot read off the workspace is still missing from this pack.
- **Being told the rules is not enough for a weaker model.** Gemma with the full handbook reaches 0.84, and its functional pass rate is 0.88 in every arm.
- **Memory costs money.** For Opus the memory-folder arm costs about three times the handbook arm per ticket, because of the extra update turn.

### Support desk

| model | arm | compliance | hidden-rule compliance | first-try fully correct |
|---|---|---|---|---|
| Haiku (2 runs) | `none` | 0.31 [0.31, 0.32] | 0.20 [0.19, 0.21] | 0.03 [0.00, 0.06] |
| Haiku (2 runs) | `notes` | 0.79 [0.76, 0.81] | 0.78 [0.77, 0.79] | 0.33 [0.28, 0.39] |
| Haiku (2 runs) | `memdir` | 0.87 [0.87, 0.87] | 0.90 [0.90, 0.90] | 0.64 [0.61, 0.67] |
| Haiku (2 runs) | `oracle` | 0.97 [0.94, 1.00] | 0.98 [0.96, 1.00] | 0.92 [0.89, 0.94] |
| Opus (1 run) | `none` | 0.24 | 0.12 | 0.00 |
| Opus (1 run) | `notes` | 0.83 | 0.83 | 0.56 |
| Opus (1 run) | `memdir` | 0.89 | 0.90 | 0.78 |
| Opus (1 run) | `oracle` | 1.00 | 1.00 | 1.00 |

- **The policy change is hidden from both models.** With no memory, Opus followed the new refund threshold on 0 of 5 cases. With notes or a memory folder it missed the first case after the change and followed the next four.
- **Stateless Opus scores below stateless Haiku here.** A capable default is still the wrong default for this company.

### What limits these numbers

- No attempt in any committed run ended with a CLI or endpoint error.
- Functional pass rate is 0.95 or higher for Haiku and Opus on the coding team, so the gaps there come from rule-following. On the support desk it is 0.94 or higher for Opus and 0.67 to 0.94 for Haiku. Most Haiku failures there are cases where the customer was owed goodwill credit and the agent gave none. Why is not established.
- The two Haiku runs differ by 0.05 or less on compliance in every arm except sparse notes (0.08). Two runs give a range, not a confidence interval.
- Hidden rules were chosen from one stateless Opus run per company. Borderline rules moved between two such runs on the support desk: `greeting` scored 0.50 then 0.40 and `credit_cap` 0.60 then 0.40, so both sit on the line.

## Limits

- **Opus and Gemma have one run per arm.** Treat differences smaller than about 0.05 as noise.
- **Two companies, written by a model to a design.** Rules are cleaner than a real team's taste, and the Slack history is small. A real export is thousands of times larger.
- **The reviewer is a script.** `lenient` makes it miss things. It never gives wrong advice, and it never stays silent on an entire task.
- **The workspace does not grow.** Every task starts from a snapshot, so the agent's own earlier work does not persist and the benchmark does not measure error build-up.
- **Some support-desk checks are keyword heuristics.** The `no_dates` check can miss a promise worded without a delivery word, and can flag a sentence about shipping policy.
- **`idempotent` passes by accident for weaker models.** Stateless Haiku and Gemma follow it half the time because they skip the guard that Opus adds.
- **No learner updates weights.** Every arm here changes what is in the prompt or on disk.
- **The agent is not sandboxed beyond a temporary directory.** The hidden checks live outside the workspace, but an agent with shell access could look for them.
- **Task order is fixed.** `--order shuffled` exists and has not been run.
