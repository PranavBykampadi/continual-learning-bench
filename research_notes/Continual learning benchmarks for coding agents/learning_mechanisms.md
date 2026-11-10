# Learning mechanisms for deployed LLM coding agents (state as of November 2026)

Verification legend used throughout:
- **[P]** = verified this session against a primary source (paper abstract page, vendor docs, official transcript, lab blog).
- **[S]** = seen this session only via a search-result summary of the primary source (numbers likely right, but the primary page was not opened; re-check before quoting).
- **[M]** = from the researcher's prior knowledge of the cited paper; the URL is the canonical primary source but it was NOT opened this session. Re-check before quoting.
- **[3P]** = third-party / community source only; no primary confirmation found.

Cross-paper numbers are not comparable: scaffolds, backbones, subsets and seeds all differ.

---

## 1. Non-parametric / context-level learning (memory files, reflection, playbooks, skills, prompt evolution, trajectory retrieval)

### Takeaway
Context-level learning is the only family that is actually deployed in coding-agent products in 2026 (CLAUDE.md/AGENTS.md, Claude Code auto memory, Codex memories, Letta Code skills), but the measured gains on SWE-style tasks are small and fragile: roughly +2 to +10 points on SWE-bench Verified subsets in the favourable papers, about zero (with >20% more cost) for auto-generated AGENTS.md files, and about -1.3 pp for self-generated skills in SkillsBench. Most of the canonical methods (Reflexion, ExpeL, AWM, Dynamic Cheatsheet, ACE, GEPA) have no headline SWE-bench result of their own; their published numbers are on web, math, QA or game tasks.

### Cited Findings

**Static / human-or-agent-written memory files (CLAUDE.md, AGENTS.md)**
- [P] Claude Code has two cross-session mechanisms: CLAUDE.md files ("instructions you write") and auto memory ("notes Claude writes itself based on your corrections and preferences"). Both are "loaded at the start of every conversation" and treated "as context, not enforced configuration". — [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
- [P] Auto memory lives at `~/.claude/projects/<project>/memory/` with a `MEMORY.md` index plus topic files; only "the first 200 lines of MEMORY.md, or the first 25KB, whichever comes first" are loaded at session start; topic files are read on demand. It can be disabled with `autoMemoryEnabled: false` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, and relocated with `autoMemoryDirectory`. — [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
- [P] Vendor-stated failure mode (context bloat): "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." — [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
- [P] Claude Code reads a repo's AGENTS.md directly from v2.1.277 onward. — [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
- [S] "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (Gloaguen, Mündler, Müller, Raychev, Vechev; arXiv Feb 2026; ICLR 2026): across multiple coding agents and LLMs, context files gave "no improvement in task success rates, while also increasing inference cost by over 20%". Agents tested: Claude Code (Sonnet 4.5), Codex (GPT-5.2, GPT-5.1 mini), Qwen Code. Evaluated on SWE-bench Lite with LLM-generated files and on a new benchmark built from repos with developer-committed context files. LLM-generated files only helped when existing repo docs were removed, i.e. they mostly duplicate documentation. Authors recommend human-written files contain only minimal requirements. — [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)
- [S, secondary summary] Size of the effect in that paper: LLM-generated files lowered success by ~0.5 points on SWE-bench Lite and ~2 points on the authors' benchmark on average. — [Moonlight review of 2602.11988](https://www.themoonlight.io/review/evaluating-agentsmd-are-repository-level-context-files-helpful-for-coding-agents)

**Productised agent-written memory (2026)**
- [P] OpenAI Codex "memories": off by default; enabled via Settings or `[features] memories = true` in `config.toml`; stored under `$CODEX_HOME/memories_v2/` (or legacy `memories/`); Codex "turns useful context from eligible prior chats into local memory files", updated "in the background instead of immediately at the end of every chat", with a separate `memories.consolidation_model` setting for "global memory consolidation". Docs state memories are a recall aid, not a rule source; required guidance belongs in AGENTS.md. Settings `generate_memories` / `use_memories` separate writing from injection (useful for ablations). — [OpenAI Codex docs: memories](https://learn.chatgpt.com/docs/customization/memories?surface=app)
- [3P] Claude Code "Auto Dream" / `/dream`: community reports describe a background sub-agent that consolidates the auto-memory directory when idle (reported triggers ~24 h and >=5 sessions), writes only to memory files, and keeps a `.bak`. It does NOT appear in the official memory docs page read this session; all sources found are third-party. Reported failure modes: misnamed files after project renames, unverified counts written into memory, no changelog of what was modified. — [Implicator](https://www.implicator.ai/anthropic-adds-auto-dream-to-claude-code-fixing-memory-decay-between-sessions/); [claudeissues feature request](https://claudeissues.com/issue/38493-feature-auto-dream-3-gaps-identity-accuracy-transparency)
- [S] Anthropic API "memory tool" + context editing (2025): Anthropic's announcement reports that combining the memory tool with context editing improved performance by 39% over baseline on an internal agentic-search eval, context editing alone 29%, and an 84% token reduction in a 100-turn web search eval. The memory tool is client-side (file-based, developer-managed storage). Not a coding benchmark. — [Anthropic: context management](https://www.anthropic.com/news/context-management)

**Reflection / verbal RL**
- [M] Reflexion (Shinn et al., 2023): episodic verbal self-reflections stored in a buffer and retried on the same task; reported 91% pass@1 on HumanEval vs 80% for the GPT-4 baseline. This is same-task retry with test feedback, not cross-task transfer. — [arXiv 2303.11366](https://arxiv.org/abs/2303.11366)
- [M] ExpeL (Zhao et al., 2023): extracts natural-language insights from success/failure trajectories and retrieves past successful trajectories as few-shot examples; evaluated on HotpotQA, ALFWorld, WebShop (no coding benchmark). — [arXiv 2308.10144](https://arxiv.org/abs/2308.10144)

**Workflow / strategy memory**
- [M] Agent Workflow Memory (Wang et al., 2024): induces reusable workflows from past trajectories, offline or online; reported 24.6% and 51.1% relative success-rate gains on Mind2Web and WebArena. Web navigation only. — [arXiv 2409.07429](https://arxiv.org/abs/2409.07429)
- [P for existence/date, S for numbers] ReasoningBank (Ouyang et al., Google; Sep 2025, revised Mar 2026): distils generalisable reasoning strategies from both successful and failed trajectories, judged by the agent itself; abstract claims it outperforms existing memory mechanisms on web browsing and software engineering benchmarks. Search summaries of the paper/blog report +8.3% on WebArena and +4.6% on SWE-Bench-Verified over memory-free agents with Gemini 2.5 Flash, and AWM as a baseline. — [arXiv 2509.25140](https://arxiv.org/abs/2509.25140); [Google Research blog](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)
- [S] MemGuard (arXiv Aug 2026): on a chronological stream of SWE-bench issues, reports +2.96 resolve-rate points and -2.10 steps versus ReasoningBank under the same settings by persisting verifier signals to govern memory. — [arXiv 2608.21867](https://arxiv.org/pdf/2608.21867)
- [S] MemCoder (arXiv Mar 2026, "Your Code Agent Can Grow Alongside You with Structured Memory"): structured memory learned from developer commits; reports resolved rate 68.4% -> 77.8% (+9.4) over DeepSeek-V3.2 on a random 200-instance subset of SWE-bench Verified. — [arXiv 2603.13258](https://arxiv.org/abs/2603.13258)
- [S] A pre-registered community benchmark of persistent memory with provenance on SWE-bench Verified found +10.2 points on 49 paired tasks in a single trial (67.3% -> 77.6%), but a multi-seed mean effect of only +0.24 per instance, 95% CI [0, 0.47]. Useful as a cautionary data point about seed variance. — [GitHub: coding-agent-memory-benchmark](https://github.com/SaravananJaichandar/coding-agent-memory-benchmark)

**Evolving cheatsheets / playbooks**
- [P] Dynamic Cheatsheet (Suzgun, Yuksekgonul, Bianchi, Jurafsky, Zou; Apr 2025): a persistent, self-curated test-time memory. Abstract results: Claude 3.5 Sonnet's AIME accuracy "more than doubled"; GPT-4o on Game of 24 from 10% to 99%; +9% GPQA-Diamond and +8% MMLU-Pro for Claude. No SWE-style result. — [arXiv 2504.07952](https://arxiv.org/abs/2504.07952)
- [P] ACE, Agentic Context Engineering (Zhang et al.; Oct 2025, v3 Mar 2026; ICLR 2026): Generator / Reflector / Curator loop that treats contexts as "evolving playbooks that accumulate, refine, and organize strategies", with incremental delta updates instead of full rewrites. Abstract: +10.6% on agent benchmarks and +8.6% on finance over strong baselines; on AppWorld it "matches the top-ranked production-level agent on the overall average" and beats it on the harder test-challenge split with a smaller open-source model; adapts without labelled supervision using execution feedback. No SWE-bench result. — [arXiv 2510.04618](https://arxiv.org/abs/2510.04618)
- [S] ACE names the two failure modes the question asks about. **Brevity bias**: prompt optimisers favour short generic instructions and drop domain heuristics, tool-use guidance and common failure modes (GEPA is cited as an example). **Context collapse**: monolithic LLM rewriting of accumulated context shrinks it into shorter, less informative summaries with sharp performance drops, observed in an AppWorld case study. — [arXiv 2510.04618 (HTML v2)](https://arxiv.org/html/2510.04618v2)
- [S, secondary] Reported ACE efficiency figures: 86.9% lower adaptation latency and up to 83.6% lower rollout cost. Not in the abstract; check the paper body. — [emergentmind summary](https://www.emergentmind.com/papers/2510.04618)

**Prompt evolution**
- [P] GEPA (Agrawal et al.; Jul 2025, revised Feb 2026): reflective prompt evolution with Pareto selection. Abstract: beats GRPO by 6% on average and up to 20% across six tasks while using up to 35x fewer rollouts; beats MIPROv2 by over 10% (e.g. +12% on AIME-2025). This is an offline optimiser over a train set, not an online deployment learner; no SWE-bench headline. — [arXiv 2507.19457](https://arxiv.org/abs/2507.19457)

**Skill libraries**
- [M] Voyager (Wang et al., 2023): the canonical executable skill library (code skills indexed by embedding, added after self-verification) in Minecraft. — [arXiv 2305.16291](https://arxiv.org/abs/2305.16291)
- [P] Letta "Skill Learning" (blog, 2 Dec 2025): two-stage reflection -> skill creation (using Anthropic's skill-creator) from past trajectories. On Terminal-Bench 2.0 (all 89 tasks, Letta Code + Sonnet 4.5 with extended thinking): trajectory-only skills +21.1% relative (+9% absolute); trajectory + verifier feedback +36.8% relative (+15.7% absolute); trajectory-learned skills cut cost 15.7% and tool calls 10.4%. Caveats: single model, no variance reported, skills learned from and evaluated on the same benchmark's tasks, vendor blog not peer reviewed. — [Letta blog: skill learning](https://www.letta.com/blog/skill-learning/)
- [S] SkillsBench (arXiv Feb 2026; NeurIPS 2026 listing): each task run with no skills / curated skills / self-generated skills across 7 agent-model configurations. Curated skills: about +16.2 pp average (sources vary 12.7 to 16.4 pp; 84 or 86 tasks depending on version), ranging from +4.5 pp in software engineering to +51.9 pp in healthcare. **Self-generated skills: about -1.3 pp on average**; models do not reliably author the procedural knowledge they need. — [arXiv 2602.12670](https://arxiv.org/abs/2602.12670)

**General agent-memory systems (canonical references, not coding-specific)**
- [M] MemGPT (Packer et al., 2023): OS-style paging between in-context "core memory" and external archival/recall stores, edited by the agent via tool calls. — [arXiv 2310.08560](https://arxiv.org/abs/2310.08560)
- [M] A-MEM (Xu et al., 2025): Zettelkasten-style linked, self-evolving notes. — [arXiv 2502.12110](https://arxiv.org/abs/2502.12110)
- [M] Mem0 (Chhikara et al., 2025): extract/consolidate/retrieve memory layer; paper reports ~26% relative gain over OpenAI's memory on the LOCOMO conversational benchmark with large latency/token savings. Conversational, not coding. — [arXiv 2504.19413](https://arxiv.org/abs/2504.19413)
- [S] Letta sleep-time compute paper (2025): pre-computing over context while idle cut test-time compute needed for equal accuracy by ~5x on Stateful GSM-Symbolic and Stateful AIME; scaling sleep-time compute raised accuracy up to 13% and 18% respectively; amortising across related queries cut cost per query 2.5x. Math benchmarks, not coding. — [Letta research](https://www.letta.com/research/); paper [arXiv 2504.13171](https://arxiv.org/abs/2504.13171) [M for the arXiv id]
- [S] Letta Code (Dec 2025) is positioned as a "memory-first coding agent". — [Letta blog](https://www.letta.com/blog/letta-code/)

**Existing continual-learning benchmark for coding agents**
- [P] SWE-Bench-CL (Joshi, Chowdhury, Uysal; June 2025): reorganises SWE-bench Verified into chronological per-repo sequences; proposes average accuracy, forgetting, forward/backward transfer, tool-use efficiency, a composite CL score and CL-F-beta; ships a LangGraph agent with FAISS semantic memory. The abstract only "outlines" a memory-on vs memory-off protocol; **no experimental results are reported on the abstract page**. — [arXiv 2507.00014](https://arxiv.org/abs/2507.00014)

### Inferences
- The strongest *independent* evidence (ICLR 2026 AGENTS.md study, SkillsBench) is negative or null for automatically generated context, while the strongest *positive* numbers come from method authors or vendors on small subsets or single seeds. A credible benchmark must report multi-seed confidence intervals and a cost axis; the pre-registered 49-task result (+10.2 single trial vs +0.24 multi-seed) shows how easily a memory "gain" is noise.
- Human-curated vs agent-generated is the key split: curated skills help (+16 pp), self-generated ones do not. A deployment-learning benchmark is specifically testing the agent-generated arm, which is the weak one.
- Failure modes to instrument, each with a named source: context bloat reducing adherence (Claude Code docs), redundancy with existing repo docs plus cost overhead (AGENTS.md study), brevity bias and context collapse (ACE), unverified or stale facts written by consolidation (community Auto Dream reports), memory that is "a recall aid, not a rule source" (Codex docs).
- Gains appear larger when the memory carries verifier feedback (Letta: +9 abs trajectory-only vs +15.7 abs with feedback; MemGuard's verifier-signal persistence), suggesting "does the agent get ground-truth outcome signal after each task" is a first-order benchmark design variable.
- Same-task retry (Reflexion) and cross-task transfer (AWM, ReasoningBank, ACE online) are different settings and should be separate tracks.

### Gaps
- No primary-source SWE-bench numbers were found for Reflexion, ExpeL, AWM, Dynamic Cheatsheet, ACE, GEPA, A-MEM, Mem0 or MemGPT; they would have to be re-implemented as baselines rather than cited.
- ReasoningBank's exact SWE-Bench-Verified table (baseline vs method per backbone) was not read from the PDF; the +4.6 figure is from a search summary.
- "RAG over past PRs / trajectory retrieval" as a standalone method: no dedicated primary source with SWE-bench numbers was located this session beyond MemCoder (commit-derived memory) and SWE-Bench-CL's FAISS agent (no results).
- Claude Code Auto Dream is not confirmed by official docs or changelog; publication date of Anthropic's context-management post and of Anthropic Agent Skills were not verified this session.
- SWE-Bench-CL full-paper results (if any appear in the PDF body) were not checked; only the abstract page was read.
- [M]-tagged numbers (Reflexion 91%, AWM 24.6%/51.1%, Mem0 26%) need re-verification before publication.

---

## 2. Parametric learning (fine-tuning on trajectories, RL, test-time training, continual fine-tuning, model editing)

### Takeaway
All strong published parametric results for SWE agents are *offline* training on large pre-collected environment sets with open-weight models (roughly 20% to 41% single-attempt on SWE-bench Verified in 2025), not online learning from a single deployment's stream. No primary source was found demonstrating online LoRA / test-time training of a coding agent on its own deployment trajectories with a forgetting analysis; that remains an open gap, and it is infeasible anyway without weight access.

### Cited Findings
- [S] SWE-Gym (Dec 2024): fine-tuning Qwen-2.5-Coder-32B on 491 sampled agent trajectories gave +12.3 pts (to 15.3%) on SWE-bench Lite and +13.6 pts (to 20.6%) on SWE-bench Verified; adding a verifier trained on trajectories for inference-time scaling reached 32.0% Verified / 26.0% Lite. — [arXiv 2412.21139](https://arxiv.org/html/2412.21139v2)
- [S] R2E-Gym (Apr 2025): 34.4% pass@1 on SWE-bench Verified with a 32B model; about 51% with hybrid verifiers and best-of-26 selection. — [arXiv 2504.07164](https://arxiv.org/abs/2504.07164)
- [S] SWE-smith (Apr 2025): Qwen-2.5-Coder-32B fine-tuned on 5,016 trajectories reaches 40.2% on SWE-bench Verified; with only 500 successful trajectories, 28.2%. — [arXiv 2504.21798](https://arxiv.org/pdf/2504.21798)
- [P] SWE-RL (Meta; Feb 2025, NeurIPS 2025): RL on open-source software-evolution data (PR histories) with a rule-based similarity reward; Llama3-SWE-RL-70B reaches 41.0% on SWE-bench Verified, described as best for medium-sized (<100B) models at the time, and the abstract says reasoning skills transfer to five out-of-domain tasks (no numbers in abstract). — [arXiv 2502.18449](https://arxiv.org/abs/2502.18449)
- [S] Agent-RLVR (Scale; Jun 2025): RL from verifiable rewards plus teacher-style "guidance" on failed trajectories; Qwen-2.5-72B-Instruct pass@1 on SWE-bench Verified 9.4% -> 22.4% with 817 training environments; 27.8% when a reward model trained on the same data ranks 32 candidates. Guidance improves pass@1 19.8% -> 22.4% and pass@32 34.2% -> 38.4%. — [arXiv 2506.11425](https://arxiv.org/abs/2506.11425)
- [S] Continual fine-tuning and forgetting (general LLMs, not coding): a 2026 experimental study finds PEFT methods such as LoRA "also suffer from catastrophic forgetting during continual fine-tuning". — [LoRA vs O-LoRA study](https://www.researchgate.net/publication/400589207_Mitigating_Catastrophic_Forgetting_in_Fine-Tuned_Large_Language_Models_An_Experimental_Study_of_LoRA_and_O-LoRA)
- [S] Experience replay is described as "a particularly practical solution" for continual LLM fine-tuning because it works at the data level and composes with LoRA (MSSR, arXiv Mar 2026). — [arXiv 2603.09892](https://arxiv.org/pdf/2603.09892)
- [S] "Continual Fine-Tuning of Large Language Models via Program Memory" (arXiv May 2026; Findings of EMNLP 2026): replaces one monolithic LoRA adapter with a library of small specialist weight matrices ("programs") and reports improved retention over other continual-LoRA strategies. Not shown to cover coding tasks. — [arXiv 2605.13162](https://arxiv.org/html/2605.13162)
- [P] Karpathy on the parametric route (Oct 2025): describes sleep as "some process of distillation into the weights of my brain", says "We don't have an equivalent of that in large language models", and sketches a LoRA-like version: "It's not a full-weight neural network. It's just some small sparse subset of the weights that are changed." — [Dwarkesh Podcast transcript](https://www.dwarkesh.com/p/andrej-karpathy)

### Inferences
- The data-efficiency numbers bound what online parametric learning could plausibly buy: hundreds of successful trajectories move a 32B model by ~13 to 20 points from a weak base (SWE-Gym, SWE-smith 500-trajectory result). A single deployment stream of tens of tasks is one to two orders of magnitude below that, so online LoRA from a short deployment stream is unlikely to show measurable gains without replay and many epochs.
- These gains are from weak starting points (9% to 20% base). There is no public evidence that the same recipes improve a frontier closed model already at the top of SWE-bench Verified.
- Cost structure differs in kind from context methods: environment construction plus GPU fine-tuning plus (for verifier results) k-sample inference, versus a few extra LLM calls per task for memory methods.
- For a benchmark that only has a headless CLI, the parametric arm can only be represented (a) as a citation-only reference row, or (b) by an open-weight model behind the same CLI scaffold, which changes the base model and confounds the comparison.

### Gaps
- No primary source found for online LoRA / test-time training of a coding agent on its own deployment trajectories, or for per-repository adapters evaluated on SWE-bench with forgetting metrics. The targeted search returned only general continual-LoRA work.
- No source found on model editing (ROME/MEMIT-style) applied to coding agents.
- No verified compute/dollar cost figures for SWE-Gym / SWE-smith / SWE-RL / Agent-RLVR training runs were collected.
- Whether frontier labs fine-tune on deployment trajectories in production is not publicly documented in anything read this session.
- All [S] numbers in this section came from search summaries of the papers, not from the PDFs directly (except SWE-RL's 41.0%, read on the abstract page).

---

## 3. Hybrid approaches and 2025-2026 frontier-lab developments (sleep consolidation, Nested Learning / HOPE, Titans, product memory features)

### Takeaway
"Sleep"-style consolidation exists in products only at the context level (background jobs that rewrite memory files: Codex memory consolidation, community-reported Claude Code Auto Dream, Letta sleep-time agents); consolidation into weights remains a research proposal. Google's Nested Learning / HOPE (Nov 2025) is the most prominent architectural proposal, but its published evidence is language-modelling and long-context benchmarks, not coding agents.

### Cited Findings
- [S] Google Research "Introducing Nested Learning: A new ML paradigm for continual learning" (blog dated 7 Nov 2025; paper "Nested Learning: The Illusion of Deep Learning Architectures", NeurIPS 2025): treats a model as nested optimisation problems updating at different frequencies, aimed at catastrophic forgetting. HOPE is a self-modifying variant of the Titans architecture with a multi-level Continuum Memory System (Titans updates at only two speeds). Reported: lower perplexity and higher accuracy than modern recurrent models and standard transformers on language modelling and common-sense reasoning, and better long-context needle-in-haystack performance. Author-reported; no independent replication found. — [Google Research blog](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/)
- [M] Titans (Behrouz et al., Google, Jan 2025): a neural long-term memory module updated at test time using a "surprise" (gradient-based) signal. — [arXiv 2501.00663](https://arxiv.org/abs/2501.00663)
- [P] Codex memories perform background extraction and a separate "global memory consolidation" pass with a configurable `consolidation_model`; context-level only. — [OpenAI Codex docs: memories](https://learn.chatgpt.com/docs/customization/memories?surface=app)
- [3P] Claude Code Auto Dream background consolidation of memory files (see section 1); not in official docs read this session. — [Implicator](https://www.implicator.ai/anthropic-adds-auto-dream-to-claude-code-fixing-memory-decay-between-sessions/)
- [P] Letta's skill-learning post frames skills as "continual learning" for CLI agents and says more sleep-time compute could improve the reflection step. — [Letta blog: skill learning](https://www.letta.com/blog/skill-learning/)
- [P] Amodei (Feb 2026) frames long context as the near-term substitute: in-context learning is "kind of like human on-the-job learning, but a little weaker and a little short term"; "A million tokens is a lot. That can be days of human learning."; longer contexts are "an engineering and inference problem", not a research problem. — [Dwarkesh Podcast transcript](https://www.dwarkesh.com/p/dario-amodei-2)
- [P] Sutskever (Nov 2025) describes deployment itself as the learning phase: "you could imagine that the deployment itself will involve some kind of a learning trial-and-error period. It's a process, as opposed to you dropping the finished thing." — [Dwarkesh Podcast transcript](https://www.dwarkesh.com/p/ilya-sutskever-2)

### Inferences
- As of November 2026 the shipped "continual learning" in coding agents is file-based memory plus periodic LLM consolidation. A benchmark's "hybrid / sleep" arm can therefore be faithfully represented without weights as an offline consolidation pass over the memory store between task batches.
- Nested Learning / HOPE and Titans are architecture-level and cannot be baselines in a CLI-only prototype; they belong in related work.

### Gaps
- No primary 2026 announcement from Anthropic, OpenAI, Google DeepMind or Meta of weight-level continual learning for a coding agent was found. Absence of evidence in ~20 searches, not proof of absence.
- No results found for HOPE or Titans on any coding or agentic benchmark.
- The Nested Learning blog was not opened directly (details from a search summary of it); HOPE numeric results were not extracted.
- Release dates/versions for Codex memories and Claude Code auto memory were not established from primary sources (one blog claims Codex CLI v0.128; unverified).
- Secondary reports of an OpenAI frontier-training "pause" in Aug 2026 surfaced in search (CoinDesk, Tech Insider) but were inconsistent with each other and are unrelated to continual learning; not used.

---

## 4. What lab leaders and researchers have said about continual learning (2025-2026)

### Takeaway
There is a clear split. Patel, Sutton, Karpathy and Sutskever describe continual / on-the-job learning as a real missing capability; Amodei says it "might not be a barrier at all" and that long context plus generalisation gets "most of the way there", while also predicting it may be solved in one to two years. No direct Altman quote on continual learning was found.

### Cited Findings (all quotes below were extracted from the linked primary page by an automated fetch; wording should be spot-checked against the page before publication)

**Dwarkesh Patel, essay "Why I don't think AGI is right around the corner" (2 June 2025)** — [dwarkesh.com](https://www.dwarkesh.com/p/timelines-june-2025)
- [P] Section heading: "Continual learning is a huge bottleneck".
- [P] "The lack of continual learning is a huge huge problem."
- [P] "But the fundamental problem is that LLMs don't get better over time the way a human would."
- [P] "How do you teach a kid to play a saxophone? You have her try to blow into one, listen to how it sounds, and adjust."
- [P] On coding agents specifically: "Even Claude Code will often reverse a hard-earned optimization that we engineered together before I hit /compact".
- [P] Forecasts: 50/50 by 2032 that "AI learns on the job as easily, organically, seamlessly, and quickly as a human, for any white collar work."; "If AI progress totally stalls today, I think <25% of white collar employment goes away."
- [S] Counter-view: Nathan Lambert's "Contra Dwarkesh on continual learning" (Interconnects) disputes the framing; content not read. — [Interconnects](https://www.interconnects.ai/p/contra-dwarkesh-on-continual-learning/comments)

**Richard Sutton, Dwarkesh Podcast (26 Sept 2025)** — [transcript](https://www.dwarkesh.com/p/richard-sutton)
- [P] "The large language models are learning from training data. It's not learning from experience."
- [P] "If you need to learn continually, continually means learning during the normal interaction with the world."
- [P] "There's no ground truth in large language models because you don't have a prediction about what will happen next."
- [P] "You have to have goals or you're just a behaving system."
- [P] On context vs weights: "in a continual learning setup, it just goes into the weights."
- [S] Patel's follow-up reflection lists Sutton's gaps as "lack of continual learning, abysmal sample efficiency, dependence on exhaustible human data". — [Patel on X](https://x.com/dwarkesh_sp/status/1973843323279569291)

**Andrej Karpathy, Dwarkesh Podcast (17 Oct 2025)** — [transcript](https://www.dwarkesh.com/p/andrej-karpathy)
- [P] "In my mind, this is more accurately described as the decade of agents."
- [P] "They don't have continual learning. You can't just tell them something and they'll remember it."
- [P] "So I compare the KV cache and the stuff that happens at test time to more like a working memory." / "anything that's in the weights, it's a hazy recollection of what you read a year ago."
- [P] "There's some process of distillation into the weights of my brain." / "We don't have an equivalent of that in large language models."
- [3P caveat] A commenter notes continual learning was one of several listed deficits, not clearly the main driver of his decade estimate, and that Karpathy later clarified his timeline on X. — [EA Forum comment](https://ea.greaterwrong.com/posts/QGfz6MgdzJ2ADyRnF/frozen-skills-aren-t-general-intelligence/comment/yJkriAZeWybpGBsaW)

**Ilya Sutskever, Dwarkesh Podcast (25 Nov 2025)** — [transcript](https://www.dwarkesh.com/p/ilya-sutskever-2)
- [P] "So it's back to the age of research again, just with big computers."
- [P] On humans not being pre-loaded AGIs: "Instead, we rely on continual learning."
- [P] "I produce a superintelligent 15-year-old that's very eager to go." / "They don't know very much at all, a great student, very eager."
- [P] "So you could imagine that the deployment itself will involve some kind of a learning trial-and-error period. It's a process, as opposed to you dropping the finished thing."

**Dario Amodei, Dwarkesh Podcast (13 Feb 2026)** — [transcript](https://www.dwarkesh.com/p/dario-amodei-2)
- [P] "Two, is this idea of continual learning, this idea of a single model learning on the job." ... "There's a good chance that in the next year or two, we also solve that."
- [P] "I think continual learning, as I've said before, might not be a barrier at all." / "I think we may just get there by pre-training generalization and RL generalization."
- [P] "I don't think people would say that learning on the job is what is preventing the coding agents from doing everything end to end." / "Again, I think you get most of the way there without it."
- [S] Earlier (reported as Aug 2025): "We have some evidence to suggest that [continual learning] is another of those problems that is not as difficult as it seems." Secondary source; original venue not verified. — [Transformer: Why is everyone talking about continual learning?](https://www.transformernews.ai/p/teaching-ai-to-continual-learning)

**Sam Altman**
- [S] Oct 2025: stated internal goals of "an automated AI research intern by September of 2026" and "a true automated AI researcher by March of 2028". Not about continual learning as such. — [Altman on X](https://x.com/sama/status/1983584366547829073)

### Inferences
- The disagreement is itself a benchmark motivation: Amodei's claim is empirically testable as "does a long-context / no-memory baseline close the gap to memory-equipped agents on a deployment stream?" A full-history-in-context arm directly operationalises his position; a memory-file arm operationalises Patel's and Karpathy's.
- Sutton's definition ("learning during the normal interaction with the world", going "into the weights") is stricter than what any shipped coding-agent memory does; under his definition context-level methods are not continual learning. The benchmark should state which definition it adopts.
- Patel's /compact anecdote identifies a concrete, testable failure: loss of within-session hard-won knowledge across compaction or session boundaries.

### Gaps
- No verified direct Altman quote about continual learning in 2025-2026 was found.
- Only the first ~100k characters of the Karpathy and Amodei transcripts were processed; later relevant passages may be missing. The Sutskever and Sutton extractions were short and may omit context.
- Quotes were extracted by an automated summariser from the primary transcript pages, so exact punctuation/wording should be confirmed by hand; surrounding context for the Sutskever "Instead, we rely on continual learning." line was not captured.
- No statements from Google DeepMind leadership (e.g. Hassabis) or Meta were collected.

---

## 5. Which mechanisms are cheap enough to be baselines in a CLI-only prototype (no weight access)

### Takeaway
Every context-level mechanism can be approximated with a headless coding-agent CLI plus a per-arm persistent directory and a few extra LLM calls between tasks; no parametric or architectural mechanism can. A credible minimal baseline set is: no-memory, static human-style context file, native agent-written memory, reflection notes, ACE-style delta playbook, retrieval over past trajectories/diffs, self-authored skills, periodic "sleep" consolidation, and a full-history long-context upper/lower reference.

### Cited Findings (feasibility facts tied to sources)
- [P] Native memory can be toggled per arm without code: Claude Code via `autoMemoryEnabled` / `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and redirected per arm via `autoMemoryDirectory`; the index loaded each session is capped at 200 lines / 25KB. — [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
- [P] Codex exposes separate switches for writing vs reading memory (`generate_memories`, `use_memories`) and is off by default, enabling "write-only" and "read-only frozen memory" ablations. — [OpenAI Codex docs: memories](https://learn.chatgpt.com/docs/customization/memories?surface=app)
- [P] Skill learning needs only trajectories plus two LLM steps (reflect, then author a skill file), and optionally verifier feedback; reported to cut cost 15.7% in the trajectory-only setting. — [Letta blog: skill learning](https://www.letta.com/blog/skill-learning/)
- [P] ACE needs no labels, only execution feedback, and uses incremental delta edits to a playbook rather than rewrites; this is implementable as a post-task reflector + curator prompt that appends/edits bullets in a file. — [arXiv 2510.04618](https://arxiv.org/abs/2510.04618)
- [P] Dynamic Cheatsheet is a single persistent, self-curated memory document updated at test time; implementable as one rewrite call per task (and thus also serves as the "monolithic rewrite" arm that ACE says collapses). — [arXiv 2504.07952](https://arxiv.org/abs/2504.07952)
- [S] Static auto-generated AGENTS.md is a known near-null, >20%-cost baseline, which makes it a useful calibration arm. — [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)
- [S] Self-generated skills averaged about -1.3 pp in SkillsBench, so a self-authored skills arm is expected to be weak without feedback. — [arXiv 2602.12670](https://arxiv.org/abs/2602.12670)
- [P] SWE-Bench-CL supplies ready-made metric definitions (forgetting, forward/backward transfer, tool-use efficiency) and a chronological task ordering to reuse. — [arXiv 2507.00014](https://arxiv.org/abs/2507.00014)
- [P] GEPA is an offline optimiser needing many rollouts on a train split (its selling point is "up to 35x fewer rollouts" than GRPO, still many); parametric methods need hundreds of environments (Agent-RLVR: 817; SWE-Gym: 491 trajectories) and weights. — [arXiv 2507.19457](https://arxiv.org/abs/2507.19457); [arXiv 2506.11425](https://arxiv.org/abs/2506.11425); [arXiv 2412.21139](https://arxiv.org/html/2412.21139v2)

### Inferences (proposed baseline ladder; costs are the researcher's estimates, not sourced)

| Arm | Mechanism represented | CLI-only implementation sketch | Extra cost per task | Feasible |
|---|---|---|---|---|
| B0 | No learning | Fresh session, memory disabled, clean checkout | none | yes |
| B1 | Static context file | One-off generated or hand-written CLAUDE.md/AGENTS.md, frozen | none after setup | yes |
| B2 | Native agent memory | Turn on built-in auto memory with a per-arm memory dir | ~0 (built in) | yes |
| B3 | Reflexion-style notes | After each task, one headless call: "given transcript + test outcome, write lessons"; append to file | 1 call | yes |
| B4 | Dynamic-Cheatsheet rewrite | One call that rewrites the whole cheatsheet each task | 1 call | yes |
| B5 | ACE-style playbook | Reflector call + curator call emitting delta edits (add/modify/delete bullets with ids) | 2 calls | yes |
| B6 | Trajectory / diff retrieval | Store past task statements, diffs, outcomes; retrieve top-k by grep/BM25/embeddings into the prompt or expose as searchable dir | retrieval only | yes |
| B7 | Self-authored skills | Reflect -> write SKILL.md files into the agent's skills dir | 2 calls | yes |
| B8 | Sleep consolidation | Every N tasks, a headless call that dedups/merges/prunes the memory dir | 1 call per N | yes |
| B9 | Long-context reference | Concatenate all prior transcripts/diffs into context until the window is full | large token cost | yes, expensive |
| B10 | Oracle memory | Human- or gold-patch-derived notes (upper bound) | none | yes |
| -- | GEPA prompt evolution | Needs a train split and many rollouts | high | only as offline pre-pass |
| -- | LoRA / RL / TTT / model editing / HOPE / Titans | Need weights or new architecture | n/a | no (cite only) |

- With vs without outcome feedback should be a crossed factor for B3, B5, B7 (Letta's +9 vs +15.7 abs gap suggests it dominates).
- Report cost and steps alongside success, with multiple seeds, because the best independent evidence shows null success effects with material cost changes.
- Include probes for the named failure modes: memory size over time (bloat / collapse), a stale-fact injection (repo convention changes mid-stream), and a backward-transfer re-test of early tasks.

### Gaps
- The per-arm cost column is an estimate; no source quantifies these overheads for a CLI harness.
- Whether native auto memory writes reliably in headless (non-interactive) runs was not verified from the docs this session; test before relying on arm B2.
- No published head-to-head of these arms on a single coding stream with multi-seed CIs was found; that is the gap the prototype would fill.
