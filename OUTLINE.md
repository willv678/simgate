# Outline

IEEE IV 2027, six pages. Rewritten 13 Oct 2026 for the paper Shao framed on
6 Oct: accelerated stress testing of a driving policy, with an AI agent in a
rule-guided search loop. The 29 Sep outline (runtime assurance for an
LLM-operated batch) is in git history; its gate results are now section 3's
support, not the claim.

Schedule: experiments run 13-24 Oct and freeze on Sat 24 Oct; Will writes
25-28 Oct; draft 2 Nov. After the freeze, runs only tighten numbers already
in a claim (more replicates), never add a claim.

## Claims, evidence, status

| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | Guided search with an AI finds a policy's hardest cases more reliably than rules, random search and a standard optimiser, on the same budget and validity gate | 3 category studies x rules, hybrid, llm, random + confirmation, optuna + confirmation; 3-5 replicates (`METHODS.md`, FACTS "2 Hz complete") | have all but Optuna (queued 13 Oct) and replicates 4-5 |
| 2 | The AI's advantage grows as failures get rarer and the space larger | the hard study (below) | **missing; the deciding experiment** |
| 3 | Counting every collision flag ranks the methods wrong | problems 25, 29, 30: up to half the car-scene "failures" were rear-endings by replayed cars or contacts begun before the hand-off; lead vehicle's winner changed | have it |
| 4 | The loop keeps every run valid unattended | 3,708 launches since 6 Oct, 97% kept; the gate; 30 problems met (FACTS table) | have it |
| 5 | What the search found in VaVAM | ego speed, not pedestrian timing, is the stressor; the left drift (`DRIFT.md`) and the mirror test (`MIRROR.md`) | have it |
| 6 | The automatic failure judgement agrees with a person | Griffin's 60 blind labels (`research-griffin`, `label_sheet.py score` still to write) | 10 of 60 |

If claim 2 does not hold, the paper leads with 3-5 and states 1 as measured.

## The hard study (claim 2)

- More knobs at once: actor time shift, actor speed, ego speed at hand-off
  (3 knobs; the method studies vary 2).
- Scenes where failures are rare at the recording. 2 Hz suits this: VaVAM
  fails less at its designed rate (`HZ.md`), and it answers "which rate".
  Rate waits on Shao (asked 13 Oct).
- Methods: rules, hybrid, llm, random + confirmation, optuna + confirmation,
  and v2 of hybrid and llm (below). 5 replicates, about 15 GPU hours.
- Do not tune v2 on this study: v2 is built on the three method studies and
  evaluated here.

## AI proposer v2 (new proposers; v1 arms stay reproducible)

What llm and hybrid see now (FACTS "2 Hz complete"): run results and
per-setting ranges only. v2 adds:
- the prompt corrected for replayed traffic (near-deterministic replicates;
  the v1 prompt says traffic is sampled);
- the triage's crash explanations and the tagger's scene facts (lead gap,
  cut-in time, pedestrian distance);
- a short note carried between rounds (hypothesis, what to test next).
Any change to confirmation applies to every method, not only v2.

## Figures

1. The loop (`figures/framework.png`, simplified).
2. Confirmed hardest cases by method and study, with replicates
   (`figures/meeting/by_scene.png` style).
3. Where each method looked (`WHERE.md`): why rules stall.
4. The hard study: the gap between guided and random against failure rarity.
5. The left drift (`figures/meeting/drift_simple.png`) and the mirror test.
Table: problems met (FACTS), grouped; counts before and after the
policy-attributable definition.

## Related work (`LITERATURE.md`, 6 Oct; refresh before writing)

- Accelerated testing: NADE, D2RL, importance sampling for cut-ins, AST,
  BO-based falsification. We do not estimate a crash rate; we find and
  confirm the hardest cases on a fixed budget.
- LLM scenario testing: ChatScene, LeGEND, TARGET, OmniTester, SoVAR,
  LLM-attacker, EvoDrive, PlannerForge, LEADE (an LMM builds scenarios from
  videos offline; its search is a fuzzer with no LLM). Check LLM-attacker
  and EvoDrive closest, where an LLM acts inside the loop. They generate
  scenarios in
  CARLA/LGSVL/SUMO/MetaDrive; none compares rules, LLM-only and hybrid
  choice of the next test on one budget under one validity gate, and none
  runs a closed-loop end-to-end policy in a neural-reconstruction simulator.
- Flaky simulation tests (Osikowicz 2025, Amini 2023, Chance 2022): our gate.

## Statistics

Per study, not pooled: confirmed count per arm, methods compared within a
study (Mann-Whitney or a permutation test), runs to goal where every arm
reaches it. The pooled first look (FACTS) mixes studies and treats the two
rates of one study as independent.

## Limits to state

One policy (VaVAM; Alpamayo does not fit 24 GB). Replayed traffic does not
react. Retiming moves only recorded actors. Unprotected left: 2 of 250
scenes. Intersection: one replicate, no separation.
