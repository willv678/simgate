# Shao's 13 Oct feedback: checklist

From the 13 Oct meeting. Each item: what was asked, what was done, where it
is. Paths are under `research/`.

## Visuals (first)

1. [x] **Case cards**: per crash, top-down paths, speeds, gap, braking,
   offset from the human, camera frame, scorer's and triage's verdicts.
   `harness/case_card.py`; 19 cards for the confirmed hardest cases
   (`figures/cards/hardest/README.md`).
2. [x] **Random spot check**: 20 random kept runs as cards
   (`figures/cards/spot/README.md`). 5 counted failures, 10 contacts not
   counted, 5 no contact. Still needs a person to mark each card "makes
   sense / does not". Griffin will mark them, with the four disputed
   hardest cards (14 Oct).
3. [x] **Inner loop at work**: `figures/paper/fig_inner_loop.pdf` (4,668
   launches) and `figures/meeting/self_healing.png` (144 failed launches:
   the agent's fix and how each ended; 129 healed).
4. [x] **Skill contract figure**: `figures/meeting/skill_contract.png`.
5. [x] **System figure**: existing `figures/framework.png` (agent and code
   coloured apart) is the system figure; the contract figure is its inset.
6. [x] **Discovery curves**: confirmed hardest cases against runs, per method,
   median and range over repeats: `figures/discovery_*.png`,
   `figures/meeting/discovery_10hz.png` (`harness/discovery_curve.py`).
   The IV survey found no comparable curve in recent IV papers.

## "Every run works" needs facts

7. [x] **Validity page**: `VALIDITY.md`: what each check verifies; planted
   faults (225 kept with no gate, 0 with gate + audit); 0 physics false
   alarms on 256 clean runs; this week's launch outcomes; what every kept
   run contains (`figures/meeting/outcome_mix.png`).

## Framing: the agent is the contribution

8. [x] **OUTLINE rewritten**: six contributions with evidence and status;
   figure list; must-cite papers and unsafe wording.
9. [x] **Optuna + agent**: new method `hybrid_optuna` (Claude chooses among
   Optuna's suggestions and the rules' confirmations). Tested offline;
   queued on the three studies, 3 repeats.

## Coverage and scenario definition

10. [x] **Coverage**: `SCENARIOS.md` and `figures/meeting/failure_types.png`.
    The studies are braking-shaped, but two thirds of the 1,252 failures
    are steering (into a road user 47%, off the road 16%); the braking
    failure is 10%. Mapped to Level 2 / Euro NCAP tests.
11. [x] **Lane-keeping study** (Euro NCAP LSS): `briefs/categories/lane_keeping.md`,
    planned by Claude and checked (12 straight scenes, plan shift x ego
    speed). Queued with 8 methods.
12. [x] **OpenSCENARIO 1.4**: `harness/to_openscenario.py` writes each study as
    a parameter distribution and its hardest cases as concrete scenarios
    (`scenarios/*.xosc`); all validate against the 1.3 and 1.4 schemas.
    esmini cannot replay AlpaSim scenes (no OpenDRIVE map); noted.
13. [x] **Which parameters**: `SCENARIOS.md` section 3: vary (knobs),
    choose (by scene: lanes, curvature, junctions, actors), not possible.

## Skills

14. [x] **Skills design**: `SKILLS.md`: the seven markdown contracts, each
    with when / what it sees / fixed answers / code check / script; how they
    map to Claude's Agent Skills format. **14 Oct: packaged as real Agent
   Skills** (`research/.claude/skills/`, `harness/package_skills.py`), plus
   an operator skill (`simgate`); routing test in `SKILLS.md`.

## Literature and figures

15. [x] **IV paper figures**: `FIGURES_SURVEY.md` (14 papers; median 6
    figures, 2 tables; framework diagram, failure snapshots, method table
    expected).
16. [x] **Literature refresh**: `LITERATURE_REFRESH.md`. EvoDrive (CoRL 2026)
    and PlannerForge (EMNLP 2026) are the papers to distinguish from; both
    claim "first"; unsafe wording listed in `OUTLINE.md`.

## Carried over

17. [x] **Optuna + repeat results**: done at 10 Hz, 3 replicates each of
    Optuna + repeat and Optuna + AI on the three studies (`FACTS.md`
    "Optuna with confirmation"). Optuna alone is no better than random +
    repeat; Optuna + AI is fastest on pedestrian (21 runs, every replicate).
    2 Hz Optuna arms queued 14 Oct.
18. [x] **AI v2**: `llm_v2`, `hybrid_v2` (`advisor/OUTER_V2.md`): fixed for
    replayed traffic, given each failure's triage, the scenes' facts and
    its own notes. Tested offline; queued on lane keeping (unseen study).
19. [~] **Hard study**: planned (`car_conflicts_3knobs_2hz`, 3 knobs, rare
    failures, 2 Hz); re-queued 14 Oct with 8 methods x 3 repeats under the
    problem 31 rule. Running.
20. [x] **Griffin's score script**: `label_sheet.py score` on his branch:
    agreement and kappa against the scorer and the triage; refuses to run
    until all 60 are labelled.
21. [x] **2 Hz timing**: a 2 Hz rollout takes 47 s of simulation, a 10 Hz
    one 84 s (a whole 10 Hz run about 3 min).

## Found while doing this (needs Will and Shao)

- **Problem 31: retimed cars freeze in their lane.** Settled 14 Oct: the
  scorer does not count a contact with a road user that stopped dead
  (`VALIDITY.md` section 4, FACTS problem 31). Every number, curve and
  figure is now under that rule.
- **Four of the 19 hardest-case cards** have a triage that says the policy
  was not at fault, or unclear. A person should look at them.
