# Benchmark design methodology: continual learning for coding agents from a single repository's history (state as of November 2026)

Verification legend used on every bullet:
- **[P]** = read from the primary source (paper HTML / official page) in this research session.
- **[S]** = seen only as a search-result snippet or summary of the primary source; the URL is the primary source but the specific number/claim should be re-checked before it is quoted in a report.
- **[2nd]** = secondary source only (blog, aggregator). Treat as unverified.

Year is given for every work so that older work (2017-2025) is distinguishable from 2026 work.

---

## 1. Task mining: turning commits/PRs into executable tasks (fail-to-pass / pass-to-pass), cheap recipes, good repos

### Takeaway
All mainstream pipelines share one validation core: check out the pre-change commit, apply only the PR's test changes, run the tests, apply the code change, run again; keep the task only if at least one test goes FAIL->PASS and previously passing tests still pass, repeated several times to remove flaky tests. The expensive part is environment setup, not mining, and the newest pipelines (SWE-smith 2025, SWE-CI 2026) reduce it by building ONE environment per repo (or per dependency-stable span) instead of one image per task, which is exactly what a single-repo stream benchmark needs.

### Cited Findings

**SWE-rebench (2025, NeurIPS D&B) - PR-based, fully automated**
- Candidate filter: Python, permissive license, issue resolved, PR merged to main, PR not linked to multiple issues, issue text > 10 chars, 1-15 files changed, PR must add/modify tests AND change non-test code. ~450,000 PRs -> ~153,400 candidates -> 21,336 final tasks from 3,468 repos. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Install recipe: an LLM picks up to 10 likely setup files (README, setup.py, requirements...), Qwen2.5-72B-Instruct emits up to three candidate JSON install recipes per task, and revises from error logs on failure. A working recipe was found for at least one task in only 31% of repositories. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Validation: at least one test from the test patch must fail before the solution patch and pass after; tests passing initially must still pass; tests are run multiple times and instances failing in any run are dropped (run count not stated). **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Tasks in a "version group" often share one environment (i.e. not strictly one image per task). **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Automated quality labels (issue clarity, task complexity, test-patch correctness) from a fine-tuned LLM reach only 79% / 81% / 67% accuracy. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- License filter list: MIT, Apache-2.0, BSD 2/3/4-clause, ISC, CC0-1.0, ZPL-2.1; "Other" manually reviewed. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Follow-up SWE-rebench V2 (Feb 2026) is language-agnostic and is the source pool for VibeMemBench. **[S]** - [SWE-rebench V2](https://arxiv.org/abs/2602.23866)

**SWE-bench-Live (2025, Microsoft) - RepoLaunch**
- Repo filter: Python-primary, > 1,000 stars (8,577 repos, Apr 2025) -> > 200 issues+PRs, > 200 forks, >= 60% Python (3,316) -> valid OSS license (2,609). **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- RepoLaunch: ReAct-style setup agent (identify relevant files -> choose base image -> interactive setup -> verify -> commit container). A "time-machine" restricts pip to package versions released no later than the base commit's timestamp, which the paper says "significantly improves setup success rates" (no number given). **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- One dedicated Docker image per task. Validation requires >= 1 FAIL_TO_PASS (FAILED or ERROR before, PASSED after) and consistent results across "multiple" repeated runs. **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- Initial release 1,319 instances / 93 repos from issues created 2024-01-01 to 2025-04-20; monthly updates planned. **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- Difficulty is strongly predicted by patch size and repo size: single-file patches < 5 lines ~48% solved; >= 3 files or > 100 lines < 10%; >= 7 files 0%. Repos with < 100 files and < 20k LOC often exceed 20% success; repos with > 500 files rarely exceed 5%. **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- The paper notes SWE-Gym's environment setup "required over 200 hours of manual effort." **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)

**SWE-Gym (2024/2025)**
- 2,438 real tasks from PRs in 11 popular Python repos using SWE-bench's instance-extraction script; ~6 TB of environment images. **[S]** - [SWE-Gym](https://arxiv.org/pdf/2412.21139); storage figure **[P]** via [SWE-smith Table 2](https://arxiv.org/html/2504.21798)

**R2E-Gym / SWE-GEN (2025) - commit-based, no issue or PR needed**
- Works from commits: rule + LLM-judge filters with thresholds: <= 5 non-test files modified, <= 100 edited lines in non-test files, patch <= 2000 chars, <= 1 deleted / 3 added / 3 edited entities, <= 10 statement-level changes. **[P]** - [R2E-Gym](https://arxiv.org/html/2504.07164)
- F2P tests come from tests in the commit; if a commit has none, F2P tests are generated with an Agentless-like reproduction-test generator that sees the ground-truth patch. Patch minimization iteratively removes changes while tests still pass. **[P]** - [R2E-Gym](https://arxiv.org/html/2504.07164)
- Issue text is back-translated by an LLM from commit message, code patch, test changes, before/after execution output and assertion failures, with the instruction to describe the bug without revealing the fix. **[P]** - [R2E-Gym](https://arxiv.org/html/2504.07164)
- 8,135 instances total; 4,578 environments across 10 repos with no SWE-bench overlap; ~4 TB. **[P]** - [R2E-Gym](https://arxiv.org/html/2504.07164), [SWE-smith Table 2](https://arxiv.org/html/2504.21798)

**SWE-smith (2025, NeurIPS D&B) - environment-first, one image per repo**
- Inverts SWE-bench: define the execution environment first, then synthesize tasks inside it. One Docker image per repo; 50k tasks / 128 repos in ~295 GB versus an estimated 50-150 TB for SWE-bench-style per-instance images. **[P]** - [SWE-smith](https://arxiv.org/html/2504.21798)
- Env build: SWE-agent installs the repo at its latest commit (<= 100 steps, avg $0.72, ~17 steps); a human checks that > 80% of existing tests pass (3-20 min per repo; ~18 human hours for 128 repos). **[P]** - [SWE-smith](https://arxiv.org/html/2504.21798)
- Task synthesis yields and per-candidate cost: Combine 96.9% / 0c; LM Modify 56.0% / 0.38c; Procedural AST mutation 40.2% / 0c; LM Rewrite 35.0% / 3.93c; PR Mirror (LLM reverts a real PR against the current HEAD) 33.8% / 5.53c. A candidate is kept only if it breaks >= 1 existing passing test; candidates whose test run exceeds two minutes are discarded. **[P]** - [SWE-smith](https://arxiv.org/html/2504.21798)
- Issue text generated by LLM from the diff, a random F2P test's source and test output (~2.54c per issue). Total build cost ~$1,360 and ~20 h of human labor. **[P]** - [SWE-smith](https://arxiv.org/html/2504.21798)
- Repo selection: top 5,000 PyPI packages by downloads, >= 1,000 GitHub stars, minus the 12 SWE-bench repos, permissive licenses. Example repos: pallets/flask, pallets/click, pydantic/pydantic, getmoto/moto, facebookresearch/hydra, dask/dask, python/mypy, tornadoweb/tornado, encode/starlette, scrapy/scrapy, iterative/dvc, pandas-dev/pandas. **[P]** - [SWE-smith](https://arxiv.org/html/2504.21798)

**SWE-CI (2026) - long spans of one repo's history**
- Task = (base commit, target commit) on main of one Python repo; 100 tasks / 68 repos; average span 233 days and 71 consecutive commits; >= 500 changed non-test source lines. Candidate spans are chosen where dependencies are unchanged, so one environment serves the whole span. **[P]** - [SWE-CI](https://arxiv.org/html/2603.03823v4)
- Repo filter: >= 3 years active maintenance, > 500 stars, config/dependency files, unit test suite, permissive license (4,923 repos pass). Dockerfile generated from the oracle (target) commit with a self-repair step for missing deps. Kept only if oracle tests run and base vs oracle differ by >= 5 passing tests. Tests run with pytest + pytest-json-report, 3600 s timeout. **[P]** - [SWE-CI](https://arxiv.org/html/2603.03823v4)

**Commit0 (2024, ICLR 2025)** - 54 Python libraries; agent gets an API spec and the unit-test suite and must fill in a starter repo with emptied function bodies; interactive test feedback helps. Not a mining recipe but a precedent for "whole test suite as the oracle." **[S]** - [Commit0](https://arxiv.org/html/2412.01769v1)

**NoCode-bench (2025)** - 634 feature-addition tasks across 10 projects; each task is a real feature documented in release notes; input is the documentation diff, verified by developer-written tests; 114-instance human-verified subset. Shows feature tasks can be mined from doc changes rather than issues. **[S]** - [NoCode-bench](https://arxiv.org/html/2507.18130v3)

**Precedents for small, cheap, single-repo streams**
- CL-Bench (2026) "Codebase Adaptation" uses just two small permissively licensed repos, jazzband/tablib (MIT) and jd/tenacity (Apache-2.0): 19 issues (9 + 10). Filters: problem statement >= 600 chars, patch 8-300 changed lines, test patch >= 4 changed lines, no doc-only/test-only issues; then "the most recent contiguous chronological window that is temporally coherent" (total span <= 365 days, max gap 120 days between consecutive issues). **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-Bench-CL (2025) reuses SWE-bench Verified: 8 repos, 273 tasks, sequences of 19-50 tasks (django 50, sympy 50, sphinx 44, matplotlib 34, scikit-learn 32, astropy 22, xarray 22, pytest 19), ordered by creation time and then re-ordered easy-to-hard; dependencies between tasks approximated by overlapping files in gold patches. **[P]** - [SWE-Bench-CL](https://ar5iv.labs.arxiv.org/html/2507.00014)

**Test quality warnings that apply to any mined task**
- OpenAI (Feb 2026) stopped reporting SWE-bench Verified: in an audited 27.6% subset of frequently failed problems, at least 59.4% had test cases that reject functionally correct submissions; the set is also described as increasingly contaminated. **[S]** - [OpenAI: Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- SWE-ContextBench (2026) reports an average of 4.8 FAIL_TO_PASS and 211.5 PASS_TO_PASS tests per task, a useful reference for what "normal" looks like. **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)

### Inferences (recommended recipe for the prototype; not directly sourced)
- **Cheapest reliable recipe, no Docker-per-task** (synthesis of SWE-smith's one-env-per-repo, SWE-CI's dependency-stable spans, and SWE-bench-Live's time-machine):
  1. Pick a window of history in which the dependency files (pyproject/setup.cfg/requirements) do not change, or change only trivially. Build ONE venv (uv or pip) at the window's last commit, with packages pinned to versions released on or before that date. Install the repo in editable mode so the venv follows whichever worktree is on `sys.path` (or set `PYTHONPATH` per worktree; editable installs point at one path, so the per-worktree `PYTHONPATH`/`pip install -e` step needs testing for src-layout and C-extension repos).
  2. For each merged PR (or first-parent merge/squash commit) in the window: `base = parent`, split the diff into test files vs non-test files. Keep if it changes both, <= ~5 non-test files and <= ~100-300 changed lines (R2E-Gym / CL-Bench thresholds).
  3. `git worktree add` at `base`; apply test patch only; run the touched test files with `pytest --json-report` N times (3-5); apply code patch; run again N times. F2P = tests failing/erroring in all pre runs and passing in all post runs; P2P = tests passing in all runs on both sides. Drop the task if F2P is empty or anything is inconsistent.
  4. Also run the whole suite at `base` once to find already-failing tests and exclude them from P2P.
  5. Task statement: linked issue text if it exists and is long enough; otherwise R2E-Gym-style back-translation from commit message + failing test output, with a leak check that it does not contain the fix.
- A single repo with a stable dependency set is the case where one-venv-plus-worktrees is safe. The risk is commits that change dependencies or build steps mid-stream; split the stream into environment epochs when that happens (inference from SWE-CI's dependency-unchanged criterion).
- A two-minute per-task test budget (SWE-smith) is a sensible admission rule because every task is run many times across seeds and conditions.
- Prefer small repos: SWE-bench-Live's data says success collapses on > 500-file repos, and a learning benchmark needs baseline success in the middle (roughly 30-70%) so both gains and losses are visible (VibeMemBench's ceiling problem, section 2).
- Candidate repo shortlist, by evidence strength: tablib and tenacity (already used for exactly this purpose by CL-Bench); click, flask, starlette, tornado, pydantic, hydra, moto, dvc (SWE-smith environments exist and pass the > 80% tests check). All would still need local measurement of suite runtime and of the count of small test-backed PRs.
- Because gold tests can reject correct patches (OpenAI audit), budget a manual review of every F2P test for a stream of 50-150 tasks; at this size full human review is feasible and is the main quality advantage a small single-repo benchmark has over 20k-task automated sets.

### Gaps
- No source found that documents or benchmarks the specific "one venv + git worktree per task" recipe; it is an inference from per-repo-image pipelines. Isolation risks (shared `.pytest_cache`, compiled extensions, editable-install path, tests that write to the home directory or network) are untested here.
- No primary source gives a ranked list of Python repos by "fast test suite + many small test-backed PRs." The R2E-Gym repo list is in an image table and was not extracted; SWE-Gym's 11 repo names were not verified.
- Number of repeated validation runs is not stated by SWE-rebench or SWE-bench-Live.
- NoCode-bench and Commit0 details are from search snippets only.
- Reports that SWE-bench Pro also has a ~30% broken-task rate and that OpenAI withdrew its recommendation of it in July 2026 appeared only in secondary/third-party text; not verified from a primary source.

---

## 2. Learning-specific validity: separating learning from leakage, difficulty drift, contamination, and context growth

### Takeaway
The only widely adopted control is a matched stateless (memory-off) run of the same agent on the same tasks; shuffled-order, irrelevant-memory, oracle-memory and frozen-probe controls each appear in at most one or two 2026 papers, and no single benchmark combines them. Existing results also show the effects are small relative to noise (VibeMemBench: all five memory gains have bootstrap intervals crossing zero), so the controls and the headroom of the task set matter more than the choice of memory system.

### Cited Findings

**Stateless / no-memory baseline (difficulty-drift control)**
- CL-Bench (2026) defines learning as the paired difference between a stateful and a stateless run of the same system on the same instance: g_t = r_t^sf - r_t^sl, and normalizes by the system's own headroom: g_hat = (mean r^sf - mean r^sl) / (r_max - mean r^sl). Stateless baselines are order-independent by construction. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- VibeMemBench (2026): each target-seed pair runs under a fixed agent configuration (model, prompt, tools, sandbox, budget); only the memory condition changes. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)
- SWE-Bench-CL (2025) defines forward transfer against a zero-shot score per task (a_{i,i+1} - a_{0,i+1}) but reports no continual-learning results at all ("full empirical evaluation using our agentic framework is ongoing"; harness pass rates "generally below 8.5%"), and deliberately re-orders tasks easy-to-hard, which confounds position with difficulty. **[P]** - [SWE-Bench-CL](https://ar5iv.labs.arxiv.org/html/2507.00014)

**Order controls**
- CL-Bench averages each task over 5 rollouts, resampled "by permuting the instance order within each variant"; it does not describe a shuffled-order baseline as a separate condition, nor oracle or context-growth controls. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-bench-Live found no clear trend of resolved rate against issue creation quarter (2024Q1-2025Q1) for a stateless agent, i.e. chronological position alone need not produce drift, but this is across 93 repos, not within one. **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)

**Context-growth / "any extra text" control**
- VibeMemBench's irrelevant-memory control (a fixed everyday-text distractor injected in place of the memory record) scored 0.7 to 3.4 points BELOW memory-off on all three solvers. Its strip ablation found that removing flagged instruction lines and removing an equal number of random lines both recover performance, which the authors read as harm from transcript volume rather than content. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)
- SWE-ContextBench (2026): full trajectories average 25,633.7 tokens vs 217.1 for summaries; free retrieval of full trajectories gave 26.26% = baseline 26.26% while raising cost to $0.98 vs $0.79 per instance; "naive context learning can increase cost without improving accuracy." **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)
- CL-Bench: plain full-context ICL (Claude Sonnet 4.6) had the top normalized gain, 25.4 +/- 3.6%, ahead of dedicated memory systems (ACE 8.6 +/- 2.5% at the highest cost, $62.8); "naive ICL outperforms systems dedicated to memory management." So context accumulation is itself a strong baseline that must be reported. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)

**Oracle-memory upper bound**
- SWE-ContextBench compares No-Context, Free Context, Oracle Context, Free Summary, Oracle Summary: 26.26 / 26.26 / 27.27 / 22.22 / 34.34% resolved on 99 related Python tasks (Claude Sonnet 4.5). Oracle summary beats free summary by 12.12 points; so the gap between retrieval-as-is and oracle selection is larger than the gap between memory and no memory. **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)
- VibeMemBench's "frozen verified experience" (one distilled lesson per target, selected in a reference setting with one model and transferred unchanged to five other solvers) is an oracle-like upper bound: gains 0.0 to +4.5 points, all intervals crossing zero. Existing memory systems (Mem0, SimpleMem, MemoryOS, A-MEM): 11 of 12 solver-system pairings at or below baseline. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)

**Solution-leakage controls**
- VibeMemBench SIEVE pipeline: only earlier same-repository history is admitted; target identifiers are excluded; the target gold patch is used only in an offline screen; the test patch is evaluator-only; neither reaches experience distillation, retrieval, or solver context; the distillation prompt never sees the target's test outcome. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)
- SWE-Bench-CL measured cross-task patch similarity as a leakage proxy: mean Jaccard of patch token sets 0.1114, mean TF-IDF cosine 0.1792, only one pair above cosine 0.4. **[P]** - [SWE-Bench-CL](https://ar5iv.labs.arxiv.org/html/2507.00014)
- SWE-ContextBench builds "related task" pairs from real issue/PR cross-references (six relationship types; 376 related tasks over 1,100 base tasks, 51 repos), i.e. it selects for tasks where prior work is legitimately reusable. **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)

**Headroom / ceiling**
- CL-Bench admission criteria for a task: headroom, shared latent structure, and a learning mechanism (feedback that makes early experience useful later). It argues chained standard benchmark instances are "diverse and independent" and therefore poor for measuring learning. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- VibeMemBench attributes much of its null result to ceiling effects (where memory-off already resolves all four seeds, memory can only lose seeds) and retained targets only if some injected experience improved pass rate in a reference setting; the authors note this selection makes it a test of transferable experience rather than a deployment-frequency estimate. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)
- "Skill Issue" (2026) reports that on one repository benchmark a Claude Code + Sonnet 4.5 harness reaches 100% on the first repository with no skill at all, leaving no room to measure repo-specific knowledge. **[S]** - [Skill Issue](https://arxiv.org/pdf/2609.12742)
- CL-Bench criticizes SWE-Bench-CL as "coding-only and not evaluated with frontier systems due to a saturated binary accuracy metric," and for its coding task replaces binary success with an efficiency reward r = 1 - (steps_to_solve - 1)/max_steps (max_steps = 40; unsolved = 0). **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)

**Pretraining contamination**
- "The SWE-Bench Illusion" (2025): models identify the buggy file path from the issue text alone, without repo access, with up to 76% accuracy on SWE-bench Verified versus up to 53% on repos outside SWE-bench, and ~10 points lower on other tasks from the same repos not in Verified. This file-path probe is a cheap contamination diagnostic. **[S]** - [The SWE-Bench Illusion](https://arxiv.org/abs/2506.12286)
- SWE-rebench marks on its leaderboard any evaluation that includes issues created before the model's release date, and compares models on January-2025 vs March-April-2025 tasks to detect inflation. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- Same agent (OpenHands + Claude 3.7 Sonnet): 43.20% on SWE-bench Verified vs 19.25% on SWE-bench-Live; and 22.96% on Live tasks from SWE-bench repos vs 18.89% on other repos. **[P]** - [SWE-bench Goes Live!](https://arxiv.org/html/2505.23419v2)
- CL-Bench does not discuss leakage or contamination for its SWE-bench-derived coding task. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)

### Inferences (recommended control set)
- Minimum condition matrix, all with identical model, scaffold, budget and seeds:
  1. **Stateless** (fresh agent per task) - gives per-task difficulty, removes drift from every paired metric.
  2. **Stateful, chronological** - the system under test.
  3. **Stateful, shuffled order** (several permutations) - if the gain is the same as chronological, the agent is learning generic repo facts, not exploiting temporal structure; if stateless scores trend along the stream, that trend is difficulty drift and should be reported separately.
  4. **Context-matched placebo** - same number of tokens of memory, but from a different repo or from irrelevant text (VibeMemBench-style). Separates "useful content" from "more context."
  5. **Oracle memory** - hand-written or gold-derived repo notes (conventions, test commands, architecture), without task solutions. Gives the regret denominator.
  6. Optional **cheating upper bound** - memory may store gold patches; used only to show how much of the gain leakage could explain.
- **Frozen probe set**: hold out K tasks (e.g. 10-20, sampled across the stream's time range, checked at a fixed code snapshot) that are never used for learning and whose feedback is never shown; re-run them with a read-only copy of the memory at checkpoints (after 0, 25, 50, 75, 100% of the stream). Because the tasks are identical at every checkpoint, the probe curve is free of difficulty drift, and it is the agent-world equivalent of the R_{i,j} matrix in GEM. No surveyed coding benchmark does this; it is an inference from classic CL evaluation.
- **Leakage audit**: (a) no task's gold patch or hidden tests are ever written to anything the agent can read later; (b) the agent's worktree at task t is the repo at base commit of t, which already contains the merged human fixes of earlier tasks - this is realistic, but it means later tasks can literally contain earlier solutions, so near-duplicate tasks (reverts, backports, follow-up fixes to the same lines) should be detected by patch-similarity (SWE-Bench-CL's Jaccard/TF-IDF check) and either removed or tagged; (c) scan memory contents for verbatim hunks of gold patches.
- **Contamination**: ideal is a stream window entirely after the evaluated model's cutoff (SWE-rebench marking rule). Where that is impossible, (i) run the Illusion-style file-path probe on the stream's tasks to estimate memorization, (ii) remember that contamination raises BOTH stateless and stateful scores so the paired gain is partly protected, but it shrinks headroom and can make "learning" look absent, (iii) inject synthetic private conventions (section 4) that cannot be in pretraining.
- Report the stateless score's slope along the stream explicitly; a learning claim should be made on the paired difference (stateful - stateless) slope, not on the raw stateful curve.
- Pick tasks so stateless success is neither ~0 nor ~100% per task (multi-seed), or use a graded reward (steps/cost to solve, fraction of F2P tests) to avoid the saturation that made SWE-Bench-CL and VibeMemBench inconclusive.

### Gaps
- No surveyed paper reports a shuffled-order-vs-chronological comparison as an explicit ablation for coding agents; CL-Bench permutes order only for variance reduction.
- No coding-agent benchmark found that uses held-out probe tasks re-evaluated at checkpoints.
- No paper found that quantifies how much of a stateful gain survives when the repo is strictly post-cutoff versus pre-cutoff.
- The Illusion numbers were not re-checked across the paper's four versions.

---

## 3. Metrics and statistics

### Takeaway
Classic CL metrics (ACC, BWT, FWT, forgetting) assume a T x T matrix R of "performance on task j after learning through task i," which a one-pass agent stream does not produce; they only become well-defined if tasks are re-evaluated at checkpoints (probe set) or if a stateless baseline replaces the random-init vector. The 2026 agent benchmarks have converged on paired stateful-minus-stateless gain normalized by headroom (CL-Bench), plus cost reporting on a Pareto frontier (Kapoor et al.), with 4-5 seeds and task-level bootstrap intervals.

### Cited Findings

**Classic definitions**
- GEM (Lopez-Paz and Ranzato, 2017): R_{i,j} = test accuracy on task j after observing the last sample of task i; b_i = accuracy at random initialization. ACC = (1/T) sum_{i=1..T} R_{T,i}; BWT = (1/(T-1)) sum_{i=1..T-1} (R_{T,i} - R_{i,i}); FWT = (1/(T-1)) sum_{i=2..T} (R_{i-1,i} - b_i). "Large negative backward transfer is also known as (catastrophic) forgetting." **[P]** (formulas reconstructed from garbled HTML; consistent with the paper's standard statement) - [GEM](https://ar5iv.labs.arxiv.org/html/1706.08840)
- Diaz-Rodriguez et al. (2018) argue evaluation should cover, beyond forgetting: accuracy over time, backward and forward transfer, memory overhead, computational efficiency, fused into a single score via Multi-Attribute Value Theory. **[P]** (abstract only) - [Don't forget, there is more than forgetting](https://arxiv.org/abs/1810.13166)
- Chaudhry et al. (2018) forgetting measure: per task, best earlier performance minus final performance, averaged over earlier tasks. **[S]** (via survey) - [FLM continual learning survey](https://arxiv.org/pdf/2405.18653)

**Agent adaptations**
- SWE-Bench-CL (2025), with a_{i,j} = success on task j after task i and a_{0,j} zero-shot: ACC = (1/N) sum_j a_{N,j}; F = (1/(N-1)) sum_{j=1..N-1} (max_{k<=j} a_{k,j} - a_{N,j}); FT = (1/(N-1)) sum_{i=1..N-1} (a_{i,i+1} - a_{0,i+1}); BWT = (1/(N-1)) sum_i (a_{N,i} - a_{i,i}); AULC = (1/N) sum_{i=1..N} [(1/i) sum_{k=1..i} a_{k,k}]; tool-use efficiency TUE = median(time | success)/median(time | all); CL-Plasticity = (1/N) sum a_{i,i}; CL-Stability = 1 - F; CL-F1 = harmonic mean. The composite CL-Score has unspecified weights and the metrics were never computed on real runs. **[P]** - [SWE-Bench-CL](https://ar5iv.labs.arxiv.org/html/2507.00014)
- CL-Bench (2026): per-instance gain g_t = r_t^sf - r_t^sl; normalized gain g_hat = (mean r^sf - mean r^sl)/(r_max - mean r^sl); normalized reward r_hat = (mean r^sf - r_external)/(r_max - r_external) with r_external = a fixed stateless reference system. Decomposition: boundary instances B (first instance after a variant/repo switch) vs within-variant W: g_stab = f_B (mean r^sf_B - mean r^sl_B)/(r_max - mean r^sl); g_plas = f_W (mean r^sf_W - mean r^sl_W)/(r_max - mean r^sl); g_hat = g_stab + g_plas. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- CL-Bench coding reward: r = 1 - (steps_to_solve - 1)/max_steps, max_steps = 40, 0 if unsolved; the stated learning opportunity is efficiency (where core logic lives, which test commands work, how maintainers structure fixes). **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-CI (2026): normalized change a(c) = (n(c) - n(c0))/(n(c*) - n(c0)) if n(c) >= n(c0), else (n(c) - n(c0))/n(c0), where n = passing tests, c0 = base, c* = oracle; EvoScore = sum_i gamma^i a(c_i) / sum_i gamma^i with gamma >= 1 weighting later iterations; zero-regression rate = share of samples where no previously passing test ever fails (most models < 0.25). **[P]** - [SWE-CI](https://arxiv.org/html/2603.03823v4)
- Evo-Memory (2025) converts static datasets into sequential streams where the agent must retrieve, adapt and update memory after each interaction; it criticizes StreamBench as mostly measuring factual retention. **[S]** - [Evo-Memory](https://arxiv.org/html/2511.20857v2)

**Cost / time normalization**
- Kapoor et al., "AI Agents That Matter" (2024; TMLR 2025): agent evaluations must be cost-controlled; report accuracy vs cost as a 2D Pareto frontier; simple baselines can Pareto-dominate complex agents; calls for held-out sets and standardized evaluation. **[S]** - [AI Agents That Matter](https://arxiv.org/abs/2407.01502)
- CL-Bench reports dollars alongside gain and notes the Pareto frontier is mostly ICL variants (Gemini 3 Flash ICL: 16.4 +/- 3.8% gain at $7.6). **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-ContextBench reports resolved rate, minutes per task and dollars per instance per condition (e.g. baseline 6.37 min / $0.79; OpenViking 4.20 min / $0.53 at 29.2% resolved). **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)
- VibeMemBench reports solver tokens and steps as secondary metrics (steps fall for all five solvers with verified experience even where accuracy does not move) but does not record memory-side token costs, which it lists as a limitation. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)

**Statistics**
- BetterBench (2024, NeurIPS): of 24 benchmarks assessed against 46 criteria, 14 did not run multiple evaluations of the same model or report significance/uncertainty; 17 lack easy-to-run replication scripts. **[P]** - [BetterBench](https://arxiv.org/html/2411.12990v1)
- Miller, "Adding Error Bars to Evals" (2024): treat questions as samples from a population; report standard errors; use clustered SEs when items are related (cluster adjustment up to 3x in the paper's example); compare systems via per-question paired differences, not unpaired summary statistics. **[S]** - [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640)
- Bowyer, Aitchison and Ivanova (2025) position paper: CLT-based intervals perform poorly with small N and usually underestimate uncertainty; recommends non-CLT frequentist or Bayesian alternatives. **[S]** - [Don't use the CLT in LLM evals with less than a few hundred datapoints](https://arxiv.org/pdf/2503.01747)
- VibeMemBench: 4 seeds per condition (444 target-seed runs per solver); target-level percentile bootstrap with 10,000 resamples of the 111 targets, seeds kept intact within target, on paired differences. With N = 111 no gain was separable from zero. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)
- CL-Bench: 5 rollouts per task, 95% CIs from per-task rollout variance. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-rebench: every model run 5 times on the full set; reports SEM and pass@5; fixed ReAct scaffold. **[P]** - [SWE-rebench](https://arxiv.org/html/2505.20411v2)
- A third-party `errorbars` package implements paired comparison, cluster-robust paired SE and exact McNemar. **[2nd]** - [errorbars on PyPI](https://pypi.org/project/errorbars/)

### Inferences (recommended metric set, with formulas)
Notation: stream of N tasks t = 1..N; S seeds; y_{t,s}^c in {0,1} (or graded reward in [0,1]) for condition c in {SL = stateless, SF = stateful, OR = oracle memory, PL = placebo}; cost_{t,s}^c in tokens, turns, seconds, dollars. Bars denote seed means.
- **Paired gain curve**: g_t = ybar_t^SF - ybar_t^SL. **Mean gain** G = (1/N) sum_t g_t. **Normalized gain** (CL-Bench): G / (1 - mean ybar^SL).
- **Learning-curve area**: AULC_gain = (1/N) sum_{t=1..N} [(1/t) sum_{k<=t} g_k] (SWE-Bench-CL's AULC applied to the paired gain rather than raw success, which removes difficulty drift). Also report the **learning slope**: coefficient beta on position in a regression of g_t on t/N, or simply late-half mean gain minus early-half mean gain.
- **Forward transfer** (agent form): FT = (1/(N-1)) sum_{t=2..N} (ybar_t^SF - ybar_t^SL), i.e. GEM's FWT with the stateless agent replacing the random-init vector b. This equals G excluding task 1.
- **Backward transfer / forgetting** (requires re-evaluation): with probe set P evaluated at checkpoints c_0 < ... < c_K using a frozen copy of memory M_{c}, define R_{k,p} = success on probe p with memory after c_k. BWT_probe = (1/|P|) sum_p (R_{K,p} - max_{k<K} R_{k,p}) is Chaudhry-style forgetting (negated); R_{K,p} - R_{0,p} is net probe gain. Alternatively re-run the first quarter of the stream at the end with final memory: BWT = mean_t (y_t^{SF,final memory} - y_t^{SF,original}). If the memory may contain task t's own trace, a positive BWT is mostly leakage and must be reported as "replay success," not learning.
- **Regret vs oracle**: Regret = sum_t (ybar_t^OR - ybar_t^SF); **fraction of oracle gain captured** = sum_t (ybar_t^SF - ybar_t^SL) / sum_t (ybar_t^OR - ybar_t^SL). SWE-ContextBench's oracle-vs-free gap (34.34 vs 22.22) is the existing empirical analogue.
- **Efficiency**: cost per solved task = sum cost / sum solved, per condition, for tokens, turns, wall-clock, dollars, INCLUDING memory read/write/consolidation cost (VibeMemBench's stated omission). Report the ratio SF/SL on the subset of tasks solved in both conditions (paired, avoids survivorship from solving different tasks), and plot success vs dollars per condition (Kapoor-style Pareto). CL-Bench's step-discounted reward is a compact alternative when success saturates.
- **Stability vs plasticity**: if the stream has natural boundaries (major refactor, subsystem switch, convention change), apply CL-Bench's boundary/within decomposition.
- **Regression safety**: SWE-CI's zero-regression rate carries over directly (share of tasks with all P2P tests still passing).
- **Statistics for small N (50-150 tasks)**:
  - Unit of analysis is the task, not the run. Use >= 4-5 seeds per task per condition (VibeMemBench, CL-Bench, SWE-rebench practice) and bootstrap over tasks with seeds kept inside the task (cluster bootstrap), 10,000 resamples, on the paired difference.
  - For binary single-seed comparisons use exact McNemar on discordant pairs; for multi-seed use the task-clustered paired bootstrap or a mixed-effects logistic model: logit P(y=1) = b0 + b1*stateful + b2*position + b3*stateful x position + (1|task) + (1|seed). b3 is the learning-rate claim; the task random intercept absorbs difficulty.
  - In a stateful stream, seeds are whole-stream rollouts: outcomes within one rollout are dependent (memory carries over), so the independent replicate is the rollout. Report between-rollout variance and never treat N x S outcomes as independent. (This follows from Miller's clustering argument; not stated by any CL paper surveyed.)
  - Power check: VibeMemBench could not separate +4.5 points from zero with 111 targets x 4 seeds. A prototype with ~100 tasks should expect to detect only effects of roughly 8-10 points or more, or should use graded/efficiency rewards with lower variance.
  - Pre-register the primary metric (suggest: normalized paired gain and late-minus-early gain) to avoid choosing among the many CL metrics after the fact; BetterBench shows significance reporting is the most commonly missing element.

### Gaps
- Exact formulas of Diaz-Rodriguez et al. (accuracy over the lower-triangular matrix, REM / BWT+, CL-score weights) and of Chaudhry et al. were not read from the primary PDFs in this session; only the abstract and a secondary description were verified.
- No surveyed paper applies mixed-effects models or McNemar to continual-learning agent streams; those recommendations are inferences from general evaluation statistics.
- "AI Agents That Matter" and Miller's paper were confirmed via search summaries, not full-text reads.
- No published definition of "regret vs oracle" for coding-agent memory was found; the formula above is proposed.

---

## 4. Org-specific, tacit knowledge: does an agent pick up undocumented conventions?

### Takeaway
No public benchmark was found that tests whether a coding agent *infers* undocumented, organization-specific conventions over a stream of work and verifies it by execution. The nearest pieces are: synthetic rule-injection through dialogue (MemoryCode, 2025), documented-rule compliance (RepoComplianceBench, 2026), context-file ablations (AGENTS.md studies, 2026), private-codebase evaluation (Real-SWE, 2026, secondary source only), and review-comment-derived tests (c-CRAB, ReviewBench). This is the clearest open niche for the prototype.

### Cited Findings
- MemoryCode (2025, ACL): synthetic multi-session mentor-mentee dialogues in which coding rules are given, mixed with office small talk, and sometimes updated later (only the last update counts). Seeds (instructions, fillers, personas) are expanded by an LLM (Command R+). Models follow single instructions well but degrade when instructions are spread across sessions, including GPT-4o. Conventions are explicitly stated, not inferred. **[S]** - [From Tools to Teammates](https://arxiv.org/html/2502.13791v2)
- CL-Bench (2026) names the latent structure for its coding task as where core logic lives, which test commands are reliable, and "how maintainers structure fixes," but scores only steps-to-solve; it does not verify that conventions were learned. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- Gloaguen et al. (2026), "Evaluating AGENTS.md": LLM-generated context files tended to reduce success vs no context and raised inference cost by over 20% (v1); a later version softens this to "no significant improvement"; developer-written files also increase steps and cost; agents do follow the instructions (e.g. run more tests). **[S]** - [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988)
- RepoComplianceBench (2026): 106 issues from 49 repos that have explicit AI-contribution rules; finding: resolving the issue does not imply resolving it by the rules. Rules are documented, not tacit. **[S]** - [Coding Agents' Compliance with AI Contribution Rules](https://arxiv.org/html/2607.26819v1)
- Legacy-modernization case study (2026): the agent handled explicit rules but missed implicit ones hidden in optional query parameters, dynamic configuration values and form-level conditions. **[S]** - [Legacy System Modernization with Coding Agents](https://arxiv.org/pdf/2608.28972)
- ReviewBench (LangChain): code-review evals built from trusted reviewers' comments on merged PRs; many comments depended on codebase-specific standards that must be reconstructed from surrounding code. **[S]** - [ReviewBench](https://www.langchain.com/blog/evaluating-code-review-agents-with-reviewbench)
- Real-SWE (Specific Labs, Sept 2026): reported to evaluate on private production codebases licensed from companies, targeting company conventions and undocumented dependencies; small (ten tasks) and not reproducible externally. **[2nd]** - [blog summary](https://promactinfo.com/blogs/the-388-ceiling-what-real-swes-private-codebase-benchmark-means-for-how-you-evaluate-ai-coding-agents/)
- agent-rules-bench (GitHub project): identical repo copies with and without convention statements; early claim that without them every run broke a convention and cost 35% more. **[2nd/S]** - [agent-rules-bench](https://github.com/clirimajeti/agent-rules-bench)
- Vercel's evaluation guide suggests testing with a rule the codebase follows but does not document, and checking output with and without a convention file. **[S]** - [Vercel guide](https://vercel.com/i/evaluating-ai-coding-agents)
- A 2026 source-code taxonomy of coding agents reports that agents without persistent memory treat every task as independent; AGENTS.md/CLAUDE.md are static configuration rather than learned knowledge. **[S]** - [Inside the Scaffold](https://arxiv.org/pdf/2604.03515)

### Inferences (how to inject and verify conventions in the prototype)
- **Injection by repo transformation** (the only contamination-proof route): fork the chosen repo and apply a deterministic, history-wide rewrite that introduces private conventions absent from the public project, replayed onto every commit so the whole stream is consistent. Examples that are mechanically checkable:
  - a renamed internal helper that must be used instead of a stdlib call (e.g. all time access through `core.clock.now()`),
  - an error-handling rule (raise project-specific exception subclasses; never bare `ValueError`),
  - a naming or layout rule (test files mirror module path; private modules prefixed),
  - a changelog/fragment rule (every behavior change adds a fragment file),
  - a deprecated internal API that changes mid-stream (tests both learning and un-learning, like MemoryCode's rule updates and CL-Bench's schema migration).
- **Never document the conventions** in README/CONTRIBUTING/AGENTS.md in the main condition; they are observable only in surrounding code and in post-task feedback. Add an "oracle" condition where they are documented (gives the upper bound and reproduces the AGENTS.md-ablation design).
- **Verification**: one hidden checker per convention (AST/lint rule or a hidden test) reported as a separate "convention compliance rate," scored on every task where the convention is applicable, independently of functional F2P success. RepoComplianceBench's finding (functional success != rule compliance) is the argument for scoring them separately.
- **Learning signal**: compliance rate as a function of the number of prior exposures to that convention (exposure = task where it applied and feedback mentioned it). A stateless agent gives the "inferable from local context" floor; the stateful-minus-stateless compliance gap is the cleanest learning measure in the whole benchmark because it cannot come from pretraining.
- Keep real, naturally occurring conventions as a second, weaker track: mine them from the repo's actual review comments (ReviewBench-style) and from linters/config the maintainers enforce; these are realistic but may be in pretraining.

### Gaps
- No primary source found for a benchmark that injects synthetic conventions into a real repo's history and scores acquisition over a stream; the injection design above is a proposal, not an established method.
- Real-SWE details come from a single secondary blog; the original report was not located.
- The AGENTS.md results differ between paper versions (v1 "reduces success" vs later "no significant improvement"); cite the specific version.
- Reviewer-preference learning (an agent adapting to one reviewer's taste across PRs) was not found as an evaluated benchmark.

---

## 5. Feedback realism: deployment-like feedback after each task rather than the gold patch

### Takeaway
Existing designs give either no explicit post-task feedback (CL-Bench coding task does not state any), test-failure reports inside an iterative loop (SWE-CI, Commit0), or review comments in a single revision pass (c-CRAB). No surveyed benchmark gives a stream agent the realistic triple of CI result, reviewer comment, and the human's merged diff, and compares learning across those feedback levels; feedback level should therefore be an explicit experimental factor.

### Cited Findings
- CL-Bench (2026) requires every task to have "a feedback loop" (test failures, error messages, intermediate predictions) as an admission criterion, and one task (Cohort Studies) deliberately gives no score feedback between instances. For Codebase Adaptation each issue runs in a fresh Docker container at the base commit and the patch is "evaluated against hidden regression tests"; the paper does not state whether results or the gold patch are shown to the agent afterward. **[P]** - [CL-Bench](https://arxiv.org/html/2606.05661v1)
- SWE-CI (2026): up to 20 CI iterations; an Architect agent reads failing-test reports (vs the oracle's tests) and writes at most five prioritized high-level requirements; a Programmer agent implements them. Feedback is therefore test-report-derived natural-language requirements, never the oracle code. **[P]** - [SWE-CI](https://arxiv.org/html/2603.03823v4)
- Commit0 (2024): agents receive the unit tests interactively; the paper reports interactive test feedback helps. **[S]** - [Commit0](https://arxiv.org/html/2412.01769v1)
- c-CRAB (2026): review tools produce comments on a PR; a separate coding agent revises the patch; success = passing executable tests derived from the original human reviews. Single revision pass. **[S]** - [Code Review Agent Benchmark](https://arxiv.org/html/2603.23448v1)
- A 2026 code-review benchmark draws verified bugs from human comments before and after merge; best agent catches 79.6% of pre-merge and 64.2% of post-merge human-found bugs within top-5 comments, a data point on how informative simulated reviewer comments can be. **[S]** - [Benchmarking Code Review Agents on Bug Detection](https://arxiv.org/html/2610.13668v1)
- SWE-ContextBench (2026) stores the agent's own unfiltered trajectories (which "may contain incorrect or partial trajectories") as the experience pool, i.e. self-generated experience without correctness labels; this did not improve accuracy unless an oracle selected and summarized it. **[P]** - [SWE-ContextBench](https://arxiv.org/html/2602.08316v3)
- VibeMemBench (2026) uses pre-computed distilled lessons ("bug class, root cause, fix pattern, reusable lesson") from completed history trajectories; retrieval is pre-trajectory, not online, which the authors list as a limitation. **[P]** - [VibeMemBench](https://arxiv.org/html/2609.23570v1)

### Inferences (recommended feedback ladder)
- Treat feedback as a factor with nested levels, each a separate stateful condition:
  - **F0 none**: agent keeps only its own trajectory (SWE-ContextBench-style self-experience).
  - **F1 CI status**: pass/fail plus names of failing hidden tests and truncated assertion messages (not test source). This is what a real CI shows.
  - **F2 CI + reviewer comment**: an LLM "reviewer" that sees the agent's diff, the gold diff and the convention checkers' output, and writes 1-3 comments in maintainer voice without quoting the gold patch (enforce with an n-gram overlap filter against the gold diff). Where the real PR has review comments, use those.
  - **F3 merged diff**: after the task, the repo advances to the next base commit, which contains the human's merged change. Tell the agent which commit resolved the previous task so it can `git show` it. This is the most realistic strong signal and is free because the stream already advances the repo.
  - **F4 gold patch + tests shown explicitly** (unrealistic upper bound).
- F3 is realistic but is also the main leakage channel for near-duplicate tasks (section 2); pair it with the duplicate filter and the frozen probe set.
- Between tasks, give the agent a bounded "reflection" turn with a token budget to update memory, and count its cost in the efficiency metrics (Kapoor et al.; VibeMemBench's missing memory-side cost).
- One real attempt per task, feedback after submission, no retries - otherwise the benchmark measures within-task iteration (SWE-CI's subject) rather than cross-task learning. A retry-allowed variant can be reported separately.
- A simulated reviewer adds an LLM-in-the-loop source of variance and possible leakage; fix the reviewer model, temperature and prompt, cache its outputs per (task, agent diff hash), and validate a sample by hand.

### Gaps
- No surveyed benchmark compares learning under different feedback levels (CI-only vs reviewer vs merged diff); the ladder is a proposal.
- No validated method was found for simulating reviewer comments that are informative without leaking the gold patch; c-CRAB and ReviewBench details are from snippets only.
- Whether CL-Bench shows the agent hidden-test results after each coding instance could not be determined from the paper text read (appendices B-D partially unread).

---

## Cross-cutting summary of the nearest prior benchmarks (for the report writer)

| Work (year) | Stream unit | Learning measure | Controls present | Main weakness for our purpose | Source |
|---|---|---|---|---|---|
| SWE-Bench-CL (2025) | 8 repos, 19-50 Verified tasks each, chronological then easy-to-hard | ACC, F, FT, BWT, AULC, CL-F1 (defined, not measured) | zero-shot baseline in FT definition | No real CL results; curriculum confounds order; Verified is contaminated and saturated | [P] [link](https://ar5iv.labs.arxiv.org/html/2507.00014) |
| CL-Bench Codebase Adaptation (2026) | 19 issues, tablib then tenacity | Stateful - stateless, headroom-normalized; step-discounted reward | stateless; 5 order-permuted rollouts | Tiny N; no leakage/contamination discussion; feedback unspecified | [P] [link](https://arxiv.org/html/2606.05661v1) |
| SWE-ContextBench (2026) | 99-376 "related" tasks with a pool of prior trajectories | resolved, time, cost per condition | no-context, free vs oracle, 4 memory systems | Not a stream; one seed apparent; no human validation of related tasks | [P] [link](https://arxiv.org/html/2602.08316v3) |
| VibeMemBench (2026) | 111 targets + 3,634 earlier same-repo trajectories, 90 repos | memory-on - memory-off resolved, steps, tokens | memory-off, irrelevant-memory, frozen verified experience, 4 seeds, task bootstrap | Pre-trajectory retrieval, not online; ceiling effects; all gains n.s. | [P] [link](https://arxiv.org/html/2609.23570v1) |
| SWE-CI (2026) | 100 base->target spans (avg 233 days, 71 commits) | EvoScore, zero-regression rate | - | Within-task iteration, not cross-task learning | [P] [link](https://arxiv.org/html/2603.03823v4) |
| MemoryCode (2025) | synthetic multi-session dialogues with coding rules | rule-following accuracy vs history length | single instruction vs session vs full history | Rules stated explicitly; no real repo or execution of repo tests | [S] [link](https://arxiv.org/html/2502.13791v2) |
