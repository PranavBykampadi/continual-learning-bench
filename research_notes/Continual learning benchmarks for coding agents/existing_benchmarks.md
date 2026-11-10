# Existing benchmarks for continual / lifelong / online learning in LLM coding agents (as of November 2026)

Verification legend used throughout:
- **[P-full]** = I read the primary paper's full HTML text (via an automated page reader, so individual table cells should be spot-checked before quoting in print).
- **[P-abs]** = I read only the primary arXiv abstract page; details beyond the abstract are not verified.
- **[S]** = only a search-result snippet or secondary source; treat as unverified.

## 1. What are the named benchmarks (and 2026 successors), and what does each actually measure?

### Takeaway
Only a handful of benchmarks actually score a coding agent on a sequence with carried state: SWE-Bench-CL (2025, metrics defined but no real results), SWE-ContextBench (2026), CL-Bench's Codebase Adaptation task (2026, only 19 issues), ChainSWE (2026), VibeMemBench and MemDev-Bench (autumn 2026), plus the older StreamBench (2024) and LifelongAgentBench (2025) on SQL/bash/DS-1000. SWE-bench-Live, SWE-rebench, SWE-Gym, CodeARC, SWE-CI and SlopCodeBench do NOT measure cross-task learning despite sounding adjacent.

### Cited Findings

#### A. Benchmarks that do measure cross-task improvement on coding tasks

**SWE-Bench-CL** (arXiv 2507.00014, June 2025) [P-full]
- Task stream: 273 SWE-Bench Verified tasks in 8 Python repositories, one sequence per repository; per-repo counts 19 (pytest) to 50 (django, sympy); difficulty split 142 easy / 117 medium / 12 hard / 2 very hard — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Ordering: by issue creation timestamp, then "further ordered by difficulty" (easier first, by estimated human fix time); inter-task dependencies approximated by overlap in modified file paths — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Carried state: FAISS vector memory of per-attempt summaries (problem, solution, rationale, tool usage, success flag); top-k retrieved at task start and prepended to the prompt, same-sequence memories prioritized. No weight updates — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Metrics: ACC, Forgetting, Forward Transfer, BWT, AULC, Tool-Use Efficiency, CL-Plasticity, CL-Stability, CL-F-beta, composite CL-Score (formulas in section 4 below) — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Headline results: essentially none for the proposed protocol. The paper states "full empirical evaluation using our agentic framework is ongoing." The only run (CodeLlama-13B, Gemma-3-12B, Mistral-7B, Gemini-2.0-Flash through the SWE-Bench harness) had pass rates "generally below 8.5%", with the memory-enabled condition "on par with or slightly worse"; authors call these results too unreliable to draw conclusions and attribute the null result to memory filled with failed attempts — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Task-similarity analysis: average Jaccard similarity of gold patches 0.1114, TF-IDF cosine 0.1792; only one task pair exceeded cosine 0.4 (i.e. little surface overlap to transfer) — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Stated weaknesses: 8 Python repos, at most 50 issues each; subjective difficulty labels; file-path dependency proxy; strictly chronological sequences with built-in curriculum may not reflect interleaved development; lambda weights of the composite score are unspecified — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Code/data: [github.com/thomasjoshi/agents-never-forget](https://github.com/thomasjoshi/agents-never-forget/)

**SWE-ContextBench** ("SWE Context Bench: A Benchmark for Context Learning in Coding", arXiv 2602.08316; v1 Feb 2026, v3 May 2026) [P-full, v3]
- Task stream: 1,100 base ("experience") tasks from SWE-Bench Lite, Multilingual and Verified whose solution trajectories form a context pool, plus 376 related tasks (319 first-order + 57 from recursive expansion); 1,476 tasks total, 51 repositories, 9 languages. A Lite version has 300 base + 99 related Python tasks from 12 repos — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Ordering: not a chronological stream. Related tasks are linked to base tasks by manually verified GitHub issue/PR cross-references (issue-to-issue 103, PR-to-issue 72, multi-issue resolution 46, issue-to-PR 41, PR-only 34, multi-reference 23). It is a two-stage design: solve base tasks, then solve related tasks with access to the pool — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Carried state (five settings): No-Context; Free Context (agent may retrieve full trajectories); Oracle Context (given the gold related trajectory); Free Summary; Oracle Summary; plus memory frameworks Mem0, OpenViking, Supermemory (LangMem only in the retrieval table). Summaries average 217.1 tokens vs 25,633.7 for full trajectories — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Metrics: resolution rate, FAIL_TO_PASS / PASS_TO_PASS, patch applicability, runtime, API cost. No transfer/forgetting metrics — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Results (99 related tasks, Claude Sonnet 4.5), resolved %: No-Context 26.26; Free Context 26.26; Oracle Context 27.27; Free Summary 22.22; Oracle Summary 34.34; Mem0 24.24; OpenViking 29.20; Supermemory 30.30. Cost per task: No-Context $0.79, Free Context $0.98, Oracle Summary $0.85, OpenViking $0.53 — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Results across five agents (baseline to oracle summary, resolved %): Claude Sonnet 4.5 / Claude Code 19.68 to 23.40; GPT-5.3 Codex 22.60 to 23.94; Qwen3.5-plus 16.22 to 21.54; GLM-5 18.35 to 19.41; MiniMax 2.7 19.68 to 22.07 — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Retrieval quality (top-1 match to the gold related task): Free Context 18.18%, Free Summary 36.36%, Mem0 39.39%, OpenViking 51.52%, Supermemory 59.60%, LangMem 73.34% — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Stated weaknesses: no systematic human validation of problem clarity or test correctness; context pool unfiltered so it can contain wrong/partial trajectories — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)

**Continual Learning Bench / CL-Bench** (arXiv 2606.05661, June 2026, UC Berkeley + Snorkel AI) [P-full for first ~75% of the paper]
- Six domains: software engineering (Codebase Adaptation), signal processing, epidemiological cohort studies, database querying, exploitable poker, demand forecasting. Only one is a coding-agent task — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Coding stream: 19 real Python bugfix issues from SWE-bench: 9 from jazzband/tablib then 10 from jd/tenacity (blocked by repo); each issue in a fresh Docker container at its base commit; patch checked against hidden regression tests — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1); [Snorkel leaderboard page](https://snorkel.ai/leaderboard/continual-learning-bench/)
- Per-issue reward is step-efficiency-weighted: r = 1 - (steps_to_solve - 1)/max_steps with max_steps = 40; 0 if unsolved — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Carried state: any context-based state (full accumulated context "ICL", notepad, retrieval memory such as Mem0, ACE playbooks, native Claude Code / Codex). Parametric methods (test-time training) are explicitly not evaluated — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Metrics: gain g_t = r_t(stateful) - r_t(stateless), with the stateless run being the same system on the same instance; normalized gain = (mean r_sf - mean r_sl)/(r_max - mean r_sl), i.e. fraction of the system's own headroom captured; normalized reward vs an external reference (stateless GPT-5.4 ICL); mean rollout cost in USD; gain decomposed into stability (first instance after a variant switch) and plasticity (within variant) — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Headline results (all six domains aggregated; normalized gain %, cost per run): ICL Sonnet 4.6 25.4% ($30.4); Claude Code Sonnet 4.6 23.9% ($38.6); Mem0 GPT-5.4 20.2% ($18.3); ICL GPT-5.4 20.1% ($18.4); ICL Opus 4.7 19.5% ($49.6); ICL Notepad Sonnet 4.6 18.2%; ICL Gemini 3 Flash 16.4% ($7.6); Codex GPT-5.4 14.6%; ACE GPT-5.4 8.6% ($62.8); ICL Notepad GPT-5.4 7.8%; ICL Gemini 3.1 Pro 6.2% — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Authors' reading: naive full-context ICL beats dedicated memory systems on most tasks; accumulated state "frequently hurts rather than helps" (spurious generalizations, stale beliefs) — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Stated weaknesses: six domains only; sequences are tens of instances, shorter than deployment horizons; context-based memory only; needs frontier models — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Venue: Snorkel's page says "Accepted to NeurIPS 2026" — [Snorkel](https://snorkel.ai/research-paper/continual-learning-bench-evaluating-frontier-ai-systems-in-real-world-stateful-environments/); an ICML 2026 virtual-site listing also exists — [ICML](https://icml.cc/virtual/2026/75698). Conflict not resolved (possibly an ICML workshop plus NeurIPS main track).

**ChainSWE** (arXiv 2607.02606, July 2026; v2 Sept 2026) [P-full for first ~80%]
- Task stream: 100 chains / 304 bug-fix tasks from 54 Python repositories, mined from six SWE-bench-family datasets (SWE-rebench-v2 contributes 52 chains); average chain length 3.04, max 5; tasks span April 2019 to August 2025 — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Ordering: single-repository, sorted by commit date; consecutive instances are chained if the later base commit immediately follows the earlier one or the later gold+test patches apply cleanly on the earlier resolved state; AST filter requires code overlap between bugs — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Carried state: Seq = repository state including the agent's own earlier patches persists, conversation reset; Seq+Mem = repo and conversation transcript both persist; Oracle = fresh repo with gold patches for earlier bugs applied — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Metrics: per-bug % resolved, chain success (all bugs pass), per-position resolution, USD cost per task/chain — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Results: averaged over models and configs, per-bug accuracy falls from 58.9% (Oracle) to 36.5% (Seq) and 36.9% (Seq+Mem); chain success 20.0% Oracle vs 17.0% Seq. GPT-5.5: 69.1 / 49.0 / 47.4; Claude Opus 4.7: 64.5 / 40.5 / 39.5; Claude Opus 4.5: 64.0 / 43.0 / 37.5 — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Per-position: under Seq, GPT-5.5 goes 62.5% (pos 1) to 40.5% (pos 2) to 28.2% (pos 3); under Oracle it rises 61.2% to 70.4% to 75.9%, so later bugs are not intrinsically harder. The abstract's "up to 70%" is a relative drop at position 3 in specific configs — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- 48% of downstream failures at positions 2-3 are chain errors (40% of those broke working code) — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Stated weaknesses: Python only; chains no longer than 5; single scaffold (SWE-Edit); difficulty filter used one baseline model; some source tests enforce unstated requirements — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- What it really measures: error accumulation in a codebase the agent itself modified, not learning. It is the closest existing design to "same codebase evolving" with agent-authored state.

**VibeMemBench** (arXiv 2609.23570, 20 Sept 2026) [P-abs]
- 111 coding targets from 90 SWE-rebench V2 repositories with 3,634 history trajectories from the target repositories; targets include bug fixes, feature requests, interface changes, configuration work — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- Selection: a target is kept only when injected history experience improves its executable outcome in a reference setting (so every target has execution-verified useful experience) — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- Metrics: test-based resolution and agent steps vs a matched memory-off baseline — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- Results: direct injection of the frozen verified experience raised resolution by 1.1 to 4.5 percentage points on four of five held-out solvers and cut steps on all five; for existing memory systems, 11 of 12 solver-system pairings did not exceed the memory-off baseline — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- A search snippet describes the history as "earlier same-repository histories ... selected, deduplicated, and chronological" [S] — [arXiv 2609.23570 PDF](https://arxiv.org/pdf/2609.23570)

**MemDev-Bench** ("Does Memory Help Code Agents? Benchmarking Memory Systems over Real Repository Histories", arXiv 2610.27524, 20 Oct 2026) [P-abs]
- 555 base tasks, each paired with relevance-annotated earlier tasks from the same repository; 4,869 historical tasks made executable and verifiable by an automated pipeline — [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1)
- Findings (qualitative in abstract): memory mainly improves fine-grained localization and editing; memory can cause failures on tasks the agent would otherwise solve, even with related history, and unrelated history increases such failures; cause attributed to agents reusing memory without checking applicability; compressed memories drop process information, and raw trajectories reduce steps substantially more than memory systems — [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1)

**StreamBench** (arXiv 2406.08747, NeurIPS 2024 D&B; older than 2025) [P-full]
- Seven datasets; coding-related ones are Spider (2,147 instances), CoSQL (1,007), BIRD (1,534) (text-to-SQL) and DS-1000 (1,000, Python). Others: ToolBench, DDXPlus, HotpotQA — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Feedback after each instance is binary correctness only (not the ground truth) — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Carried state: stored (input, output, feedback) records via sliding window (GrowPrompt) or vector memory (MemPrompt, Self-StreamICL, MAM-StreamICL) — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Metrics: final execution accuracy / pass@1 over the stream. Gains (average of three LLMs), best non-streaming vs MAM-StreamICL: Spider 68.55 to 75.69; CoSQL 50.61 to 55.17; BIRD 30.40 to 36.38; DS-1000 37.70 to 43.10 — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Finding: storing only incorrect outputs degraded performance, sometimes below zero-shot; storing only correct outputs consistently helped — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Stated weaknesses: text-only; simulated binary feedback has a sim-to-real gap — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)

**LifelongAgentBench** (arXiv 2505.11942, May 2025) [P-full for first ~55%]
- Three environments: Database (SQL on Dockerized MySQL, 500 tasks, 22 SQL skills), Operating System (bash in Ubuntu containers, 29 command skills), Knowledge Graph (396 tasks). Tasks are tagged with atomic skills; task relatedness = harmonic mean of shared-skill proportions — [arXiv 2505.11942](https://arxiv.org/html/2505.11942v3)
- Carried state: replay of recent successful trajectories. Metric: task success rate — [arXiv 2505.11942](https://arxiv.org/html/2505.11942v3)
- Results (Llama-3.1-8B): DB 0.19 to 0.78 with 64 replayed examples; OS 0.43 to 0.50 with 4-16 examples but back to 0.42 at 32; KG 0.28 to 0.35 with 1 example, out-of-memory at 16+. Llama-3.1-70B DB 0.81 to 0.90. Qwen2.5-32B starts 0.82 and does not improve (0.71 at 4 examples) — [arXiv 2505.11942](https://arxiv.org/html/2505.11942v3)

**EvoAgentBench** (arXiv 2607.05202, 6 July 2026) [P-abs]
- Four domains including software engineering; 528 train / 267 test tasks; trace-grounded "Abilities" linked through Ability Graphs so every test task has verified training-side ability support; two scaffolds, three backbones — [arXiv 2607.05202](https://arxiv.org/abs/2607.05202)
- Findings: curated ability content transfers reliably across model families; no current automatic method sustains positive gain across all settings — [arXiv 2607.05202](https://arxiv.org/abs/2607.05202)
- It is a train-then-test transfer split, not an online stream.

#### B. Named in the brief but NOT cross-task learning benchmarks for coding

- **SWE-bench-Live** (arXiv 2505.23419, 2025): 1,319 issue-resolution tasks from GitHub issues created since 2024, 93 repositories; contamination-resistant and continuously updatable; tasks are scored independently — [arXiv 2505.23419](https://arxiv.org/html/2505.23419v2) [S]
- **SWE-rebench** (arXiv 2505.20411, NeurIPS 2025 D&B): automated pipeline producing over 21,000 interactive Python tasks from 3,468 repositories, with a continuously updated decontaminated leaderboard; i.i.d. scoring — [NeurIPS 2025 proceedings](https://papers.neurips.cc/paper_files/paper/2025/hash/21bec6ace947b1b58967b945c8ac0f10-Abstract-Datasets_and_Benchmarks_Track.html) [S]. It matters here mainly as the task source for ChainSWE and VibeMemBench.
- **SWE-Gym**: described in the SWE-rebench paper's comparison as roughly 2,400 tasks from a small number of repositories, a training environment (weight updates via fine-tuning on trajectories), not a sequential evaluation — [arXiv 2505.20411](https://arxiv.org/pdf/2505.20411) [S; I did not open the SWE-Gym paper itself]
- **CodeARC** (arXiv 2503.23145, NeurIPS 2025): inductive program synthesis; agent queries a hidden function and refines against a differential-testing oracle; 1,114 functions; best model o3-mini 52.7%. Learning is within an episode only. I found no "CodeARC-style sequence" benchmark — [arXiv 2503.23145](https://arxiv.org/abs/2503.23145) [S]
- **SWE-CI** (arXiv 2603.03823, March 2026) [P-full]: 100 tasks from 68 Python repos, each spanning on average 233 days and 71 consecutive commits; up to 20 Architect/Programmer iterations driven by the CI test gap; metrics normalized change, EvoScore (gamma-weighted mean favoring later iterations), solved rate, zero-regression rate. Most models have zero-regression rate below 0.25; only two Claude Opus models exceed 0.5. Only the codebase carries between iterations; it measures maintainability within one long task, not cross-task learning — [arXiv 2603.03823v4](https://arxiv.org/html/2603.03823v4)
- **SlopCodeBench** (arXiv 2603.24755, 2026) [P-abs]: 36 problems / 196 checkpoints where agents repeatedly extend their own solution; measures structural erosion and verbosity; best agent passes 14.8% of checkpoints; erosion rises in 77% of trajectories. Within-problem degradation, not learning — [arXiv 2603.24755](https://arxiv.org/abs/2603.24755)

#### C. Non-coding lifelong benchmarks with reusable metric design (brief)

- **MemoryAgentBench** (arXiv 2507.05257, July 2025; v4 June 2026) [P-abs]: four competencies: accurate retrieval, test-time learning, long-range understanding, selective forgetting; incremental multi-turn format; finding that no method masters all four. No coding tasks confirmed — [arXiv 2507.05257](https://arxiv.org/abs/2507.05257)
- **Evo-Memory** (arXiv 2511.20857, Nov 2025; v2 May 2026) [P-abs]: restructures 10 datasets into sequential task streams; implements 10+ memory modules; proposes ExpRAG and ReMem. No coding tasks mentioned in the abstract — [arXiv 2511.20857](https://arxiv.org/abs/2511.20857)
- **EvoMemBench** (arXiv 2605.18421, 2026; listed as NeurIPS 2026 poster) [S]: reports long-context baselines remain highly competitive and no single memory form works consistently — [arXiv 2605.18421](https://arxiv.org/pdf/2605.18421); [NeurIPS listing](https://neurips.cc/virtual/2026/poster/139805)
- **ContinualSkillBench** (arXiv 2608.03874, Aug 2026) [P-full for first ~75%]: five streams (Healthcare, Law, Math, Finance, Office; none is software engineering) of 100 subtasks ordered by difficulty then skill dependency; agents (Codex CLI, Claude Code on Harbor) keep an explicit skill repository updated in a reflection turn. Metric is Gain = Sequential - Independent reward. Sequential raised normalized reward in 14 of 15 model-domain pairs, macro +0.078; but explicit skills had no aggregate edge over plain ICL (Independent 0.469, ICL 0.585, Sequential 0.582). Curated order beat random permutations on skill-coverage. Does not report FWT/BWT/forgetting — [arXiv 2608.03874](https://arxiv.org/html/2608.03874)

### Inferences
- The field split in 2026 into two designs: (i) "stream" designs where the agent's own outputs become later inputs (ChainSWE, SWE-CI, SlopCodeBench), which so far show degradation, and (ii) "experience pool" designs where prior trajectories are offered as retrievable context (SWE-ContextBench, VibeMemBench, MemDev-Bench), which show small or negative gains from automatic memory and modest gains from oracle-selected experience. Almost nobody combines both: a long stream with agent-authored state AND a measured learning curve.
- SWE-Bench-CL is widely cited as "the" continual-learning coding benchmark but contributes a metric vocabulary rather than evidence.

### Gaps
- VibeMemBench and MemDev-Bench: only abstracts read. Names of memory systems, exact deltas for the memory systems, ordering scheme, leakage controls and limitations are unverified. The VibeMemBench abstract's "twelve pairings" from 4 systems x 5 solvers is unexplained.
- CL-Bench: I could not find per-domain numbers for Codebase Adaptation alone, nor exactly what feedback the agent sees after each issue (the unread tail of the paper may contain it).
- SWE-Gym and CodeARC primary papers were not opened; SWE-bench-Live and SWE-rebench facts are from search snippets of the primary pages.
- Did not verify whether any public leaderboard exists for SWE-Bench-CL; a secondary 2026 blog claims it still lacks frontier-model results ([blog](https://codex.danielvaughan.com/2026/08/05/swe-bench-cl-continual-learning-coding-agents-catastrophic-forgetting-codex-cli-memory-strategy/), not a primary source).
- StuLife and "Agents' Last Exam" surfaced in results but were not investigated.

## 2. Which use a single repository's chronological history as the stream?

### Takeaway
Three use genuinely chronological single-repo ordering (SWE-Bench-CL, ChainSWE, and by snippet VibeMemBench/MemDev-Bench as "earlier same-repo tasks"), but all are short or sparse: chains of at most 5 bugs, or at most 50 non-contiguous issues per repo. None replays a long contiguous slice of one repository's real history with the agent's memory persisting.

### Cited Findings
- SWE-Bench-CL: one sequence per repo (8 repos, 19-50 tasks each), ordered by creation timestamp then by difficulty; each task still starts from its own SWE-Bench base commit, so the codebase state is the real historical one, not the agent's — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- ChainSWE: single-repo chains sorted by commit date with verified patch-compatibility and code overlap; the agent's own patches persist; max length 5, average 3.04 — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- CL-Bench Codebase Adaptation: two repos in blocks (9 tablib then 10 tenacity), each issue at its own base commit in a fresh container; designed to test a repo switch — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- MemDev-Bench: each of 555 base tasks is paired with earlier tasks from the same repository (4,869 historical tasks), annotated for relevance — [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1)
- VibeMemBench: 3,634 history trajectories from the target repositories (90 repos, 111 targets) — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- SWE-CI: each task is a single repo's span of on average 71 consecutive commits over 233 days, but collapsed to one base-to-oracle task with up to 20 iterations, no cross-task memory — [arXiv 2603.03823v4](https://arxiv.org/html/2603.03823v4)
- SWE-ContextBench: related tasks are linked by issue/PR cross-reference, not time-ordered; no ordering scheme beyond the relationships — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- MemCoder (a method, arXiv 2603.13258) restricts retrieval to historical experiences created before the test issue to avoid temporal leakage — [arXiv 2603.13258](https://arxiv.org/pdf/2603.13258) [S]

### Inferences
- VibeMemBench averages about 1.2 targets per repo (111/90), so it evaluates "history then one target", not a learning curve along a repo.
- In SWE-Bench-CL the difficulty re-sort partly breaks chronology, confounding "learning" with "curriculum" and with later, harder tasks.
- No benchmark found has the agent work N >> 5 consecutive real tasks in one repo where both the repo state it produced and its memory persist.

### Gaps
- Whether MemDev-Bench orders history strictly by time and how many tasks per repo: not in the abstract.
- Whether CL-Bench orders issues chronologically within each repo: not confirmed.

## 3. Which measure learning from deployment-style feedback (CI, code review, merged vs rejected) rather than gold tests?

### Takeaway
I found none. Every sequential coding benchmark scores with hidden gold tests, and where feedback is given to the agent it is binary correctness (StreamBench), a test-gap summary (SWE-CI) or evaluator output (ContinualSkillBench). No benchmark feeds reviewer comments or merge/reject decisions back as the learning signal.

### Cited Findings
- StreamBench deliberately gives only binary correctness after each instance, arguing ground truth is too expensive in deployment; its authors list the sim-to-real gap of this simulated feedback as a limitation — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- SWE-CI drives each iteration from CI results: an Architect agent compares current test results with the oracle and writes at most five requirements per iteration; this is CI-style feedback but derived from gold tests of the target commit and within one task — [arXiv 2603.03823v4](https://arxiv.org/html/2603.03823v4)
- ContinualSkillBench's sequential mode retains evaluator feedback and has a reflection turn after each subtask; not coding — [arXiv 2608.03874](https://arxiv.org/html/2608.03874)
- CL-Bench: the readable portion of the paper does not state what feedback the agent receives after each coding issue — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Empirical PR studies (2026) exist on why agent PRs are merged or rejected, e.g. "Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study" — [arXiv 2605.22534](https://arxiv.org/abs/2605.22534) and "Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub" — [arXiv 2601.15195](https://arxiv.org/html/2601.15195). Search snippets attribute to this literature that roughly 61-68% of rejected agent PRs carry no explicit reviewer feedback or stated reason, and that only 35.7% of rejections reflected clear agent failure [S; I could not map each statistic to its specific paper].
- GitHub's ReviewBench is an open benchmark for AI code review (reviewing, not learning from review) — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/) [S]

### Inferences
- If the PR-study numbers hold, merge/reject labels are noisy and often rationale-free, so a deployment-feedback benchmark needs either curated review threads or a simulated reviewer, plus a gold-test check held out from the agent to measure whether learning from the noisy signal actually improves correctness.
- This is the most clearly open axis in the space.

### Gaps
- The PR-study statistics are from search snippets; primary papers not read.
- I did not search exhaustively for code-review-comment-conditioned benchmarks (e.g. review-revision datasets); absence of evidence here is from two extended searches only.

## 4. How have classical continual-learning metrics (GEM ACC/BWT/FWT, forgetting, plasticity/stability) been adapted to agents?

### Takeaway
Only SWE-Bench-CL ports the full GEM matrix-style metric family to coding agents, and it never populated them with data; benchmarks that report real numbers (CL-Bench, ContinualSkillBench, ChainSWE, SWE-ContextBench) instead use a paired stateful-minus-stateless gain, sometimes decomposed into stability/plasticity.

### Cited Findings
- Original definitions (Lopez-Paz and Ranzato, 2017; older than 2025): with R(i,j) the accuracy on task j after training through task i and b the accuracy at random initialization, ACC is the mean of the final row, BWT is the influence of learning a task on previous tasks (negative = forgetting), FWT compares R(i-1,i) with the random-init baseline b_i — [arXiv 1706.08840](https://arxiv.org/pdf/1706.08840)
- SWE-Bench-CL adaptations (a_{i,j} = success on task j after experiencing task i; zero-shot success replaces the random-init baseline):
  - ACC = (1/N) sum_j a_{N,j}
  - Forgetting F = (1/(N-1)) sum_{j<N} (max_{k<=j} a_{k,j} - a_{N,j})
  - Forward transfer FT = (1/(N-1)) sum_i (a_{i,i+1} - a_{0,i+1})
  - BWT = (1/(N-1)) sum_i (a_{N,i} - a_{i,i})
  - AULC = (1/N) sum_i (1/i) sum_{k<=i} a_{k,k}
  - Tool-use efficiency = median(time | success) / median(time | all)
  - CL-Plasticity = (1/N) sum a_{i,i}; CL-Stability = 1 - F; CL-F-beta = (1+b^2) P S / (b^2 P + S)
  - CL-Score = ACC - lF*F + lFT*FT + lBWT*BWT + lAULC*AULC + CL-F-beta, lambdas unspecified
  — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- CL-Bench: per-instance gain g_t = r_sf - r_sl against the same system run statelessly on the same instance; normalized gain as fraction of own headroom; stability = gain on the first instance after a variant switch, plasticity = gain within a variant; cost in USD reported alongside — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- ContinualSkillBench: Gain = Sequential - Independent (raw and normalized reward), plus skill reuse rate and core-skill coverage over a window of prior tasks (cosine >= 0.85), compared against 10,000 random-order permutations; explicitly no FWT/BWT/forgetting — [arXiv 2608.03874](https://arxiv.org/html/2608.03874)
- ChainSWE: per-position resolution under Oracle vs Seq vs Seq+Mem; the Oracle-vs-Seq gap by position functions as a (negative) transfer curve — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- SWE-CI: EvoScore = sum gamma^i a(c_i) / sum gamma^i with gamma >= 1 weighting later iterations; zero-regression rate as a stability proxy — [arXiv 2603.03823v4](https://arxiv.org/html/2603.03823v4)
- MemoryAgentBench treats "test-time learning" and "selective forgetting" as separate competencies rather than matrix metrics — [arXiv 2507.05257](https://arxiv.org/abs/2507.05257)
- A 2026 survey ("Always-On Agents") is reported to describe SWE-Bench-CL as measuring forgetting and forward/backward transfer over per-repo streams — [arXiv 2606.30306](https://arxiv.org/pdf/2606.30306) [S]

### Inferences
- BWT and Forgetting require re-running earlier tasks after later ones (the full a_{i,j} matrix): O(N^2) agent runs, which at 2026 per-task costs ($0.3-$7 per task/chain in ChainSWE and SWE-ContextBench) is probably why nobody reports them. For non-parametric agents with append-only memory, "forgetting" mostly reduces to retrieval interference or memory compaction loss, so the metric is less natural than for weight updates.
- The paired counterfactual (same agent, same task, memory on vs off) is the de facto standard for forward transfer in agents. It cleanly isolates the learning effect from base capability, which a raw learning-curve slope cannot do when task difficulty drifts along the stream (ChainSWE's Oracle curve rising with position illustrates that drift).
- No benchmark found reports a fitted learning-curve slope or sample-efficiency figure (tasks-to-reach-X) for coding agents; AULC in SWE-Bench-CL is the nearest, and is unpopulated.

### Gaps
- I did not find a paper that critically analyzes whether GEM-style metrics are well-defined for retrieval-memory agents; the inference above is mine.
- Evo-Memory's metric definitions (possibly step efficiency and order robustness) were not verified; abstract only.

## 5. How big is the reported "learning effect"? Are there negative results where memory hurts?

### Takeaway
On realistic repo-level coding tasks the measured effect of automatic memory is small: roughly -4 to +5 percentage points of resolution rate, with oracle-selected experience reaching about +1 to +8 points; negative and null results are common. Large gains (tens of points) appear only on simpler, highly repetitive streams (SQL) with weak base models.

### Cited Findings
- SWE-ContextBench (99 tasks, Sonnet 4.5): Oracle Summary +8.08 points (26.26 to 34.34); Oracle full trajectory +1.01; free retrieval of trajectories 0.00 at higher cost ($0.98 vs $0.79); free retrieval of summaries -4.04; Mem0 -2.02; OpenViking +2.94; Supermemory +4.04. Across five agents with oracle summaries: +1.06 to +5.32 points — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- VibeMemBench: execution-verified experience injected directly gives +1.1 to +4.5 points on 4 of 5 solvers; 11 of 12 pairings with existing memory systems fail to beat memory-off — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570)
- MemDev-Bench: memory can break tasks the agent would otherwise solve, even with related history; unrelated history makes it worse — [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1)
- ChainSWE: adding the conversation transcript as memory changes average per-bug accuracy from 36.5% to 36.9%; Claude Opus 4.5 drops 43.0 to 37.5; GPT-5.5 is the main exception when config-averaged (42.2 to 46.8). Sequential state overall costs about 22 points vs Oracle (58.9 to 36.5) — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- CL-Bench (six domains): best normalized gain 25.4% of headroom (ICL, Sonnet 4.6); ACE captures 8.6% at the highest cost ($62.8/run); the notepad variant underperforms plain ICL for Sonnet 4.6 (18.2 vs 25.4) and GPT-5.4 (7.8 vs 20.1) but beats it for Gemini 3.1 Pro (9.4 vs 6.2); authors say accumulated state "frequently hurts rather than helps" — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- SWE-Bench-CL: memory-enabled "on par with or slightly worse" in the only (unreliable) run — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- ReasoningBank (a method, Google, arXiv 2509.25140, 2025): +4.6 points on SWE-Bench-Verified with Gemini-2.5-Flash over a memory-free agent, and almost 3 fewer steps per task — [Google Research blog](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/) [S]; a third-party summary gives 34.2% to 38.8% — [secondary](https://aiagentmemory.org/articles/reasoningbank-llm-agent-memory-framework/) [S]
- StreamBench (2024): +4.6 to +7.1 points on text-to-SQL and +5.4 on DS-1000 for the best streaming method over the best non-streaming baseline; memory of only-incorrect outputs can fall below zero-shot — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- LifelongAgentBench (2025): Llama-3.1-8B on SQL 0.19 to 0.78; on bash only 0.43 to 0.50 and declining with more replay; a strong model (Qwen2.5-32B, 0.82) gets no benefit; larger replay buffers cause OOM — [arXiv 2505.11942](https://arxiv.org/html/2505.11942v3)
- ContinualSkillBench (non-coding): +0.078 normalized reward macro average; explicit skill libraries roughly tie plain ICL (0.582 vs 0.585); Opus 4.7 slightly negative on Math (-0.008) — [arXiv 2608.03874](https://arxiv.org/html/2608.03874)
- EvoAgentBench: no automatic method sustains positive gain across all settings — [arXiv 2607.05202](https://arxiv.org/abs/2607.05202)

### Inferences
- The effect sizes on repo-level tasks (a few points) are comparable to typical run-to-run variance on 99-111 task sets (one task is about 1 point), and most papers do not report seeds or confidence intervals for the coding results (CL-Bench does report CIs). A new benchmark needs enough tasks and repeats to resolve a roughly 3-point effect.
- The consistent pattern "oracle-selected experience helps, self-retrieved experience does not" locates the bottleneck in selection/applicability judgment rather than in the availability of useful experience.
- Gains shrink as base model strength rises (LifelongAgentBench Qwen 32B; SWE-ContextBench GPT-5.3 Codex +1.34), so headroom must be designed in.
- Efficiency gains (fewer steps, lower cost) are more robust than accuracy gains (VibeMemBench steps fell on all five solvers; SWE-ContextBench memory frameworks cut cost to $0.53-$0.62 from $0.79).

### Gaps
- No verified per-domain learning effect for CL-Bench's coding task.
- MemDev-Bench and VibeMemBench exact deltas for named memory systems not obtained.
- ReasoningBank numbers not checked against the paper itself. I found nothing on SWE-Exp or Agent KB in the searches run.

## 6. What criticisms exist (contamination, solution leakage through memory, task-similarity confound, uncontrolled cost)?

### Takeaway
Criticism is mostly self-reported in limitations sections and implicit in later benchmarks' designs rather than in dedicated critique papers: lack of real results (SWE-Bench-CL), tiny streams (CL-Bench coding: 19 issues), selection bias toward memory-helpable tasks (VibeMemBench), unfiltered experience pools, low intrinsic task similarity, and source-data contamination inherited from SWE-bench.

### Cited Findings
- Contamination: SWE-bench-Live and SWE-rebench were created because static SWE-bench tasks leak into training data; SWE-rebench offers a decontaminated, continuously updated leaderboard — [arXiv 2505.23419](https://arxiv.org/html/2505.23419v2); [NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/hash/21bec6ace947b1b58967b945c8ac0f10-Abstract-Datasets_and_Benchmarks_Track.html) [S]. SWE-Bench-CL, SWE-ContextBench and CL-Bench's coding task are all built on SWE-bench-family data — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1); [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3); [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1). ChainSWE tasks span April 2019 to August 2025 — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Temporal leakage through memory: MemCoder explicitly restricts retrieval to experiences created before the test issue "to avoid temporal leakage", implying this is a recognized hazard — [arXiv 2603.13258](https://arxiv.org/pdf/2603.13258) [S]
- Task-similarity confound: SWE-Bench-CL's own analysis shows very low gold-patch similarity within sequences (Jaccard 0.11, cosine 0.18), i.e. chronological adjacency alone gives little to transfer; its dependency proxy is file-path overlap only — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1). Later benchmarks respond by engineering relatedness: verified cross-references (SWE-ContextBench), AST code-overlap filter (ChainSWE), relevance annotation (MemDev-Bench), ability graphs (EvoAgentBench), LLM-judged skill dependency (ContinualSkillBench) — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3); [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2); [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1); [arXiv 2607.05202](https://arxiv.org/abs/2607.05202); [arXiv 2608.03874](https://arxiv.org/html/2608.03874)
- Selection bias: VibeMemBench keeps a target only if injected history improved its outcome in a reference setting, so the benchmark is conditioned on memory being helpful — [arXiv 2609.23570](https://arxiv.org/abs/2609.23570). ChainSWE keeps only chains where a baseline solved more than half the bugs in Oracle mode — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Order/curriculum confound: SWE-Bench-CL re-sorts by difficulty and admits strict chronological-with-curriculum order may not reflect interleaved development — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1). ChainSWE shows Oracle success rises with position (61.2 to 75.9% for GPT-5.5), i.e. position effects exist independent of learning — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Memory quality / poisoned memory: SWE-Bench-CL attributes its null result to memory dominated by failed attempts; SWE-ContextBench's pool is unfiltered and may contain incorrect trajectories; StreamBench shows incorrect-only memory hurts — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1); [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3); [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2)
- Cost: reported but not controlled. CL-Bench reports cost per run ($7.6 to $62.8) next to gain; SWE-ContextBench reports per-task cost and time; ChainSWE reports per-chain cost ($0.2 to $6.8). None budgets or normalizes the learning gain by cost — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1); [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3); [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Baseline strength: CL-Bench and ContinualSkillBench both find plain full-context ICL matches or beats purpose-built memory/skill systems; EvoMemBench reports long-context baselines remain highly competitive — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1); [arXiv 2608.03874](https://arxiv.org/html/2608.03874); [arXiv 2605.18421](https://arxiv.org/pdf/2605.18421) [S]
- Scale/horizon: CL-Bench admits sequences of tens of instances are shorter than deployment horizons; ChainSWE could not build chains longer than five — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1); [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Test validity: ChainSWE notes source tests sometimes enforce unstated requirements; SWE-ContextBench lacks human validation of task solvability — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2); [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3)
- Parametric learning untested: CL-Bench evaluates context-based memory only — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)

### Inferences
- Solution leakage is structurally possible in "experience pool" designs: when related tasks are linked by PR/issue cross-reference (SWE-ContextBench multi-issue resolution, 46 links), the base task's trajectory may contain most of the related task's fix. Oracle Summary's +8 points could therefore partly reflect near-duplicate solutions rather than transferable skill. I did not find a paper that quantifies this.
- A memory-on vs memory-off comparison does not separate "learned something about the repo" from "pretrained model already memorized this repo's history"; using post-cutoff tasks (SWE-rebench style) is the only control seen, and only VibeMemBench and partly ChainSWE draw on such data.
- Because full-context ICL is such a strong baseline at tens of tasks, a benchmark must be long enough that the stream cannot fit in context, otherwise it measures context length rather than learning.

### Gaps
- I found no standalone critique paper on continual-learning agent benchmarks (as opposed to limitations sections). The leakage and memorization concerns above are partly my inference.
- No source found that measures variance/seeds for the sequential coding results.

## 7. What gap remains unfilled?

### Takeaway
No benchmark as of November 2026 measures whether a coding agent gets better over a long, contiguous, chronological stream of real work in one evolving repository, with its own code and memory persisting, learning from deployment-style signals (CI, review, merge/reject) rather than gold tests, with a cost-controlled paired counterfactual and enough tasks to resolve a few-point effect.

### Cited Findings
- Longest verified single-repo persistent-state stream: 5 bugs (ChainSWE) — [arXiv 2607.02606v2](https://arxiv.org/html/2607.02606v2)
- Only benchmark with full CL metric definitions has no populated results (SWE-Bench-CL) — [arXiv 2507.00014](https://arxiv.org/html/2507.00014v1)
- Only benchmark with a clean stateful-vs-stateless gain and stability/plasticity split has 19 coding issues across two repos (CL-Bench) — [arXiv 2606.05661](https://arxiv.org/html/2606.05661v1)
- Experience-pool benchmarks are two-stage (history then target), not streams with a learning curve (SWE-ContextBench, VibeMemBench, MemDev-Bench) — [arXiv 2602.08316v3](https://arxiv.org/html/2602.08316v3); [arXiv 2609.23570](https://arxiv.org/abs/2609.23570); [arXiv 2610.27524](https://arxiv.org/abs/2610.27524v1)
- Feedback given to agents is binary correctness or test results in every case found (StreamBench, SWE-CI) — [arXiv 2406.08747](https://arxiv.org/html/2406.08747v2); [arXiv 2603.03823v4](https://arxiv.org/html/2603.03823v4)

### Inferences
Specific unfilled pieces, in rough order of how clearly the evidence supports them:
1. Deployment-style feedback as the learning signal (review comments, CI logs, merge/reject), with gold tests held out purely for scoring. Nothing found.
2. Long horizon in one repo (tens to hundreds of chronologically contiguous tasks) where the stream exceeds context so naive ICL cannot win by default.
3. Learning curve as a first-class output: per-position paired gain (memory on minus memory off on the same task at the same repo state), slope, tasks-to-threshold; currently only ChainSWE reports per-position numbers and they show decline.
4. Separation of the two kinds of carried state: the codebase the agent changed (source of error accumulation in ChainSWE/SWE-CI/SlopCodeBench) vs the agent's knowledge (memory/notes/skills). No benchmark crosses these factors beyond ChainSWE's Seq vs Seq+Mem.
5. Backward transfer / forgetting actually measured (re-test earlier tasks or probe repo knowledge after later tasks, after a repo switch as CL-Bench gestures at).
6. Cost-controlled comparison (equal token/dollar budget for memory-on and memory-off) and reporting variance across seeds.
7. Controls for leakage: post-cutoff tasks, temporal cutoffs on memory, and a near-duplicate-solution check between history and target.
8. Weight-update (parametric) learners evaluated on the same stream as memory-based ones.

### Gaps
- This gap statement rests on roughly 30 searches/fetches; a benchmark released in the last weeks before November 2026 or one outside arXiv (lab blog, product eval) could be missed. In particular I did not check vendor blogs for internal "memory" evals of coding products.
