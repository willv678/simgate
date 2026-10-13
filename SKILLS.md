# How the agent's skills are designed

Shao, 13 Oct: can the markdown that drives the agent be structured ("if
this, run this script") and shown in the paper as a design? It already is.
Every job the agent does is a markdown **contract** in `harness/advisor/`,
and every contract has the same five parts:

1. **When** Python calls the agent (one headless `claude -p` call; a fresh
   context each time).
2. **What it sees**: named input fields, and whether it has read-only tools.
3. **What it may answer**: a fixed menu or a JSON schema. Free text only
   where a person reads it.
4. **Who checks the answer**: plain code, before anything happens.
5. **Who acts**: a script, never the agent.

## The seven contracts

| contract | called when | sees | answers | checked by | acted on by |
|---|---|---|---|---|---|
| `CLAUDE.md`: diagnose | a run is FAILED | status, config, error lines, machine at timeout; read-only tools | one skill: RE-RUN, CONFIGURE, CLEANUP_ENV, RESTART_CLEANUP, HALT | `validate_diagnosis.py` (e.g. no CONFIGURE of a measured knob, CLEANUP_ENV at most once) | `recover.py` |
| `PLAN.md`: plan a study | a brief is submitted | the brief, the knob catalogue, the tagged scenes | a plan (scenes, knobs, rounds, goal) as JSON | the plan check (real knobs and scenes, budget cap, a well-formed goal) and a person | `study.py` |
| `OUTER.md`: choose the next runs | each round of a study | every run so far, per-setting failure ranges, the goal's status | this round's runs as JSON | `knobs.rejection` (legal values, candidate scenes); for hybrid, only the rules' candidates | `outer.py` queues them |
| `AUDIT.md`: audit a batch | a batch has finished | the batch's runs, configs, metrics, a reference run | quarantine flags, proposed rules | `promote.py` (a rule must catch the flagged runs and no clean one), then a person enacts it | `rules.py` on every later run |
| `TRIAGE.md`: explain a failure | a run failed | frames before the failure, metrics | cause from a fixed list, policy at fault, one paragraph | schema; counts come from code | the report and the cards |
| `TAGS.md`: tag a scene | a scene is added | three frames | categories from a fixed list, with a reason | compared with rules from the recorded tracks; a person checks a sample | `scene_tags.json` |
| `REPORT.md`: answer the brief | a study ends | the results table by setting id | findings citing setting ids | the report guard refuses hand-written counts | `report.md` |

## Why the design matters (the paper's point)

- **Finite menus make the agent checkable.** The diagnose contract has five
  skills, so every answer the agent could give was tried against every
  failure state: 0 violations in 3,822 transitions, at most 3 launches per
  run, no cycles (`verify_supervisor.py`, FACTS "Exhaustive check").
- **The agent proposes; code decides.** No contract lets the agent act. The
  inner loop's 144 failed launches this week went through the diagnose
  contract: 129 healed and kept, 15 stopped for a person
  (`figures/meeting/self_healing.png`).
- **What the agent learns becomes code.** An audit's proposed rule, once
  admitted, runs on every later run with no model call
  (`rules/promoted.json`).
- **Numbers never come from the model.** Reports cite setting ids; Python
  writes the counts beside them.

Figure: `figures/meeting/skill_contract.png`.

## Agent Skills packaging

Claude Code's Agent Skills format is a folder with a `SKILL.md` (name,
description, instructions) and scripts. Each contract above maps onto it
directly: the contract is the `SKILL.md`, the checker and the actor are its
scripts. Packaging them that way would let another lab load SimGate's
skills into their own agent; it is a packaging change, not a behaviour
change, and is left until the experiments freeze so the runs stay
comparable.
