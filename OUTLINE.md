# Outline

IEEE IV 2027, six pages. Rewritten 13 Oct 2026 after Shao's feedback that
day (`CHECKLIST.md`): **the contribution is an AI agent that runs AV stress
testing continuously and can be trusted to**: it plans, runs, heals, checks
and explains, and it discovers corner cases with whatever search sits
underneath (rules, its own choice, Optuna). Accelerated discovery is the big
picture; a new optimisation algorithm is not the claim. The 29 Sep outline
(runtime assurance for an LLM-operated batch) is in git history.

Schedule: experiments run 13-24 Oct and freeze on Sat 24 Oct; Will writes
25-28 Oct; draft 2 Nov. After the freeze, runs only tighten numbers already
in a claim, never add a claim. At 10 Hz an arm takes about 2.5-3 h (two at
once), so about 16 arms a day.

## Contributions, evidence, status

| # | Contribution | Evidence | Status |
|---|---|---|---|
| 1 | An agent that runs AV stress testing end to end, unattended, on a closed-loop end-to-end policy in a neural-reconstruction simulator | 4,668 finished launches 6-13 Oct, 4,542 kept (97.3%, one cutoff with the self-healing counts); 144 failed launches healed or stopped by the agent (129 kept); every check and its evidence in `VALIDITY.md` | have it |
| 2 | Skills as structured markdown contracts with code-checked actions (finite menus, checked by code, executed by scripts), packaged as Claude Agent Skills | 7 contracts + an operator skill (`SKILLS.md`, `research/.claude/skills/`); Claude picks the right skill by itself on real inputs (`skills_routing.json`); exhaustive check of the diagnose menu (3,822 transitions, 0 violations); planted faults: 225 kept with no gate, 0 with gate + audit | have it |
| 3 | The agent discovers and confirms corner cases on a small budget | 3 studies x 6 methods x 3 replicates at 10 Hz (`FACTS.md` "Optuna with confirmation"); discovery curves (`figures/discovery_*.png`, `figures/paper/fig_discovery.pdf`). Car scenes, confirmed of 30 (contacts with cars that stopped dead not counted, problem 31): rules 6, random + repeat 10, Optuna + repeat 13, AI picks 13, Optuna + AI 13, hybrid 17 (hybrid vs rules p 0.006; vs random p 0.08; AI picks vs rules 0.10, Optuna + AI vs rules 0.15). Pedestrian: Optuna + AI reaches the goal first in every replicate (21 runs; rules 25, random 32) | have it at 10 Hz; claim is "the AI choosing among rule candidates beats rules, and Optuna alone does not beat random", not "AI beats random" (problem 31). Lane keeping (unseen study, 8 methods x 3, done 15 Oct): every free-choosing AI arm (AI picks, v2, Optuna + AI; 17-21 runs to goal) beats every random and Optuna + repeat arm (25-32), rules never reach it; hybrid trails there (rule candidates). Hard study (3 knobs, rare failures, 8 methods x 3, done 16 Oct): confirmed of 15, AI picks v2 14, AI picks 12, Optuna + AI 9, random + repeat 4, rules 0; only free-choosing AI arms reached the goal (pooled vs random/Optuna p 0.006). 2 Hz Optuna arms done 17 Oct: Optuna alone never beats random + repeat, AI choosers lead or tie in every study. All queued experiments done 17 Oct, a week before the freeze |
| 4 | Results a person can check | case cards for every confirmed hardest case and 20 random runs (`figures/cards/`); what every kept run contains (`figures/meeting/outcome_mix.png`); Griffin's blind labels | cards done; spot-check verdicts and labels pending |
| 5 | What it found in VaVAM | two thirds of failures are lane keeping (steered into a road user, left the road), not braking (`figures/meeting/failure_types.png`); the left drift and the mirror test; ego speed is the pedestrian stressor | have it |
| 6 | Lessons (issues met) | 33 problems (FACTS table): naive counting ranks methods wrong (problems 25, 29, 30); replayed traffic rear-ends the ego in 27-38% of car-study runs | have it |

## Figures (survey of IV papers: `FIGURES_SURVEY.md`; median 6 figures, 2 tables)

1. **System**: the agent's two loops, code and agent coloured apart
   (`figures/framework.png`), with a skill contract inset
   (`figures/meeting/skill_contract.png`).
2. **The inner loop at work**: launch outcomes and self-healing
   (`figures/meeting/launch_outcomes.png`, `self_healing.png`).
3. **Case cards**: two or three hardest cases, top-down paths, speeds, gap,
   camera (`figures/cards/hardest/`). Every IV paper surveyed shows the
   failures found.
4. **Discovery curves**: confirmed hardest cases against runs, per method
   (`figures/discovery_*.png`). None of the surveyed papers has this curve.
5. **Coverage and findings**: failure types per study
   (`figures/meeting/failure_types.png`) and the drift.
Table I: methods x metrics (confirmed, runs to goal, model time).
Table II: issues met and self-healing, grouped.

## Scenario definition and coverage (`SCENARIOS.md`)

Studies stated as OpenSCENARIO 1.4 parameter distributions
(`scenarios/*.xosc`, schema-valid). Covered: AEB car-to-car rear, cut-in,
pedestrian; lane keeping (LSS) queued; crossing traffic next; turn across
path not possible (2 scenes).

## AI proposer v2 and the hard study

v2 (new proposers, v1 stays reproducible): prompt corrected for replayed
traffic; triage explanations and scene facts in its input; a note carried
between rounds. Built on the three method studies, evaluated on studies it
has not seen (lane keeping, and a 3-knob study with rare failures).
Lower priority than the figures and validity evidence above.

## Related work (`LITERATURE.md`, refreshed 13 Oct: `LITERATURE_REFRESH.md`)

Must cite and distinguish:
- **EvoDrive** (CoRL 2026): unattended LLM agents evolve adversarial
  scenario generators, proposals checked by a deterministic validator, LLM
  vs non-LLM ablations; MetaDrive/CARLA, state-based egos. We operate the
  whole testing pipeline (plan, heal, check each run, explain, report),
  compare six selection strategies at an equal budget under one validity
  gate, on neural-reconstruction real scenes with a camera-to-trajectory
  policy.
- **PlannerForge** (EMNLP 2026): claims the first full-lifecycle LLM testing
  framework; human-driven chatbot, 2D CommonRoad, classical planners, no
  search comparison, no self-healing or validity gate.
- **LLM-attacker** (T-ITS 2025) / **Teach-to-Crash** (2026): an LLM inside
  one step of scenario generation, scored by collision rate.
Also: NADE, D2RL, AST, BO falsification; NeuroNCAP and HUGSIM (closed loop
in neural rendering came first); LEADE (LMM builds scenarios offline, no LLM
in its search); self-healing orchestrators; markdown skill libraries.

**Unsafe wording**: "first" anything about full-pipeline LLM testing
(PlannerForge), agentic scenario generation (EvoDrive), LLM vs rule
comparison (EvoDrive, LLM-attacker), validated LLM actions, or closed-loop
neural-reconstruction testing (NeuroNCAP). Safe, with "to our knowledge":
unattended agent-operated stress-testing campaigns on a
neural-reconstruction simulator with an end-to-end policy; six strategies
at an equal budget under one validity gate; collision counting that
reorders methods.

## Statistics

Per study: confirmed count per arm, methods compared within a study
(Mann-Whitney or permutation), runs to goal where every arm reaches it.

## Limits to state

One policy (VaVAM; Alpamayo does not fit 24 GB). Replayed traffic does not
react. Retiming moves only recorded actors; road geometry is chosen, not
varied. Unprotected left: 2 of 250 scenes. Pedestrian failures often far
from the recording (rendering less certain, flagged).
