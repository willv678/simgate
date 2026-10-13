<!-- Literature refresh, 13 Oct 2026 (subagent report; EvoDrive and LLM-attacker read in full). -->
# Literature check: agentic AV stress testing on AlpaSim (IEEE IV 2027)

I read EvoDrive and LLM-attacker in full from the arXiv HTML. For the other papers, the table marks how much I read. Some arXiv HTML math was stripped, so any number I could not recover is left out rather than guessed.

## 1. The two target papers (full text read)

### EvoDrive: [arXiv 2606.03678](https://arxiv.org/abs/2606.03678)
Nie, Mei, Tang, He, Deng, Sun, Ma (PolyU, Tongji, McGill/Mila). Accepted at CoRL 2026; v2 is dated 9 Oct 2026.

- **What it does:** LLM agents evolve adversarial scenario-generator programs. These are typed structures (operator graph, parameters, mechanism modules, constraints, lineage), not free code.
  - An actor proposes a bounded edit to a parent generator.
  - Critics check it: structural, attack, realism and isolation. A repair agent revises it if needed.
  - A deterministic validator checks the schema, parent identity, allowed fields, protected resources and whether it compiles. No rollout starts unless it passes.
  - A "world evaluator" that also evolves decides which candidates get simulator budget.
  - A Pareto archive keeps the trade-off between attack and realism. Memory cards and lineage give an audit trail.
- **Simulators and systems under test:**
  - MetaDrive with 500 Waymo scenes (240 for evolution, 100 held out). Ego policies are a fixed IDM and an RL policy.
  - CARLA/SafeBench with 8 NHTSA families × 10 routes. Ego is a fixed learned RL policy.
  - No camera-based end-to-end policy and no neural rendering.
- **LLM:** GPT-5.5 through Codex CLI (xhigh reasoning) for every role. The paper cites Claude Code as an example coding agent.
- **Budget:**
  - MetaDrive: 10 epochs × 20 parallel proposal slots per lineage. That is about 200 proposals, of which about 10 reach the simulator.
  - CARLA: 4 rounds. A typical run used 232 LLM calls, 13.5 h and about US$5.88.
- **Baselines:** 8 parent generators in MetaDrive (CAT, ADV-BMT, AT, SAGE, LLM-Attacker, KING, SEAL, STRIVE) and 4 in CARLA (AdvSim, AT, ChatScene, Human). Ablations: no critic, no memory, non-LLM Pareto search, actor-only with matched LLM calls, attack-only, and OpenEvolve scalar search.
- **Metrics:** Attack (collision rate), realism penalty, ARS, CR, OS, and PF-Area@3 (hypervolume gain).
- **Main numbers:**
  - MetaDrive: PF-Area gain on every family, from +5.2% (LLM-Attacker) to +18.7% (ADV-BMT).
  - CARLA: PF-Area gain of +73.7% to +255.7%.
  - ADV-BMT ablation: full system 31.0±4.2%, actor-only 21.2%, non-LLM Pareto search 10.6%.
  - OpenEvolve gets Attack 0.18 against 0.40 for the full system.
  - The evolving evaluator needs 0.51× the evaluations of random ordering to reach 90% of the hypervolume.
  - SAC fine-tuned on evolved ChatScene scenes: CR falls from 0.163 to 0.106.
- **Overlap with our claims:**
  - **(a) Partial.** It is an unattended agentic loop whose LLM proposals are gated by deterministic code checks. But it evolves generators. It does not plan studies from a question, self-heal failed runs, check that a run's config landed or that its physics is plausible, or write reports.
  - **(b) Partial.** It compares LLM and non-LLM search (non-LLM Pareto, OpenEvolve, call-matched actor-only). These are ablations inside its own framework. Rules, hybrid, random+repeat and Optuna are not tested, and an equal simulator budget is not stated for the non-LLM arm.
  - **(c) None.**
  - **(d) Partial.** It argues that maximising a single scalar attack score gets "hacked" by implausible scenes.
- **Wording to avoid:** "first automated LLM agentic framework for safety-critical AV scenario generation/testing" (EvoDrive claims "first"); "deterministic validation of LLM proposals before simulation" as a novelty; "first comparison of LLM-guided vs. non-LLM search for AV testing."

### LLM-attacker: [arXiv 2501.15850](https://arxiv.org/abs/2501.15850)
Mei, Nie, Sun, Tian (Tongji). Published in IEEE T-ITS 2025.

- **What it does:** Three LLM modules (Initialization, Reflection, Modification) write and refine Python code that picks attacker vehicles. Each iteration takes the best of N candidates, scored by small simulation tests, with memory of earlier code and its success rate. DenseTNT then gives the attacker trajectories that maximise collision likelihood. The resulting scenarios are used for testing and for closed-loop adversarial training.
- **Setup:** MetaDrive with 485 Waymo scenes (385 train, 100 test). The system under test is a TD3 RL policy whose inputs are ego state and 2D LiDAR, plus a log-replay ego. The LLM is a local LLaMA 3.1-8B.
- **Baselines:** Random, Min-TTC and Kinetic Field for choosing the attacker. For training: Replay and Kinetic-II.
- **Metrics:** Attack success (collision) rate, acceleration KL divergence, abnormal-jerk rate, crash rate and route completion.
- **Numbers:**
  - One attacker: success on the log-replay ego is 63.5% (best rule baseline, Kinetic Field: 57.7%). On the RL ego it is 45.0% (best rule baseline, Min-TTC: 37.9%).
  - Two attackers: 90.4% on log replay and 50.8% on RL.
  - Realism: KL 0.0112, jerk 1.84%.
  - Training on its scenarios roughly halves crash rate compared with Replay.
  - The identifier reaches at least 83% success. Its search took an average of 4.42 h.
- **Overlap:** (a) none, since the LLM is one component; (b) weak/partial, an LLM vs. rule heuristic vs. random comparison for one sub-decision, not a budgeted search comparison; (c) none; (d) none. It uses raw collision rate as its headline metric.
- **Wording to avoid:** "first to compare LLM vs rule-based selection in AV testing."

## 2. Other potentially overlapping work (2025–2026)

| Paper | Read | Summary | (a) | (b) | (c) | (d) |
|---|---|---|---|---|---|---|
| **PlannerForge**, Gao, Müller et al. (TUM), EMNLP 2026, [2609.08965](https://arxiv.org/abs/2609.08965) | Main body read | LLM agents (LangChain/Gradio chatbot) cover generation, selection, modification, test execution, analysis, planner tuning and benchmarking. Setting is CommonRoad/SUMO, 2D, with classical planners (Frenetix, MP-RBFN). It claims to be "the first full-lifecycle LLM framework" for scenario-based testing. Chaining the stages end to end keeps 83%/78% of 200 seed queries (commercial/open models). It is driven by a human user, with no adaptive failure search, self-healing or physics-validity gate. | **Strong** (claim) | none | none | none |
| **Teach-to-Crash**, AgenticDev '26 workshop, [2609.27296](https://arxiv.org/abs/2609.27296) | Abstract + key sections | A Teacher LLM steers search when collision/TTC metrics stall; a Student LLM writes JSON scenarios that a validator checks. CARLA Town06; egos are Traffic Manager and TransFuser. Collision hit rate 90.8% vs 79.1% (PAFOT) and 64.0% (ChatScene). It uses a heuristic at-fault/avoidability proxy. No BO or random arm. | partial | partial | none | partial |
| **SPHINX**, Do et al. (UF), [2606.17482](https://arxiv.org/abs/2606.17482) | Abstract + skim | XAI concept analysis plus a VLM critic that diagnoses why the policy fails, then targeted adversarial scenarios for retraining. Tested on several E2E policies (DAVE-2, MILE, RAP...) in CARLA-type simulators. Explains failures, but is not agentic operation. | none | none | none | partial (explanation) |
| **LLM-Falsifier**, ArjomandBigdeli, Zhou et al. (Stony Brook), [2609.20752](https://arxiv.org/abs/2609.20752) | Abstract + setup | LLM used as the optimizer for STL falsification on ARCH-COMP; beats the BO, surrogate and search-based tools on 14/21 specs. Budgets are **not** equal: 100 sims vs ARCH-COMP's 1500, plus a uniform-random arm. Not AV. | none | partial | none | none |
| **Agent-driven Long-tail Sim / SemanticPlan**, Gu, Zhao et al. (Tsinghua/Bosch), [2607.04331](https://arxiv.org/abs/2607.04331) | Abstract + intro | LLMs control surrounding agents in nuPlan for long-tail closed-loop planning tests. The LLM is the traffic, not the test operator. | none | none | none | none |
| **AutonomyLens**, Agrawal et al., FSE Companion '26, [2604.11672](https://arxiv.org/abs/2604.11672) | Abstract only | Early-stage design for UAVs: an LLM agent compiles scenarios, runs simulations, analyses telemetry and creates counterfactual tests from failures. | partial (other domain, no results) | none | none | none |
| **Self-Healing Agentic Orchestrators**, Suresh Babu & Agrawal, [2606.01416](https://arxiv.org/abs/2606.01416) | Abstract only | Recovery limited to a fixed set of failure classes, within budgets, with verification of the recovered output. On fault injection: 98.8% vs 94.5% retry-only. General tool agents, not simulation. | partial (self-healing concept) | none | none | none |
| **NeuroNCAP**, ECCV 2024, [2404.07762](https://arxiv.org/abs/2404.07762) | Abstract/summary | NeRF closed-loop safety testing of E2E planners with NCAP-style scenarios. The scenarios are fixed, with no search or agent. | none | none | **partial (prior art for c)** | none |
| **HUGSIM**, Zhou...Geiger, Liao, [2412.01718](https://arxiv.org/abs/2412.01718) | Abstract only | Real-time 3DGS closed-loop simulator with a benchmark of more than 400 scenarios from KITTI-360, Waymo, nuScenes and PandaSet. | none | none | partial | none |
| **Driving in Corner Case**, [2512.16055](https://arxiv.org/abs/2512.16055) | Abstract only | Images from a flow-matching generator plus an adversarial traffic policy, in closed loop with UniAD and VAD. | none | none | partial | none |
| **OmniSCS** [2607.09764](https://arxiv.org/abs/2607.09764), **DecoupleGS** [2608.01761](https://arxiv.org/abs/2608.01761) | Snippets only | 3DGS-based editable, safety-critical closed-loop testing for E2E stacks. | none | none | partial | none |
| **AlpaSim users**: Alpamayo-R1 [2511.00088](https://arxiv.org/abs/2511.00088), RoaD [2512.01993](https://arxiv.org/abs/2512.01993), ECO [2609.31383](https://arxiv.org/html/2609.31383v1), OPTED [2609.20756](https://arxiv.org/abs/2609.20756) | Snippets only | Use AlpaSim to evaluate or train policies. ECO reports VaVAM scene-score gains there. None does agentic or adversarial testing. | none | none | partial (same platform) | none |
| **Scientific Agent Skills** [2609.00065](https://arxiv.org/abs/2609.00065), **Formal Skill** [2605.19604](https://arxiv.org/abs/2605.19604) | Snippets only | Markdown skill libraries for research agents. Formal Skill argues markdown skills lack enforced state and completion checks. | partial (skills/contracts) | none | none | none |

Searches that found nothing:
- No paper running LLM-driven failure search or an agent-operated campaign on AlpaSim, NuRec or another neural-reconstruction simulator.
- No AV paper comparing LLM, rules, hybrid, random and Optuna/TPE at equal simulation budget.
- No AV paper showing that raw collision counts reorder search methods.

These gaps rest on web search, not exhaustive arXiv crawling.

## 3. Must-cite papers and unsafe wording

**The three papers we most must cite and distinguish ourselves from:**
1. **EvoDrive.** It also runs an unattended LLM loop with code-checked proposals and LLM vs non-LLM ablations. We differ in four ways: we operate the whole testing pipeline (study planning, self-healing of failed runs, checking each run's config and physics, explaining crashes, reporting) rather than evolving generators; we compare six selection strategies at an explicitly equal budget under one validity gate; we use neural-reconstruction real scenes; and our system under test is a camera-to-trajectory E2E policy, not MetaDrive/CARLA state-based policies.
2. **PlannerForge.** It claims to be the first full-lifecycle LLM testing framework. We differ because ours runs unattended on adaptive failure search, with self-healing and validity checks, on a closed-loop E2E policy in reconstructed real scenes, whereas PlannerForge is a human-driven chatbot over 2D CommonRoad with classical planners and no search comparison.
3. **LLM-attacker** (or Teach-to-Crash as the newest LLM-steered collision search). They put an LLM inside one step of scenario generation and score by collision rate. We evaluate the LLM as a test-selection policy against rules, hybrid, random and Optuna arms at equal budget, and show that raw collision counts can rank those methods wrongly.

**Wording that is now unsafe:**
- "First LLM agent covering the full / end-to-end AV testing pipeline": PlannerForge claims this, and AutonomyLens claims something similar for UAVs. Safer: "unattended, closed-loop agentic operation of a stress-testing campaign on a neural-reconstruction simulator with an end-to-end policy," hedged as "to our knowledge."
- "First fully automated / agentic LLM framework for safety-critical scenario generation": EvoDrive claims this.
- "First to compare LLM vs non-LLM (or vs rule-based) test generation": EvoDrive, LLM-attacker and Teach-to-Crash all do partial versions. Claim only the specific design: six strategies, equal simulation budget, the same validity gate.
- "Validated / verified LLM actions" as new in itself: EvoDrive has deterministic validators, Teach-to-Crash has a validator, and the self-healing orchestrator paper has bounded failure classes with verification. Claim instead the specific combination: run-level checks that the config landed and the physics is plausible, plus a fixed menu of self-healing skills.
- "First closed-loop testing in neural reconstruction": NeuroNCAP and HUGSIM came first. Claim "first agent-driven failure search on AlpaSim/NuRec" only with "to our knowledge."
- "LLM beats BO": not supported by prior AV work. LLM-Falsifier's comparison used unequal budgets, and that is a point we can make in our own favour.
