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

## Packaged as Claude Agent Skills (14 Oct)

Shao, 13 Oct, asked whether these could be real Claude skills. They now are:
`harness/package_skills.py` writes each contract as an Agent Skill under
`research/.claude/skills/` (where Claude Code loads a project's skills),
plus an operator skill:

| skill | from | what it is for |
|---|---|---|
| `simgate` | `advisor/OPERATE.md` | operate SimGate: an "if this, run this" table from a person's request to the command (`simgate doctor / new / plan / queue / status`, the report, method comparison, case cards, OpenSCENARIO export), and what the agent never does |
| `simgate-diagnose` | `CLAUDE.md` | choose a recovery for a FAILED run |
| `simgate-plan` | `PLAN.md` | brief to study plan |
| `simgate-propose` | `OUTER.md` (+ `v2.md`) | the next round of runs |
| `simgate-audit` | `AUDIT.md` | audit a finished batch |
| `simgate-triage` | `TRIAGE.md` | explain one failure |
| `simgate-tag-scene` | `TAGS.md` | tag a scene |
| `simgate-report` | `REPORT.md` | answer the brief |

Each `SKILL.md` is the Agent Skills frontmatter (name; a description saying
when to use it), the contract unchanged, and the scripts that check and act
on its answer. `advisor/` stays the source the harness calls, so every run
so far and every run until the freeze sees exactly the same prompt;
`test_package_skills.py` fails if the package drifts from it.

**Does Claude choose the right skill by itself?** (`harness/skills_routing.py`,
`skills_routing.json`). Claude Code was given only the eight skills (no
system prompt from us, no tools but Skill) and one real SimGate input on
stdin, with the same instruction for every input: "use the SimGate skill
that fits it". The answer then went through the same code check the harness
applies. 22 inputs, $3.29:

| inputs | count | loaded the right skill first | answer passes the code check |
|---|---|---|---|
| failed runs (every kind of failure and recorded recovery, 3 of each kind at most) | 16 | 16 | 16 |
| briefs (lane keeping, cut-in, the three-knob study) | 3 | 3 | 2 |
| a round of a study after 20 runs (cut-in, lead, pedestrian) | 3 | 3 | 3 |

- 12 of the 16 recoveries are the one the harness's own call chose. The
  other 4: CLEANUP_ENV where the harness chose RESTART_CLEANUP on three Docker
  port conflicts (the skill's reason: the port is held by another run's
  leftovers, which only CLEANUP_ENV removes), and on one environment failure
  where the harness chose HALT. All 4 pass the check.
- The rejected plan (lane keeping) put the policy's defaults (delay, noise,
  controller) under `fixed`, which allows only traffic, retiming, compare and
  the control step. The check caught it, as it is there to.

So the same markdown works two ways: as a fixed contract the harness hands
to a headless call (the experiments), and as skills an agent picks up by
itself (another lab's agent, or a person driving SimGate from Claude Code).
