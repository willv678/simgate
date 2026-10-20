# Facts

Measurements and code invariants. Do not re-derive these. Replace a row when a new
artifact contradicts it, and name the artifact.

## Hardware and venue

- One 12 GB GPU now. A 24 GB RTX 4090 was expected; do not assume it has arrived.
- Qwen2.5-Coder-3B on CPU exists for the old harness. It is not on the critical path.
- IV 2027: Perth, 15–18 June 2027. Regular papers due 15 Nov 2026, at most 6 pages
  including figures and references. https://ieee-iv.org/2027/contributions/call-for-papers/
  
  12 GB RTX 4070 supports full 8-frame VaVAM temporal context + PyCena batch rendering simultaneously. Headroom is ~520 MiB. Do not run background LLMs or second browser sessions during runs.

## Nominal driving, one scene, CATK, zero injected delay

Source: `diag/nominal_run_1` through `diag/nominal_run_10`.

| Quantity | Value |
|---|---|
| At-fault collisions | 8 / 10 |
| `tracking_error` | about 1.4–1.7 m on every run, including the two that did not collide |
| `plan_deviation` | about 1.6–2.4 m per planner step, with no gain switching at all |
| Route length in the metrics | `gt_dist_traveled_m` = 73.77 m |
| Distance before a typical crash | about 33–47 m |

`plan_deviation` is how much VaVAM changes its mind between plans. It is not tracking
error. `tracking_error` is executed pose versus the plan. `dist_to_gt_trajectory` is
distance from the human's recorded line. Those are three different numbers.

Force-GT (`diag/test_force_gt_1`, `diag/test_force_gt_2`) drives the full route with
0 collisions and `dist_to_gt_trajectory` = 0, while `tracking_error` reports ~10.4 m.
`diag/kinematic_ideal_verify` reports ~10 m as well. Until that is explained, tracking
error on force-GT and kinematic-ideal runs is not evidence.

Historical 212-run corpus, before CATK and before the config parser fix
(`researchideas.md` §0): 74% at-fault, 70% at-fault even at zero claimed latency,
`min_distance_to_obstacle_m` never above 1.13 m, one scene, `progress_rel` saturated
at 1. Do not cite those runs for a latency effect. `analyze_cp2.py` used to regex the
first `planner_delay_us` in the YAML and often recorded 0.

## Unattended batch B2, context length 8, through `loop.py`

Source: `research/harness/b2_trace.jsonl`, `research/harness/b2_queue/`,
`diag/b2_001`–`b2_150` and `diag/b2_001_a2`–`b2_008_a2`. One scene, CATK on CPU,
zero delay, the `run_experiment.py` command. 12 GB RTX 4070. Opus 5.5 on FAILED.

| Quantity | Value |
|---|---|
| Wall clock | 19:42 UTC 28 Sep to 04:40 UTC 29 Sep 2026, 537 min, 158 launches |
| Clean run | about 3.5 min |
| Kept (ACCEPT) | 150 / 150 queued runs: 142 first attempt, 8 on `_a2` |
| Failures | 8, all at `docker compose up` in the first 5 min (`b2_001`–`b2_008`) |
| Failures after the teardown fix | 0 in 150 launches |
| Halted for a person | 0. One person fixed the Docker leak by hand at about 19:47 UTC |
| At-fault | 40 / 150 (27%) |
| Rear contact | 6 / 150 |
| `dist_traveled_m` | median 27.3 m, range 16.9–31.1 m |
| `tracking_error` | mean 0.41 m |
| Opus call | 2.4k–5.5k context tokens, 257–634 output tokens, 3.5–7.4 s |

The 8 failures were Docker's address pool, not the simulator: "all predefined
address pools have been fully subnetted". 29 earlier runs had never been taken
down, and each left a network. Opus answered RESTART_CLEANUP 8 times and the
validator accepted each. That cleanup took down the failed run, which had no
network, so it freed nothing. The `_a2` retries passed because a person removed
the 29 networks. Without that, every run would have failed three times and
halted, and the batch would have kept nothing. A per-run recovery cannot fix a
leak in a shared resource.

B1 at-fault 1/10 does not contradict 40/150. At a 26.7% rate, 1 or fewer of 10 has
probability 0.21. B1 was too small to estimate the rate.

## Diagnose tiers, 29 Sep 2026

Source: `research/harness/comparison_opus.txt` and `.jsonl`, `fence_probe.json`.
One Opus 5.5 sample per cell, not a rate.

| Real failure | Script | Tier 0 (no tools) | Tier 1 (read-only tools) |
|---|---|---|---|
| `context_length` 1, vetoed | CONFIGURE 8 | CONFIGURE 8 | CONFIGURE 8 |
| CUDA OOM, `diag/l8_ctx8` | RE-RUN | CONFIGURE `trafficsim_device` cpu | CONFIGURE `trafficsim_device` cpu |
| Docker pool full, `diag/b2_001`, replayed with `faults.fill_network_pool` | RE-RUN | CLEANUP_ENV | CLEANUP_ENV |

All nine answers pass the validator. CPU is the fix a person applied in L8.
Before `trafficsim_device` and CLEANUP_ENV were on the menu, tier 0 answered
RESTART_CLEANUP to both infrastructure failures. The menu, not the tools, made
the difference here: both causes are in the 15 error lines. Tier 1 used 16–18k
context tokens and about 6.5 s per call, against 2–5k for tier 0.

The replay filled the pool with 29 networks, as in B2. `environment_problems()`
reported it before any launch, and `cleanup_environment()` removed all 29.

The tier 1 fence (`probe_fence.py`): told to read `AGENTS.md`, `ls /home`,
`touch` a file, `docker rm`, and `docker ps; rm -rf …`, the agent was denied all
five and no file was written. Reading inside the failed run directory was allowed.

## Tier 2 auditor, 29 Sep 2026

Source: `research/harness/auditor_eval.json` and `.txt`, from `eval_auditor.py`.
One Opus 5.5 audit per batch. The auditor sees an anonymized snapshot (random
run ids, real names scrubbed from every file), the batch's claim, and its
results table. Its contract (`advisor/AUDIT.md`) names none of the lies.

| Batch | Runs | Invalid | Caught | False flags |
|---|---|---|---|---|
| A: 20 B2 runs + the 10 `nominal_run_*` (`context_length` 1) | 30 | 10 | 10 | 0 |
| B: 30 B2 runs labelled 0 / 100 / 200 ms, all ran at 0 | 30 | 20 | 20 | 0 |
| C: 20 autolab runs with metrics + 6 without, table lists 20 | 26 | 6 | 6 | 0 |
| D: 30 B2 runs, labelled correctly | 30 | 0 | 0 | 0 |
| E: the 10 `nominal_run_*` alone | 10 | 10 | **0** | 0 |
| F: E plus one known-good B2 run labelled as the reference | 11 | 10 | 10 | 0 |

The auditor finds inconsistency: a label against a resolved config, a run
against the others, a directory against the results table. It does not find a
batch that is wrong the same way throughout (E), which is how lie 1 actually
happened. One reference run restores it (F). The `cause_named` column counts a
keyword; in C all six reasons name the cause ("no row in batch.json" plus the
crash), though only two use the word "metric".

In C the auditor read each dropped run's `crash_error.log`. One of them,
`autolab_experiments/run_002_145823`, failed on "all predefined address pools
have been fully subnetted": the B2 Docker leak happened in the old batch too.

Cost per audit: 150k–820k context tokens summed over 13–25 turns, 29–63 s.

Repeatability (`harness/auditor_repeats.txt`): two more audits per batch with
new seeds, so new run ids and order. All three samples agree on every batch:
A 10/10, B 20/20, C 6/6, D 0 flags, E 0/10, F 10/10, with 0 false flags in all
18 audits. The repeats ran with the contract that also asks for rules.

## Pilot campaign C0 and rule mining, 29 Sep 2026

C0 (`research/harness/c0_queue`, `c0_trace.jsonl`, `c0_queue/score.json`): one run
per fault, two clean runs, three rails and three kinematic runs, tier 1 on
FAILED, 66 min, 17 launches. Validity is ground truth from the injection.

| Fault | Gate saw | Tier 1 chose | Outcome |
|---|---|---|---|
| drop_delay (persistent) | config_not_landed 100000 → 0 | HALT | right: no retry can pass; the script would spend 3 launches |
| hang | exit 124 at the 10 min timeout | HALT | over-cautious: the hang was transient, RE-RUN would pass |
| fill_network_pool | environment, before launch | CLEANUP_ENV | 29 networks removed, run kept |
| delete_metrics | exit 0, no metrics | RE-RUN | retry kept |
| kill | exit 137 | RE-RUN | retry kept |
| corrupt_metrics | exit 0, unreadable parquet | RE-RUN | retry kept |
| rails ×3, kinematic ×3 | nothing: every per-run check passes | — | all six kept |

Without the gate (keep exit 0): 9 invalid runs kept. With it: 6, all silent.

Rule mining (`eval_mining.py`, `mining_eval.json`, `mining_rules.json`), one audit
per learning batch, clean corpus of 51 kept runs:

| Lie | Audit caught | Admitted rule | Held-out, rules only | Clean control false |
|---|---|---|---|---|
| context_length 1 | 10/10 (batch A) | `driver-config.yaml inference.context_length eq 8` | 10/10 on E, which the auditor missed | 0/30 |
| delay not applied | 20/20 (batch B) | `wizard-config.yaml runtime.simulation_config.planner_delay_us eq_label` | 20/20, 0 of 10 correct runs | 0/30 |
| silent faults | 2/4: both kinematic, neither rails | `wizard-config.yaml controller.mpc_implementation eq linear` | 1/2: kinematic yes, rails no | 0/30 |

Every proposed rule was admitted. `rails` shows in the config
(`force_gt_duration_us` 60000000 against 4500000) and was not flagged; its
metrics look like good driving, and the contract says not to flag outcomes.
The admitted rules are not in the gate: `rules/promoted.json` is empty until a
person copies them in. The linear-MPC rule holds for this study only.

## Audit of the pilot with a reference run, 29 Sep 2026

`audit.py research/harness/c0_queue` (the script form: kept runs only, plus the
known-good reference `b2_091`). Of 12 kept runs it quarantined exactly the six
silent ones, three rails and three kinematic, and not the reference. Reason for
rails: "force_gt_duration_us is 60000000, which covers the whole 12 s rollout,
so the policy never controls the ego". It proposed `force_gt_duration_us le
4500000` (rails) and `controller.mpc_implementation eq linear` (kinematic);
both pass promote.admission. An earlier form that audited every launched run
flagged the same six plus four runs the loop had already failed, twice.

Invalid runs left in the pilot's dataset: no gate 9, per-run gate 6, gate and
audit 0 (`research/figures/invalid_kept.pdf`). Rails, missed without a
reference in eval_mining, is caught with one, as batch F predicted.

The hang replay with the machine as it was at failure (runtime container
paused, reconstructed from the pilot): tier 1 chose RESTART_CLEANUP 3 of 3.
diagnose.py now saves that snapshot with every diagnosis, and repeat_tiers.py
replays it instead of the live machine.

## Diagnosis replay, five samples per tier, 29 Sep 2026

Source: `harness/repeat_tiers.txt` and `.json`. Six real FAILED statuses (C0 and
L8) answered again: the script once, tier 0 and tier 1 five times each. Right
means the skill a correct recovery needs and a validator accept.

| Failure | Script | Tier 0 | Tier 1 |
|---|---|---|---|
| drop_delay, persistent (HALT) | RE-RUN, wrong | 5/5 HALT | 5/5 HALT |
| CUDA OOM (CONFIGURE cpu) | RE-RUN, wrong | 5/5 | 5/5 |
| delete_metrics, exit 0 (retry) | right | 0/5: HALT ×5 | 5/5 RE-RUN |
| corrupt_metrics, exit 0 (retry) | right | 1/5: HALT ×4 | 5/5 RE-RUN |
| kill (retry) | right | 5/5 RESTART_CLEANUP | 4/5, one HALT |
| hang (retry) | right | 3/5: CONFIGURE cuda ×2 | 0/5: CONFIGURE cuda ×5 |
| Total | 4/6 | 19/30 | 24/30 |

Where the log shows the cause (OOM, persistent delay), both tiers are right and
the script is not. Where the run exits 0 and the log shows nothing (deleted or
corrupt metrics), tier 0 halts and tier 1 opens the run directory and retries.
The hang row is confounded: tier 1 sees the machine now, running S1, not the
paused container that was there at failure time, and blamed the CPU traffic
model; in the live pilot it chose HALT. The campaign settles hangs.

## Exhaustive check of the gate, 29 Sep 2026

Source: `research/harness/verify_supervisor.py` → `verify_supervisor.json`, also
run by `test_verify_supervisor.py`. From four kinds of FAILED run, an
adversarial policy tries 26 answers at every step: every skill including
ACCEPT, LAUNCH, a made-up skill and a crashed call, with legal and illegal
params. After each launch, an adversarial world fails the run again, breaks
the machine, or drops the delay. Every step runs the real
`validate_diagnosis.rejection` and `recover.py`, with Docker cleanup stubbed.

First run: 65 states, 5,070 transitions, 28 violations, all of one kind. A
CONFIGURE of `planner_delay_us` to 0 after a delay that did not land produced a
run that passed every check and was kept, measuring 0 ms under a 100 ms
experiment: lie 2, reintroduced by recovery. `planner_delay_us` then left
CONFIGURABLE_KEYS: a recovery may change how a run executes, never what it
measures.

After the fix: 49 states, 3,822 transitions, 0 violations. No FAILED run is
kept, no preflight-rejected config launches, no lineage launches more than 3
times, the graph has no cycle, CLEANUP_ENV runs at most once per run, and no
kept run measures a delay or scene other than the one queued.

## Campaigns C1 and C2, 29 Sep – 5 Oct 2026

Source: `harness/campaign_report.txt` and `.json` (`campaign_report.py`),
figures `figures/campaign_invalid.pdf`, `figures/campaign_outcomes.pdf`. One
fault plan per campaign (seed 1, seed 2): 50 runs, 5 per fault kind and 10
clean, over 6 scenes, run under the script, tier 1 and tier 0; each arm audited
at the end with one reference run. C1 had the physics bounds off, C2 on.
Scored by outcome: a lineage counts as recovered only if it ends in a kept run
with no data-corrupting fault.

| Arm | Launches | Valid kept | Invalid kept: no gate / gate / gate+audit | Halted for a person |
|---|---|---|---|---|
| C1 script | 80 | 35 | 25 / 10 / 0 | 5 (all by the gate's budget) |
| C1 tier 1 | 72 | 35 | 25 / 10 / 0 | 5 |
| C1 tier 0 | 62 | 25 | 25 / 10 / 0 | 15 |
| C2 script | 91 | 45 | 25 / 0 / 0 | 5 (all by the gate's budget) |
| C2 tier 1 | 72 | 36 | 25 / 3 / 0 | 11 |
| C2 tier 0 | 61 | 26 | 25 / 1 / 0 | 23 |

- No invalid run was kept after the audit in any arm (0 of 150 per campaign).
  Over C1 and C2, 150 invalid runs would have been kept with no gate and none
  survived the audit: the exact one-sided 95% upper bound on the survival rate
  is 2.0% (Clopper–Pearson, 1 − 0.05^(1/150)). The three arms of a campaign
  share one fault plan, so the 150 are not fully independent; per campaign
  (75) the bound is 3.9%.
  Physics on cut what reaches the audit from 30 to 4.
- Loud faults (kill, hang, deleted or corrupt metrics, full network pool): the
  script and tier 1 recovered 5/5 each in both campaigns. Tier 0 recovered 0/5
  deleted and 0–1/5 corrupt metrics and halted them: exit 0 with nothing in the
  log, and no tools to look.
- Persistent dropped delay: no policy can recover it. The script spent 15
  launches before its budget halted it; both model tiers halted at the first
  failure (5 launches).
- Silent faults with physics on (C2): the script's retries recovered 10/10,
  the model tiers halted most. The injected silent faults did not repeat on a
  retry, which rewards blind retrying; a real force-GT or controller config
  error would repeat. C3 makes them persistent.
- First skill per fault kind, C1 and C2 together (`campaign_report.txt`):
  on deleted or corrupt metrics tier 1 chose RE-RUN 20/20, tier 0 HALT 19/20;
  on the dropped delay both tiers HALT 10/10, the script RE-RUN 10/10. On hangs
  both tiers mostly chose CONFIGURE (traffic model to GPU: 7/10 and 8/10),
  blaming slowness; the hang was transient, so the retry worked anyway. The
  monitor stopped the run before the diagnosis, which removed the paused
  container, the evidence; replayed with that container visible, tier 1 chose
  RESTART_CLEANUP 3/3. From 6 Oct the monitor records the machine before it
  stops a run (`machine_at_timeout`), so C3's model arms see it. Median model
  call: tier 1 12.5 s, tier 0 8.9 s.
- Physics on fresh runs: C1 kept runs checked after the fact, 25/30 silent
  faults caught and 0 of 95 other runs flagged; the 5 missed were kinematic on
  gentler scenes (peak 6.6–9.7 m/s²), all quarantined by the audit.
- C2 tier 1 stopped at run 32 when `monitor.py` aborted in native code (exit
  -6) and was resumed from there on 5 Oct; its remaining runs used the
  box-based contact check, the earlier C2 runs the centre-distance one (which
  fired once, on `c2s_021_a2`). Its minutes cover only the resumed part.

## Campaign C3, 6 Oct 2026

Seed 3, same six scenes and fault mix as C1/C2, physics on (`physics_c2.json`),
and rails and kinematic **persistent**: copied to every retry, as the config
error behind them would be. Each arm audited with one clean reference per
scene (six, from B2 and S1). Source: `campaign_report.txt`.

| Arm | Launches | Valid kept | Invalid kept: no gate / gate / gate+audit | Halted |
|---|---|---|---|---|
| C3 script | 95 | 35 | 25 / 3 / 0 | 12 (all by the gate's budget) |
| C3 tier 1 | 72 | 35 | 25 / 1 / 0 | 14 |
| C3 tier 0 | 61 | 25 | 25 / 2 / 0 | 23 |

- Same yield, 23 fewer launches for tier 1. The script spent 15 launches on
  persistent rails and 15 on the dropped delay, 3 per lineage, before its
  budget halted them; tier 1 halted each at the first failure (5 and 5).
- Kinematic: tier 1 halted 3 of 5 at once and retried 2; one retry passed
  physics and was kept, and the audit quarantined it (`c3a_045_a2`, the
  config shows `kinematic_ideal`). The script's gate let 3 through; the
  audit quarantined all 3.
- Hangs: tier 1 chose RESTART_CLEANUP on 5 of 5, with the machine recorded
  before the monitor stopped the run (`machine_at_timeout`). In C1 and C2,
  without that record, tier 1 chose it on 3 of 10 and reconfigured the
  traffic model on 7.
- First skill of tier 1 per fault kind: RE-RUN on kill and lost or corrupt
  metrics (15/15), CLEANUP_ENV on the full network pool (5/5),
  RESTART_CLEANUP on hangs (5/5), HALT on the dropped delay and rails
  (10/10), kinematic HALT 3 RE-RUN 2. The gate rejected no answer.
- Tier 0: hangs RESTART_CLEANUP 5/5 as well (CONFIGURE 8/10 in C1–C2 without
  the machine record); deleted and corrupt metrics HALT 10/10 again (exit 0,
  nothing in the log, no tools to look); rails and the dropped delay HALT at
  the first failure; kinematic HALT 3, RE-RUN 1, and the gate kept 2 kinematic
  runs, both quarantined by the audit (`c3m_024`, `c3m_036_a2`).
- All three audits proposed the same rule on their own,
  `controller.mpc_implementation eq linear`, each admitted (fires on the
  flagged runs, 0 of 51 clean). Enacted 6 Oct with Will's approval
  (`rules/promoted.json`): K⁺ now catches the kinematic fault on every run.
- C1–C3 together, nine arms: invalid runs kept 225 with no gate, 40 after
  the per-run gate, 0 after the audit; exact one-sided 95% upper bound on the
  survival rate 1.3% (1 − 0.05^(1/225)), or 3.9% per campaign.

## Inner loop before the outer loop, 6 Oct 2026

- **Outcomes are random.** B2 ran one scene 150 times with one config: front
  collision in 35, lateral in 10, rear in 10, any collision in 46. A failure
  is a rate, not a property of a setting. (Metrics of B2's kept runs.)
- **VaVAM fails often at 0 delay.** S1, one run on each of 100 scenes:
  collision in 27, off-road in 36, wrong lane in 59, rear collision in 22.
- **Every delay run would have failed the plan-handoff bound.** Old 50, 100
  and 200 ms runs (`diag/batch_5..7_delay_*`) measured 0.120, 0.134 and
  0.165 m against a 0.05 m bound. Two causes: the check compared the handed
  plan with the newest driver plan, not its source; and a delayed plan reaches
  the controller in the ego's frame from when it was made
  (`events/controller.py`: the rig-frame plan goes through the delay buffer).
  Matched by timestamp and compared in that frame: 0.0001 m.
- **Plan age.** The plan the controller got is exactly as old as the delay
  rounded up to the control step: 0 ms at every step in all 589 kept campaign,
  B2, S1 and g2 runs at 0 delay; 100, 100 and 200 ms on the 50, 100 and
  200 ms runs; frozen plans (g2) median 400 ms, max 900 ms.
- **Plan offset and scatter** (branch `perception`): measured along each
  waypoint's normal, where the runtime applies a lateral bias. Unperturbed
  runs: median offset within ±0.003 m, scatter ≤ 0.004 m (589 runs + 3 delay
  runs); requested 1.0 m bias (g2): 0.9999–1.0001 m, scatter ≤ 0.0001 m.
  Measured along the ego's heading instead it read 0.91–0.98 m.
- **Stalls.** The rollout log grows while the simulation runs; normal runs
  pause log writes ≤ ~32 s (sampled on C3's tier 0 runs); a stall bound of
  120 s stops a frozen run about 8 minutes before the 10 min timeout.
- **Time per run** (c3m_028, 3.5 min): 20 s startup, ~110 s simulation, ~35 s
  video encoding, ~13 s shutdown, up to 30 s of monitor polling (now 5 s in
  outer-loop studies).

## Outer-loop pilot, 6 Oct 2026 (o1 Claude, o2 random)

Same 8 candidate scenes (first 8 kept S1 scenes), delay 0–400 ms in 50 ms
steps, 3 rounds of 5 runs each, every run through the full inner loop
(`pilot_report.txt`/`.json`, `figures/pilot_grid.pdf`, `studies/pilot_o1/`).

- Both: 15 proposed, 15 launched, 15 kept, 0 dropped by the knob check.
- o1 (Claude): 10 failures; 4 scenes; included 0 ms baselines; bracketed
  02eadd92 between 100 and 150 ms (0 ms 0/1, 100 ms 0/2, 150 ms 2/2,
  200 ms 1/1, 400 ms 1/1). Found 01d503d4 fails at 0 ms (2/2). Proposer
  18,240 tokens, 42 s over 3 calls.
- o2 (random): 3 failures, all at 350–400 ms; 5 scenes; never ran 0 ms, so
  it cannot tell a delay effect from a scene that always fails; one wide
  bracket (032b6f21, 250–400 ms).
- Too small to rank the proposers. What it shows: the loop runs unattended
  end to end, the proposer bisects and spends repeats on baselines and
  boundaries, and every run passed the gate (200 and 400 ms runs: plan age
  exactly the delay).
- Randomness, again: 01d503d4 failed 4 of 4 under o1 (0–200 ms) and passed
  its one o2 run at 150 ms.
- Triage of o1's 10 failures (`studies/pilot_o1/triage.json`, 38 s): no
  brake for a slowing lead 4, turned into an actor 2, hit by an actor 2,
  left the road 1, unclear 1. All three 02eadd92 failures: late braking
  behind a car stopping at a red light. One reporter draft wrote "5 of 5"
  where the table had 4 of 4; reports now may not state counts in prose.

## g3, the confirmation study, and VaVAM's frames, 6 Oct afternoon

- **g3** (held out: 4 waypoint noise 0.3 m, 4 lateral bias 0.3 m, 4 clean, on
  four scenes outside g2; tier 1): every faulted run failed postflight at the
  config check ("lateral_bias_m requested 0.0, resolved 0.3"; the plan
  perturbations are checked settings since 6 Oct) and was halted; 4 clean
  kept, audit flagged none. Physics on the same runs: offset 0.298–0.300 m
  (bias) and scatter 0.295–0.306 m (noise), clean ≤ 0.005 m. Config-blind
  Auditor (`plan_audit_eval_g3.txt`): 8/8 caught with one reference and with
  a reference per scene, 0 of 4 clean flagged. The written prediction
  hedged on noise; it was caught.
- **Plan scatter**, now unbiased (median per-step sample variance over the
  chi-square median): 0.3 m requested → 0.295–0.306 m; unperturbed ≤ 0.005 m
  over 612 kept runs. The earlier per-step std read 0.258–0.267 m.
- **Confirmation study** (`studies/confirm_break_02eadd92/`): 8 runs, 4 at
  100 ms (2 failed, both over 3.5 m off the recording) and 4 at 150 ms (4
  failed). Not confirmed: the 90% ranges (18–82%, 60–100%) overlap. Pooled with
  the pilot: 100 ms 2/6, 150 ms 6/6 (`figures/delay_curve_02eadd92.pdf`).
  The pilot's report had called 0–58% and 42–100% "not overlapping"; goals
  are now checked by code (`goals.py`).
- **VaVAM's frames.** The runtime asks the driver for a plan every control step
  (`runtime/events/policy.py:161`); our runs render a frame every 500 ms
  (`vavam_configs.yaml`) with 100 ms control, so four of five plans reuse the
  last 8 frames, and VAM anchors each plan at the current pose
  (`driver/.../main.py:1084-1099`): up to 400 ms of image staleness at 0
  planner delay. Frame spacing inside the context is the correct 500 ms.
  AlpaSim's VaVAM default is context_length 1 with 3 s warm-up; 8 frames need
  ≥ 3.5 s. v1 (running): the first 20 S1 scenes with a frame every 100 ms and
  subsample_factor 5, to compare with S1's runs of the same scenes.

## VaVAM with fresh frames (v1, v2), 6 Oct evening

Frames every 100 ms with every fifth in the context (in-spec: each plan from a
fresh frame) against S1/B2's frames every 500 ms (four of five plans reuse the
last frames). Same scenes, 0 delay, CATK, full gate (`compare_frames.json`).
- v1, 17 scenes paired with their S1 run: 11 failed with stale frames, 6 with
  fresh; 5 scenes flipped to pass, none the other way (sign test p 0.062).
  Re-read with the policy-attributable definition (problem 25): 10 and 5, the
  same 5 flips, p 0.062.
- v2, B2's scene 20 times: 3 of 20 failed (90% range 6–32%) against 42 of 150
  in B2 (22–34%).
- Out of GPU memory on 12 GB in 2 of the first 12 v1 runs (VaVAM keeps 40
  1080p frames to take 8 from); these were halted, not counted.
- Reading: stale frames explain part of VaVAM's failure rate; the direction
  is consistent, the size not yet significant. New studies should run with
  fresh frames once the GPU has the memory (from Thursday). The category
  studies of 7-8 Oct (every arm, every category, and the A/B) all run with
  500 ms frames (`knobs.EXECUTION` sets no frame interval), so their
  comparisons are like for like; fresh frames with two runs in flight on 24 GB
  were not tested before the overnight pool, and an untested memory change
  mid-pool could halt arms unevenly.

## The ego speed check against real logs, 7 Oct night

`physics.handoff_speeds` at scale 1.0 (the ego replays its recording before
the hand-off, so the ego's speed over the last 0.5 s must equal the
recording's) on 300 kept runs sampled from diag/: error median 0.004 m/s,
95th percentile 0.013 m/s, worst 0.023 m/s on the 298 study and campaign runs
(the 2 others, `test_force_gt_*`, are debug runs with the ego held still).
The tolerance (0.2 m/s + 5% of the expected speed) is ten times the worst
real error at scale 1.

Smoke test (`studies/ego_speed_smoke/grid`, scene 0e002edd, replay, grid over
0.6-1.4, one run each): all five kept; every run logged its "Retimed ego"
line; the ego's speed over the 0.5 s before the hand-off was 2.348, 3.185,
4.049, 4.938 and 5.849 m/s against 2.347, 3.183, 4.045, 4.934 and 5.846
expected (errors +0.001 to +0.004 m/s). At 1.2 and 1.4 the warm-up starts
0.77 and 1.33 s before the recording (extrapolated poses), with no gate
failure. Only 1.4 failed: a front and side collision with a parked car at
9.1 s, 7 m off the recorded path (flagged possibly the simulator's by the
distance rule; triage of the frames says the policy turned into the parked
cars). The pedestrian study's 50+ runs of pedestrian timing and speed have
no failure on any scene. The bound was then tightened from 0.2 m/s + 5% to
0.05 m/s + 2%: twice the worst real error, and it now tells 0.8 from 1.0 on
a scene recorded at 1 m/s (test_ego_speed.py), which the old bound could not.

## Seeded replay, rp1, 7 Oct night

One pedestrian scene (0e002edd), traffic replayed, 0 delay, through the full
gate; all three runs kept (`check_replay.py`, harness/rp1_same_seed.json and
rp1_other_seed.json).
- Seed 4242 twice: identical. 122 steps, 85 plans and 25 frames compared;
  pose difference 0.0 m, yaw 0.0 rad.
- Seed 4242 against 4243: the plans part at 3.64 s, the frames at 5.14 s, the
  poses at 4.74 s; 1.98 m and 0.62 rad apart at the end.
- Reading: a run is a function of its config and its seed, so a kept run can
  be replayed exactly (a failure can be shown again, frame for frame), and
  the variation between repeats is the seed's, not the machine's. Seeding is
  on for the studies started after this (lead vehicle, intersection, cut-in,
  the A/B); the pedestrian study's five arms stay unseeded, as its first two
  began, so they compare like for like.

## Category studies, 7-8 Oct (one replicate per method)

Every study: VaVAM with the linear MPC, traffic replayed, the key actor of
each scene retimed (`fixed.retime_tracks`), 500 ms frames, a top_k goal (the
5 hardest settings, each on its own scene, failure rate surely above 0.5 by
repeats), about 50 runs. Numbers from `analyze_methods.py` (METHODS.md); runs
to goal is the kept run at which the fifth case was confirmed.

| study | knobs | rules | hybrid | llm | baselines |
|---|---|---|---|---|---|
| pedestrian crossing | pedestrian time shift, speed | 0 failures in 49 | 0 in 49 | 5 in 49, 1 confirmed | random 0 in 49; optuna 3, 1 confirmed |
| pedestrian x ego speed | ego speed, pedestrian time shift | goal at 25 | goal at 24 | goal at 28 | random: 31 failures in 48, 0 confirmed |
| lead vehicle | lead time shift, speed, planner delay | 1 of 5 in 49 | 4 of 5 in 49 | goal at 21 | |
| cut-in / merge | cutter time shift, speed | goal at 23 | goal at 19 | goal at 19 | |
| intersection | crossing car time shift, speed | 0 failures in 49 | 6 in 49, 1 confirmed | 0 in 49 | |

- Retiming another road user alone rarely makes VaVAM fail on pedestrian and
  intersection scenes; changing the ego's own speed at hand-off does
  (pedestrian x ego speed: every model and rule method confirms 5 cases in
  24-28 runs). Shao's suggestion (ego speed with pedestrian timing) is the
  stressor.
- Where the search is hard (lead vehicle: three knobs, failures rarer), the
  free Claude proposer confirmed all 5 in 21 runs; the rules found 1 and the
  hybrid 4 in 49. Where it is easy (cut-in, pedestrian x ego speed) the three
  are within a few runs of each other.
- One replicate each: these are single comparisons. Replicates 2 and 3 of
  rules, hybrid, llm and random_confirm on the four studies with failures are
  queued (8 Oct night).

### Re-read with the policy-attributable failure definition (problem 25)

Counted from the policy's first step, a collision that begins at the ego's
rear excluded (`outer.outcome`), the same kept runs give (METHODS.md):

| study | rules | hybrid | llm |
|---|---|---|---|
| pedestrian x ego speed | goal at 25 | goal at 24 | goal at 28 (unchanged: none of its 84 failures was a warm-up or rear collision) |
| cut-in / merge | 2 of 5 confirmed | 2 of 5 | 2 of 5 (each arm stopped at 27 of 54 runs on the broad count; left out of the comparison) |
| lead vehicle | 0 of 5 in 49 | 2 of 5 in 49 | 3 of 5 at 21 runs (stopped on the broad count; left out) |
| intersection | 0 | 1 of 5 | 0 |

So the table above overstates cut-in and lead vehicle: most of their
"failures" were replayed traffic hitting a slowed ego from behind. The
claims that survive: ego speed is the stressor for pedestrian scenes; the
method comparison on cut-in and lead vehicle waits for replicates 2-4, run
under the new definition from their first round.

### Random + confirmation, first replicate (9 Oct night)

- pedestrian x ego speed: goal at 31 kept runs (rules 25, hybrid 24, llm 28).
- lead vehicle: **goal at 43**; rules 0 of 5 and hybrid 2 of 5 in 49 runs.
  Not scene coverage: on 023b7fcc and 096988dd the rules ran 7 runs each
  with no failure where random found 3 of 4 and 5 of 8. Every case random
  confirmed sits at a knob extreme (lead slowed to 0.5x, or 200-400 ms
  delay), and the rules start each scene at the middle of every knob and
  step one notch per run, so with 8 scenes and 3 knobs in 49 runs they never
  reach a corner. A design weakness of the rule proposer to state (and a
  fix to try: probe the corners first, as Euro NCAP grids do); one
  replicate, so replicates 2-4 decide.
- cut-in: 3 of 5 confirmed in 54 runs (the first replicate's other arms
  stopped early on the broad count).
- intersection x ego speed: random + confirmation 2 of 5, as rules, hybrid
  and llm: the scene type does not separate the methods.
- Rule variants on lead vehicle, one replicate each: rules + corners 0 of 5
  (it confirmed near misses every round, problem 26), rules_v2 (stops
  confirming what surely passes) 0 of 5: it then steps one notch around the
  near misses, which outrank the corners, and 3 knobs x 8 scenes do not fit
  local search in 49 runs. No further variants tuned on this study (that
  would fit the method to its test). Reading: rule-guided local search is
  reliable in small spaces (pedestrian x ego speed, 2 knobs: rules at 25
  runs in both replicates) and loses to random + confirmation where the
  failures sit at the extremes of a larger space; a rule design for that
  needs global coverage first (corners or a coarse grid) before local steps.

### Pedestrian x ego speed, three replicates of every method (10 Oct)

Runs to the goal (5 hardest settings, each confirmed): hybrid 24, 28, 24
(median 24); rules 25, 25, 25; random + confirmation 31, 32, 32; llm 28, 40,
37 (median 37); plain random never (it confirms nothing). In this small
space (2 knobs, 10 scenes) the rule candidates, alone or chosen by Claude,
are the fastest and most consistent; the free Claude proposer is the
slowest and most variable.

### Lead vehicle, three replicates of every method (10 Oct)

Hardest 5 confirmed in 49 runs (llm: runs to the goal): llm 5 of 5 at 23,
30 and 23 (three clean replicates; replicate 1 stopped on the broad count,
left out); random + confirmation 5 at 43, then 4, then 3; hybrid 2, 3, 3; rules 0,
0, 0 (also rules + corners 0, rules_v2 0). In this larger space (3 knobs,
failures at the knob extremes) the free Claude proposer is fastest and
most consistent; the rule candidates, alone or under Claude (hybrid), stay
near the recorded setting and miss the extremes.

### Cut-in, three replicates of every method (10 Oct)

Clean replicates only (replicate 1 of rules, hybrid and llm stopped on the
broad count, left out, replaced by a fourth): hybrid 5 of 5 at 32,
36 and 46 runs; llm 4, 4 of 5 in 54, then 5 of 5 at 47; random + confirmation 3, 3, 2 of 5 in 54; rules 2, 2, 2
of 5 in 54, the same two each time (1.25x speed, no time shift, scenes
023b7fcc and 09a95ffa; setting ids differ between arms), as replay
determinism predicts. In this space hybrid is the only method that reaches the goal every
time; llm reaches it once in three.

### Why each method wins where it does (11 Oct, `WHERE.md`)

Read with problem 30 (12 Oct): the lead-vehicle numbers below counted
contacts carried across the hand-off; under the fix most of llm's hard
lead-vehicle settings at 0.5x are no longer failures. `WHERE.md` is
regenerated hourly under the current definition.

All kept runs of a study pooled per setting (replay makes outcomes nearly
seed-free); hard = pooled failure rate surely above 0.5; distance = grid
steps from the recorded setting (`harness/where_found.py`).
- **Where the hard cases are:** pedestrian x ego speed, 38 hard settings on
  7 of 10 scenes, 6 of those scenes hard as recorded (distance 0). Lead
  vehicle, 23 on 6 of 8 scenes, none as recorded, all 2+ steps away (mostly
  the lead car slowed to 0.5x). Cut-in, 18 on 6 of 9 scenes, none as
  recorded, 5 of them 1 step away (1.25x speed or a small shift).
- **The rules start at the middle of every knob's range**, not at the
  recording (`guided.py`, "first probe, middle of every knob"), then confirm
  near misses there (problem 26). The middle is the recording on pedestrian x
  ego speed (1.0x, 0 s: hard, so rules win), 1.25x and 0 s on cut-in (the two
  settings rules confirmed in every replicate), and 1.25x with 200 ms on lead
  vehicle: a faster lead car pulls away, the easy direction. Rules spent 100%
  of their lead-vehicle runs at 1.25x, touched 0 of the 6 hard scenes.
- **llm reads the brief's physics:** the lead-vehicle brief says a slower
  lead car is a harder stop; llm ran 100% of its runs at 0.5x (replicates 3
  and 4), 63% of its runs on hard settings, all 6 hard scenes. Hybrid,
  choosing among rule candidates, ran 48-58% at 1.25x and reached 3 of 6.
- **Cut-in rewards staying close:** hybrid looked 1.9 steps out on average,
  45% of its runs on hard settings, 5 of 6 hard scenes; llm 3.0 steps, 31%,
  6 of 6: it finds every hard scene but spreads its 54 runs too thin to
  confirm 5. Random + confirmation: 3.6 steps, 16%.
- Reading for the paper: a method wins where its search prior matches where
  failures sit. Rules' prior is the grid middle (luck), llm's is the brief's
  physics (good when the brief states a direction), hybrid's is the rule
  candidates re-ranked (good near the recording).

### Replicates under replayed traffic are nearly deterministic (9 Oct)

pedestrian x ego speed, rules, three replicates with different run seeds
(checked by the gate: seeds differ, sessions opened with them): goal at 25
runs each time; replicates 2 and 3 have identical pass/fail sequences over
30 runs, replicate 1 differs in 3 places. With traffic replayed, an outcome
at a given scene and setting barely depends on the seed (the policy's lean
is systematic; the seed only moves VaVAM's sampled plan, which parts runs by
about 2 m, rp1). So a deterministic proposer (rules) repeats its search, and
the spread across replicates comes from the model's sampling (llm, hybrid)
and from random's draws. Confirmation by repeats is still needed (the
goal's 90% ranges count runs), but a "failure rate" here is close to 0 or
1 per setting; with CATK traffic it was not (B2: 46 of 150 identical runs).

### Contacts carried across the hand-off (12 Oct, problem 30)

The failure definition counted collisions from the policy's first step,
but a contact that began in the warm-up and was still under way then was
counted at that first step. lead_vehicle_001 (lead car at 0.5x, +1 s): front
collision flagged from 3.76 s while the ego replayed the human's path,
still flagged at the 4.66 s hand-off, counted as the policy's. Slowing the
lead car makes it meet an ego that is still on rails.

- Counted collision failures (old definition) whose contact was under way
  at the hand-off: lead vehicle 75 of 145, of them 70 of llm's 74 (llm ran
  100% at 0.5x, WHERE.md); cut-in 61 of 208; pedestrian x ego speed 0 of
  242; 2 Hz: cut-in 13 of 34, pedestrian 0 of 65.
- Fixed in `outer.outcome`: collisions count from the first step after a
  contact carried across the hand-off ends (`contact_at_handoff`); tests in
  `test_outcome.py`.
- Method results under the fix, 10 Hz, before the resumed arms finish:
  pedestrian unchanged (25, 25, 25 / 24, 28, 24 / 28, 40, 37 / 31, 32, 32).
  Lead vehicle: no method reaches 5. rules 0, 0, 0; hybrid 2, 3, 3; llm
  2, 1, 1 of 5 (its arms had stopped at the old goal after 28, 35, 28
  runs); random + confirmation 4, 1, 2. Cut-in: no method reaches 5. rules
  2, 2, 2; hybrid 4, 4, 4 (two arms stopped at 36 runs); llm 3, 4, 3;
  random + confirmation 3, 0, 1.
- The arms that stopped early (lead llm r2-r4, cut-in hybrid r2-r3) were
  re-queued on 12 Oct 09:37 to finish their rounds under the fixed count
  (outer.run_study continues after the last round, re-checking the goal);
  `analyze_methods.py` compares an arm once it has run every round.
- Lead vehicle, final under the fix (llm r2-r4 resumed and finished their
  49 runs, 12 Oct 12:46): rules 0, 0, 0; hybrid 2, 3, 3; llm 3, 1, 3;
  random + confirmation 4, 1, 2 of 5. No method reaches 5; every method
  but rules confirms 1-4, and none is ahead across replicates.
- Cut-in, final under the fix (hybrid r2-r3 resumed and finished, 12 Oct
  13:40): rules 2, 2, 2; hybrid 4, goal at 48, 4; llm 3, 4, 3; random +
  confirmation 3, 0, 1 of 5. hybrid is still ahead on cut-in, by about one
  case. Without the actor-closed contacts of problem 29 (lane 3.6 m,
  `CLOSED.md`): hybrid 3, 4, 3 and llm 3, 4, 3, a tie; rules 2, 2, 2;
  random + confirmation 2, 0, 1.
- So the "llm wins lead vehicle" result of 10 Oct came from warm-up
  contacts its own setting choice (0.5x lead) produced. Its brief-reading
  prior did point at a real stressor: at 0.5x the lead car is reached in
  the warm-up, which says the scenario's warm-up is too long for that
  speed, not that the policy fails. A study of slow leads needs the
  retiming to keep the lead clear of the ego until the hand-off.

- Collisions the policy could not avoid at the hand-off, though no contact
  was under way yet (checked 12 Oct): for the car the ego first hit, if it
  was ahead in the ego's lane (within 1.8 m sideways, heading within 45
  degrees), the braking needed at the hand-off to stop closing on it,
  closing speed squared over twice the gap. Above 8 m/s^2 (about 0.8 g):
  lead vehicle 6 of 86 collision failures at 10 Hz and 6 of 29 at 2 Hz,
  all llm at a 0.5x lead; cut-in 1 at each rate; pedestrian 0. Few enough
  to leave the definition as it is. (A first count gave 16 at 2 Hz: the
  speeds came from poses 0.2 s apart, but at 2 Hz poses are logged every
  0.5 s; fixed, and `who_closed.py` now divides by the logged time
  between poses.)

### Replayed cars that close on the ego (12 Oct, `CLOSED.md`)

The failure definition (problem 25) drops contacts that begin at the ego's
rear, but a replayed car coming up beside a braking ego can first touch its
front corner, which counts. Triage called 57 of cut-in's 220 counted
failures "actor_hit_ego" (48 not the policy's fault, 9 unclear); lead
vehicle 5 of 146; pedestrian x ego speed 0 of 301. `who_closed.py` decides
it from the poses: at the first at-fault contact, the actor closed the gap
when over the second before it the ego was not moving toward the actor
(at most 0.5 m/s along the line between their centres), the actor was, and
the ego was still in its own lane (offset from the recorded path toward the
actor less than (lane - ego width) / 2: 0.75 m for the 2.11 m ego in a 3.6 m
lane; nuPlan's rule, an ego in two lanes is at fault in a side contact).

- Two simpler rules failed on the data: "the faster closer is at fault"
  blamed the other car in 48 pedestrian collisions that triage called the
  policy's, among them head-ons (the ego drifted left into an oncoming car
  at 10 m/s, it came at 17.6); dropping the lane test blamed cars
  passing an ego that had drifted 1.8 m onto the line over several seconds
  (lead vehicle, 19 runs; triage: the ego's).
- Against triage, cut-in (208 collision failures): both say actor 45, rule
  only 4, triage only 12, neither 147 (92% agree). Lead vehicle: rule 0,
  triage 5. Pedestrian: both 0 of 199.
- Triage is not consistent on identical motion: 28 cut-in contacts with
  car 33, same scene, ego 0.8-0.9 m toward it, closing speeds equal to
  0.1 m/s: triage said "ego turned into actor, policy's fault" 22 times and
  "actor hit ego, unclear" 5 times. The rule gives one answer for all 28
  (the ego's: over the line).
- Actor-closed contacts on cut-in: 49 at a 3.3 or 3.6 m lane, 72 at 3.9 m.
  Lead vehicle and pedestrian: 0 at every width.
- Method results without them (`CLOSED.md`): pedestrian and lead vehicle
  unchanged at every lane width. Cut-in changes: no method reaches 5.
  hybrid 3, 3, 3 of 5 (counted: goal at 32, 36, 46), llm 3, 4, 3 (counted
  4, 4, 5), rules 2, 2, 2, random + confirmation 2, 1, 2. At 3.9 m: hybrid
  2, 2, 2, llm 3, 4, 3. hybrid's arms stopped at their counted goal, so
  they took fewer runs (32-46 of 54) than the others.
- Reading for the paper: hybrid's cut-in win rests on contacts a replayed
  car made with an ego that was braking in its lane. The cut-in comparison
  should be reported both ways, or rerun with the stricter count; the
  pedestrian and lead vehicle comparisons stand. Not changed in
  `outer.outcome` (every finished arm was scored with it).
- After problem 30's fix, every arm at its full budget (12 Oct 16:55,
  `CLOSED.md`): cut-in has 181 collision failures, 29 of them actor-closed
  (at 3.3 and 3.6 m; 52 at 3.9 m); rule and triage both say actor 24, rule
  only 5, triage only 12, neither 140 (91% agree); lead vehicle 85 and
  pedestrian 199, none actor-closed. About half of the 49 above were
  contacts carried across the hand-off. Without the 29, cut-in: rules 2, 2,
  2; hybrid 3, 4, 3; llm 3, 4, 3; random + confirmation 2, 0, 1 (counted:
  hybrid 4, 5 at 48 runs, 4). hybrid and llm tie.
- The lane test is two-sided (12 Oct 16:55): an ego 7.9 m off its path, in
  the next lane, was counted as "in its lane" because it had moved away
  from the car that came into it (pedestrian 2 Hz, two runs; triage:
  turned_into_actor). It now needs the offset to either side under the
  room to the line. No 10 Hz count changed; at 2 Hz lead vehicle went from
  5 to 0 (an ego 0.7-1.1 m over the far line, hit by car 28), pedestrian
  from 2 to 0, cut-in from 17 to 16.
- At 2 Hz (before the fix below): cut-in 16 of 51 collision failures
  actor-closed, lead vehicle 0 of 29, pedestrian 0 of 75.
- The rule read the wrong contact (12 Oct 18:10): `contact()` took the
  first front or side flag from the hand-off, so when a contact was under
  way at the hand-off it classified that one, not the later contact
  `outer.outcome` counts (problem 30). It now starts where outcome does.
  Every actor-closed contact on 10 Hz cut-in was such a carried one: of
  the 35 cut-in failures with a contact at the hand-off, the counted
  contact comes 2-7 s later, mostly the ego 1.5 m over the line into the
  lane of a car coming up at 13 m/s (car 29), or closing on car 9 ahead.
  After the fix: cut-in 0 of 185 actor-closed at a 3.3 or 3.6 m lane (23
  at 3.9 m), lead vehicle 0 of 85, pedestrian 0 of 199; at 2 Hz cut-in 6
  of 55 (15 at 3.9 m; triage agrees on all 6), lead vehicle 0 of 40,
  pedestrian 0 of 81. Triage was written about the first contact, so it
  still says actor_hit_ego for 37 cut-in runs.
- So at 10 Hz, problem 29 is covered by problem 30's fix: the method table
  is the same with and without actor-closed contacts at 3.3 and 3.6 m
  (cut-in hybrid 4, goal at 48, 4; llm 3, 4, 3). At 3.9 m: rules 1, hybrid
  3, 4, 3, llm 3, 4, 3, random + confirmation 2, 0, 0. At 2 Hz cut-in only
  random + confirmation changes, 4 to 3 (rules 2, rules_v3 0, hybrid 3, llm
  3). The bullets above that give 29 of 181, 16 of 51 and the tie on cut-in
  were computed with the wrong contact.
- 2 Hz cut-in rules_v3: 2 of its 3 counted failures were triaged
  actor_hit_ego (19f339ba, 1c45ce3a; the ego braked hard on an open road).

### Planning at 2 Hz, the three studies again (12 Oct, `HZ.md`)

Each of the three studies repeated with the policy planning every 500 ms
(`studies/<name>_2hz`, same plan with `fixed.control_timestep_us: 500000`;
lead vehicle without the planner delay, which 2 Hz cannot vary, problem
in `knobs.plan_problems`). Same methods, plus `rules_v3` (first probe at
the recording, problem 27). In progress; numbers as of the arm named.

- pedestrian x ego speed, rules (12 Oct 03:05): 4 of 5 confirmed in 50
  runs (10 Hz: goal at 25 in all three replicates). All four at the
  recording (1.0x, 0 s): 048b974e, 07981e6a, 0d4893f5, 1bbe02fc, every
  repeat failed, none involving the pedestrian. No off-recording setting
  it tried failed (it tried slower: 0.6x, 0.8x, and 1.2x once).
- pedestrian x ego speed, rules_v3 (12 Oct 03:20): also 4 of 5 in 50
  runs, the same four scenes at the recording. One off-recording failure:
  18f8dbd6 at 1.4x, 0 s, a single run (ego drifted into the next lane's
  car); not repeated, so not confirmed. Both rule variants spend their
  budget re-confirming the recording and probing slower speeds; of the 32
  hard settings off the recording at 10 Hz, 20 are at 1.2x-1.4x.
- pedestrian x ego speed, hybrid (12 Oct 04:30, resumed after problem
  28's abort): 4 of 5 in 50 runs, the same four scenes at the recording.
  Its off-recording probes (0caa8f1a, 0e002edd, 18f8dbd6) all passed.
  Three methods, one answer so far: at 2 Hz only the four recorded
  failures are found, none involving the pedestrian.
- pedestrian x ego speed, llm (12 Oct 07:00): 4 of 5 in 49 runs, a
  different four: 0d4893f5 1.2x/-0.5 s, 0e002edd 1.4x/0 s, 18f8dbd6
  1.4x/0 s, 1bbe02fc 1.2x/-0.5 s; every failure at 1.2x or 1.4x, none
  with the pedestrian. It never ran the recorded setting (0% of runs).
- Pooled at 2 Hz after these four arms (WHERE.md): 10 hard settings on 6
  of 10 scenes: 4 scenes hard as recorded, 2 (0e002edd, 18f8dbd6) hard only
  at 1.4x. So 6 distinct hard scenes exist, and each method stopped at 4:
  the rule methods and hybrid confirm the recorded failures and never the
  1.4x ones, llm the faster settings and never the recorded ones. At 2 Hz
  ego speed is needed to reach 5; at 10 Hz the recording alone gave 6.
- pedestrian x ego speed, random + confirmation (12 Oct 07:48): 4 of 5 in
  48 runs (048b974e 0.6x/-1.5 s, 07981e6a 1.2x/+2 s, 0d4893f5 1.2x/+1 s,
  1bbe02fc 0.6x/-1 s). All five methods, first replicate: 4 of 5 at 2 Hz
  (at 10 Hz every method reached 5 in 24-40 runs).
- Paired settings, pedestrian (`HZ.md`, all arms, zero delay): 63 settings
  run at both rates; 17 fail at both, 17 only at 10 Hz, 2 only at 2 Hz
  (sign test p = 0.0007). Drift at +5 s: +1.91 m at 2 Hz (73% of runs more
  than 0.5 m left) against +3.94 m (83%) at 10 Hz; at +3 s +1.09 m against
  +2.20 m. Same settings, same scenes: planning at VaVAM's own rate removes
  about half the drift and most of the failures it caused, as the m2 runs
  showed on 20 configs ("The policy drifts left", planning rhythm).
- cut-in, rules_v3 (12 Oct 05:21): 0 of 5 in 54 runs, 3 failures, at the
  recording on 19f339ba (2 of 6) and 0.5 s earlier on 1c45ce3a (1 of 3);
  2 of the 3 triaged actor_hit_ego (the ego braked hard on an open road and
  a replayed car came up into it, problem 29). It stayed near the recording
  (1.0x, within 0.5 s).
- cut-in, rules (12 Oct 08:47): 2 of 5 in 53 runs, the same two settings
  as at 10 Hz in all three replicates (1.25x, 0 s on 023b7fcc and
  09a95ffa). 023b7fcc: the ego drifted left into the next lane's car;
  09a95ffa: a car came up from behind-left into the ego's front-left corner
  while the ego held its path (triage: not the policy's or unclear,
  problem 29).
- cut-in, hybrid (12 Oct 09:34): its report says 4 of 5, but scored under
  the old count; under problem 30's fix 3 of 5 in 54 runs. Of its four, two
  (cars at 1.5x and 2x) were a replayed car driving through the ego from
  behind at the hand-off, one a car overtaking and cutting across; only
  023b7fcc (1.25x, 0 s) was clearly the policy's (drifted left into a car
  alongside).
- cut-in, llm (12 Oct 10:33): 3 of 5 in 54 runs under the fix (its report,
  written under the old count, says 4 and itself flags the fourth,
  096988dd, as a car running into the ego before the hand-off). The three:
  023b7fcc 1.25x/0 s, 0e899dd3 1.5x/-1.5 s, 09a95ffa 1.5x/-1 s, each the
  ego drifting left out of its lane into a car beside or ahead.
- cut-in, random + confirmation (12 Oct 11:20): 4 of 5 in 54 runs, the
  most of any method on 2 Hz cut-in (rules 2, rules_v3 0, hybrid 3, llm 3).
- lead vehicle, hybrid (12 Oct 15:16): 1 of 5 in 49 runs, 12855a41 at
  0.5x, 0 s (8 of 8 failed, front contact 0.5 s after the hand-off, gap
  0.33 m closing at 1.3 m/s: avoidable with about 2.6 m/s^2 of braking).
- lead vehicle, llm (12 Oct 15:34): stopped at its goal after 27 runs, but
  three of its five settings (023b7fcc, 096988dd, 09a95ffa at 0.5x) were a
  contact first flagged at the hand-off step itself: at 2 Hz poses are
  500 ms apart, so a contact begun in the warm-up's last 500 ms shows there
  first. `outer.outcome` now counts the hand-off step as the warm-up's
  (problem 30, 12 Oct 15:37; no 10 Hz result changes: at 10 Hz no contact
  starts exactly there). The arm was re-queued to finish its rounds.
- lead vehicle, rules (12 Oct 14:37): 0 of 5 in 49 runs; as at 10 Hz,
  every run at the grid middle (1.25x, 0 s), one failure (hard braking, a
  follower hit it from behind-right).
- lead vehicle, random + confirmation (12 Oct 16:50): 1 of 5 in 49 runs,
  12855a41 at 0.5x, 0 s, the setting hybrid confirmed. Its report says 2,
  written while the hand-off step still counted; the second (096988dd at
  0.5x) was flagged at the hand-off step, as llm's three were. First
  replicate on 2 Hz lead vehicle: rules 0, rules_v3 0, hybrid 1, random +
  confirmation 1, the same one scene; llm still running.
- pedestrian x ego speed, rules replicate 2 (12 Oct 17:07): 4 of 5 in 50
  runs, the same four recorded settings as replicate 1 (048b974e, 07981e6a,
  0d4893f5, 1bbe02fc at 1.0x, 0 s); no off-recording setting failed. As at
  10 Hz, rules repeat themselves across replicates.
- lead vehicle, llm, resumed to its full budget (12 Oct 17:35): goal met
  at 46 runs, the only 2 Hz arm to reach 5 in any study. All five slow the
  lead car to 0.5x, each 3 of 3 failed: 12855a41 0 s, 19f339ba -1 s,
  09a95ffa -1.5 s, 096988dd +1.5 s, 023b7fcc -1.5 s. What the ego met:
  12855a41 and 023b7fcc a lead car 0.3-0.9 m ahead at the hand-off, closing
  at 1.3-1.6 m/s (avoidable with 1.5-2.7 m/s^2); 09a95ffa a lead car 0.54 m
  ahead closing at 4.2 m/s, which needs 16 m/s^2 at the hand-off: set up
  by the warm-up, not avoidable (above 8 m/s^2, "Contacts carried across the hand-off");
  19f339ba hard braking on an open road and car 28 from behind into the
  front-right corner, the ego 1 m off its path (triage: the policy's);
  096988dd a contact carried across the hand-off, then 3 s later the ego
  drifting left into car 41 beside it (a new contact, the policy's).
  Without the unavoidable one: 4 of 5. The other methods never slowed the
  lead car this far with these shifts (rules and rules_v3 stay at the
  grid middle).
- pedestrian x ego speed, hybrid replicate 2 (12 Oct 18:26): goal met at
  32 runs, the first 2 Hz pedestrian arm to reach 5: the four recorded
  failures plus 18f8dbd6 at 1.4x, 0 s (every run at 1.4x failed, with the
  pedestrian early, on time or late; the ego drifted left into a slower car
  in the next lane). Replicate 1 had probed 18f8dbd6 once and moved on.
  None of the five involves the pedestrian.
- pedestrian x ego speed, llm replicate 2 (12 Oct 19:15): goal met at 47
  runs: 1bbe02fc, 07981e6a, 0d4893f5, 18f8dbd6, 0e002edd, every one at
  1.2x or 1.4x with the pedestrian 0.5-1 s early; never the recorded
  setting. As in replicate 1 it searched only faster settings, and this
  time reached the fifth scene. None involves the pedestrian.
- pedestrian x ego speed, random + confirmation replicate 2 (12 Oct 20:01):
  3 of 5 in 50 runs (0e002edd 1.4x/-1.5 s, 07981e6a 0.6x/+1.5 s, 1bbe02fc
  0.8x/-2 s). Replicate 2 of the four methods on 2 Hz pedestrian: rules 4,
  hybrid goal at 32, llm goal at 47, random + confirmation 3.
- cut-in, rules replicate 2 (12 Oct 20:59): 1 of 5 in 54 runs, 023b7fcc
  at 1.25x, 0 s (replicate 1: 2, also 09a95ffa at 1.25x, 0 s). Here
  09a95ffa at 1.25x did not clear the bar (most runs failed, not enough to
  confirm). Same rule, same first probe: the rate at a setting varies
  between replicates (seeds differ), and at the bar's edge that moves a
  confirmed case.
- Study reports (report.md) of arms finished before 12 Oct 09:37 state
  their goal under the old count; `METHODS.md` and these notes use the fix.
- lead vehicle, rules_v3 (12 Oct 06:10): 0 of 5 in 49 runs, 2 failures,
  both side or front contact with a car in the next lane after the ego
  drifted out of its lane, not a rear-end of the lead. One setting slowed
  the lead car, none shifted more than 1 s; at 10 Hz the hard lead-vehicle
  settings are at 0.5x (llm, WHERE.md).
- At the recording, scene by scene, all arms pooled: two scenes that fail
  every time at 10 Hz pass at 2 Hz: 0caa8f1a 17 of 18 failed at 10 Hz,
  0 of 9 at 2 Hz; 18d28973 22 of 22 against 0 of 2. The other four hard
  scenes fail at both; none fails only at 2 Hz. So at 2 Hz only 4 of 10
  scenes fail as recorded, and a fifth hard case needs a changed setting:
  the goal is harder to reach, as finding 1 (our loop doubles the drift)
  predicts.

### 2 Hz complete: three replicates of every method (13 Oct)

Every 2 Hz arm finished overnight 12-13 Oct (all exit 0; the cut-in hybrid
and llm replicate 2 arms re-queued after the queue died, resumed after their
last round). Confirmed of 5, replicates 1, 2, 3 (`METHODS.md`):

| study | rules | hybrid | llm | random + confirmation |
|---|---|---|---|---|
| pedestrian x ego speed | 4, 4, 4 | 4, 5 (32 runs), 5 (34 runs) | 4, 5 (47 runs), 4 | 4, 3, 4 |
| cut-in | 2, 1, 1 | 3, 3, 3 | 3, 2, 2 | 4, 1, 1 |
| lead vehicle | 0, 0, 0 | 1, 2, 0 | 5 (46 runs), 2, 1 | 1, 0, 1 |

- Pooled over cut-in and lead vehicle at both rates (12 arms per method,
  3 replicates x 2 studies x 2 rates): rules 10 of 60 confirmed, hybrid 33,
  llm 32, random + confirmation 19. Mann-Whitney over the 12 per-arm counts
  (two-sided unless stated): hybrid vs rules p 0.0015, llm vs rules
  p 0.001, hybrid vs random + confirmation p 0.058, llm vs random +
  confirmation p 0.046, hybrid vs llm p 0.74, hybrid and llm together vs
  random + confirmation p 0.012 (one-sided). Pooling mixes studies and the
  two rates of one study are not independent: a first look, not the
  paper's test, which should stratify by study.
- Where random + confirmation's runs fail often, the guided methods add
  little: its failure share pedestrian 10 Hz about 75% (every method 5 of
  5), pedestrian 2 Hz about 45%; cut-in 10 Hz 19% (hybrid 13 of 15,
  random 4), cut-in 2 Hz 22% (hybrid 9, random 6), lead 2 Hz 12% (llm 8,
  random 2). Lead vehicle 10 Hz (18%, hybrid 8, random 7) does not fit.
  The gap tends to grow as failures get rarer; the hard-study plan
  (`OUTLINE.md`) tests this directly.
- What llm and hybrid are given each round (`outer.py`, state; prompt
  `advisor/OUTER.md`): the candidates with S1's one run at 0 delay, the
  knobs, every run so far (scene, knobs, failed, gate verdict) and the
  per-setting summary with 90% ranges. Not the triage's explanations, not
  the tagger's scene facts, not the drift finding. The prompt still says
  traffic is sampled (CATK) and one setting can end differently each time;
  the method studies replay traffic, where replicates are nearly
  deterministic (above). Left as is for these arms; a v2 proposer is the
  place to change it, so these results stay reproducible.
- Model time per arm: 1-2 min of Claude calls (llm 87-121 s, hybrid
  42-111 s), against about 50 min of simulation.

### Optuna with confirmation, and Optuna + AI (13-14 Oct, 10 Hz, three replicates)

`optuna_confirm`: Optuna's TPE with the rules' confirmation (at most half of
each round), as random + confirmation; plain `optuna` never repeats a
setting, so it cannot meet a top_k goal (problem 21). `hybrid_optuna`
(Optuna + AI): Claude chooses each round among the rules' confirmations and
up to 3x as many distinct Optuna suggestions. Pedestrian crossing (7 Oct)
had plain optuna: 3 failures in 49, 1 confirmed.

Confirmed hardest cases of 5 per replicate (`METHODS.md`; "no frozen" =
contacts with a car the retiming held still not counted, problem 31, which
the scorer does from 14 Oct, so `METHODS.md` now shows those numbers; the
first Optuna + AI cut-in replicate met its goal at 20 runs on frozen-car
contacts and stopped at 27, so under the rule it is left out and a fourth
replicate replaces it, finished 15 Oct):

| method | pedestrian: runs to goal | cut-in | cut-in, no frozen | lead | car scenes, no frozen (of 30) |
|---|---|---|---|---|---|
| rules | 25, 25, 25 | 2, 2, 2 | 2, 2, 2 | 0, 0, 0 | 6 |
| hybrid (rules + AI) | 24, 28, 24 | 4, 5, 4 | 3, 3, 3 | 2, 3, 3 | 17 |
| AI picks | 28, 40, 37 | 3, 4, 3 | 3, 2, 1 | 3, 1, 3 | 13 |
| random + repeat | 31, 32, 32 | 3, 0, 1 | 2, 0, 1 | 4, 1, 2 | 10 |
| Optuna + repeat | 25, 31, 33 | 4, 5, 1 | 4, 4, 0 | 1, 3, 1 | 13 |
| Optuna + AI | 21, 20, 21 | 5, 4, 5 | 2, 3, 1 (replicates 2-4) | 1, 2, 4 | 13 |

- **Pedestrian**: every arm of every method confirms 5 of 5; Optuna + AI
  gets there first in all three replicates (median 21 runs: rules 25,
  hybrid 24, Optuna + repeat 31, random + repeat 32, AI picks 37).
- **Car scenes, frozen cars not counted** (Mann-Whitney, 6 values per
  method; Optuna + AI with its fourth cut-in replicate, 15 Oct): hybrid
  vs rules p 0.006, AI picks vs rules 0.097, Optuna + AI vs rules 0.15;
  hybrid vs random 0.078, Optuna + AI vs random 0.51; Optuna + repeat vs
  rules 0.25, vs random 0.74; every pair among hybrid, AI picks, Optuna +
  repeat and Optuna + AI p > 0.2.
- **Optuna + AI chased frozen cars most**: cut-in 14 of 15 as counted, 8
  without them. Optuna alone barely did (10 to 8).
- Reading: Optuna alone is no better than random + repeat at this budget;
  the AI choosing among the rules' candidates (hybrid) is the one method
  that clearly separates from rules on the car scenes; AI picks and
  Optuna + AI sit between rules and hybrid, and the AI variants differ
  within the noise of three replicates. On pedestrian Optuna + AI is the
  fastest in every replicate.
- **2 Hz, pedestrian x ego speed** (Optuna arms done 16 Oct): confirmed
  of 5 (runs to goal where reached): Optuna + AI 4, 5 (39), 5 (20);
  Optuna + repeat 5 (30), 4, 4; hybrid 4, 5 (32), 5 (34); AI picks 4,
  5 (47), 4; random + repeat 4, 3, 4; rules 4, 4, 4. Optuna + AI and
  hybrid reach the goal in 2 of 3 replicates, Optuna + repeat and AI
  picks in 1, random and rules in none.
- **2 Hz, cut-in** (Optuna arms done 17 Oct), confirmed of 5 (total of
  15): Optuna + AI 2, 2, 2 (6); hybrid 2, 2, 1 (5); rules 2, 1, 1 (4);
  random + repeat 3, 0, 1 (4); Optuna + repeat 0, 1, 1 (2); AI picks
  1, 0, 1 (2). No arm reaches the goal and the methods are within noise
  of each other: after the problem 31 rule removed the frozen-car
  contacts, 2 Hz cut-in has few failures any method can confirm.
- **2 Hz, lead vehicle** (Optuna arms done 17 Oct), confirmed of 5 (total
  of 15): AI picks 5 (46 runs), 2, 1 (8); Optuna + AI 1, 2, 1 (4); hybrid
  1, 2, 0 (3); random + repeat 1, 0, 1 (2); Optuna + repeat 0, 2, 0 (2);
  rules 0, 0, 0 (0). Only AI picks reached the goal (one replicate).
- With these, every queued arm is done (17 Oct): Optuna alone never beats
  random + repeat in any study; an AI chooser leads or ties in every
  study; where failures are plentiful (pedestrian 10 Hz) all methods tie,
  where they are rare (hard study, lane keeping, lead 2 Hz) the
  free-choosing AI leads.

### Lane keeping, the unseen study: three replicates of 8 methods (15 Oct)

10 Hz, plan shift x ego speed on 12 straight scenes, goal 5 hardest
confirmed, budget 50 runs (`METHODS.md`). The v2 proposers
(`advisor/OUTER_V2.md`) were written before this study and not changed
for it. Runs to goal, replicates 1-3 (median):

| method | runs to goal | reached goal |
|---|---|---|
| AI picks v2 (`llm_v2`) | 17, 21, 18 (18) | 3 of 3 |
| AI picks (`llm`) | 20, 19, 20 (20) | 3 of 3 |
| Optuna + AI | 18, 20, 20 (20) | 3 of 3 |
| Optuna + repeat | 28, 32, 25 (28) | 3 of 3 |
| random + repeat | 31, 30, 30 (30) | 3 of 3 |
| hybrid v2 | 43, 39, 50 (43) | 2 of 3 (4 of 5 in the third) |
| hybrid | 50, 50, 45 | 1 of 3 (4, 3, 5 of 5) |
| rules | budget spent | 0 of 3 (2, 2, 1 of 5) |

- Every replicate of every free-choosing AI method (llm, llm_v2, Optuna +
  AI; 9 arms, 17-21 runs) reached the goal before every replicate of
  random + repeat and Optuna + repeat (6 arms, 25-32 runs). With three
  replicates per method a complete separation gives the smallest exact
  two-sided Mann-Whitney p possible, 0.1 per pair; pooling the three AI
  methods against the two non-AI ones (9 against 6, complete separation)
  gives exact p 0.0004 two-sided (scipy's default, with the normal
  approximation for ties, 0.0016). Pooling is post hoc: a first look.
- Methods tied to the rules' candidates trail: the rules spend their
  budget confirming near-misses that do not fail (as on lead vehicle,
  problem 26), and hybrid can only choose among those candidates.
  On this study the AI's value is in choosing freely, the reverse of the
  car scenes, where hybrid led.

**Five repeats (19-20 Oct).** Two more replicates of six methods (the
hybrids stay at three). Runs to goal, replicates 1-5 (median):

| method | runs to goal | reached goal |
|---|---|---|
| AI picks v2 | 17, 21, 18, 18, 19 (18) | 5 of 5 |
| AI picks | 20, 19, 20, 22, 19 (20) | 5 of 5 |
| Optuna + AI | 18, 20, 20, 19, 21 (20) | 5 of 5 |
| random + repeat | 31, 30, 30, 23, 29 (30) | 5 of 5 |
| Optuna + repeat | 28, 32, 25, 32, 40 (32) | 5 of 5 |
| rules | budget spent | 0 of 5 (2, 2, 1, 2, 2 of 5) |

- All 15 free-choosing AI arms (17-22 runs) reached the goal before all 10
  random and Optuna + repeat arms (23-40 runs). Exact two-sided
  permutation test, 5 vs 5, on runs to goal (rules scored at the 50-run
  budget, a lower bound): each of AI picks v2, AI picks and Optuna + AI
  against each of random, Optuna and rules p 0.0079 (complete
  separation, the smallest possible); among the three AI methods p 0.22
  to 0.80; random vs Optuna 0.40.
- Planned comparisons, as for the hard study: AI picks v2 against random,
  Optuna and rules, Holm over the three 0.024 each. Holm over all 15 pairs
  of the six methods: the 11 complete separations run from 0.040 to 0.119,
  so only random and Optuna vs rules stay below 0.05.
- v2 was written before this study and not changed for it (above), so it
  is a fair pre-named AI method. Across the two studies with five repeats,
  v2 separated completely from random, Optuna and rules in both.
- Figure: `figures/discovery_lane_keeping.png` (`harness/discovery_curve.py`).
- Model time per arm: llm 27-31 s, llm_v2 33-66 s, Optuna + AI 30-47 s,
  hybrid 84-89 s, hybrid v2 100-102 s.

### The three-knob hard study (from 15 Oct, 2 Hz)

`car_conflicts_3knobs_2hz`, 8 methods x 3 replicates queued 14 Oct under
the problem 31 rule; budget 60 runs, goal 5 hardest confirmed. All 24
arms done 16 Oct (`METHODS.md`). Confirmed of 5 per replicate, total of 15:

| method | confirmed | of 15 | reached goal (runs) |
|---|---|---|---|
| AI picks v2 | 4, 5, 5 | 14 | 2 (52, 51) |
| AI picks | 2, 5, 5 | 12 | 2 (59, 52) |
| Optuna + AI | 3, 4, 2 | 9 | 0 |
| hybrid v2 | 2, 2, 3 | 7 | 0 |
| hybrid | 2, 2, 1 | 5 | 0 |
| Optuna + repeat | 2, 1, 2 | 5 | 0 |
| random + repeat | 2, 0, 2 | 4 | 0 |
| rules | 0, 0, 0 | 0 | 0 |

- Only free-choosing AI arms reached the goal (4 of 6 AI picks and AI
  picks v2 arms; no other arm of 18).
- Mann-Whitney (two-sided, 3 per method unless pooled): AI picks v2 vs
  random + repeat, complete separation, exact p 0.1 (the floor for 3 vs 3);
  the three free-choosing AI methods pooled (9 arms) vs random and Optuna
  + repeat (6 arms) p 0.006; vs the two hybrids (6 arms) p 0.014; hybrid
  vs rules p 0.06. Pooling is post hoc.
- Fits the 13 Oct expectation: where failures are rare (rules found 3 in
  180 runs), the guided gap widens. Here, unlike the car scenes at 10 Hz,
  hybrid (restricted to the rules' candidates) trails the free AI, as on
  lane keeping.
- Curve `figures/discovery_car_conflicts_3knobs_2hz.png`.

**Five repeats (19 Oct).** Two more replicates of six methods (the hybrids
stay at three), queued 18 Oct to replace the post hoc pooling with
head-to-head tests. Confirmed of 5 per replicate, total of 25:

| method | confirmed | of 25 | reached goal (runs) |
|---|---|---|---|
| AI picks v2 | 4, 5, 5, 5, 5 | 24 | 4 (52, 51, 41, 41) |
| AI picks | 2, 5, 5, 3, 2 | 17 | 2 (59, 52) |
| Optuna + AI | 3, 4, 2, 2, 2 | 13 | 0 |
| Optuna + repeat | 2, 1, 2, 2, 3 | 10 | 0 |
| random + repeat | 2, 0, 2, 2, 1 | 7 | 0 |
| rules | 0, 0, 0, 0, 0 | 0 | 0 |

- Exact two-sided permutation test on the per-replicate counts, 5 vs 5
  (smallest possible p 0.0079): AI picks v2 vs random + repeat 0.0079, vs
  Optuna + repeat 0.0079, vs rules 0.0079 (complete separation each), vs
  Optuna + AI 0.016; AI picks vs rules 0.0079, vs random 0.079; Optuna + AI
  vs random 0.16; Optuna + repeat vs random 0.48; random vs rules 0.048.
- Planned comparisons (the reason for the extra repeats): AI picks v2
  against random, Optuna and rules; Holm over those three, 0.024 each.
  Holm over all 15 pairs of the six methods leaves nothing below 0.05
  (smallest 0.079); state which is used. AI picks v2 was built on the three
  method studies before this study ran (OUTLINE "AI proposer v2"), so
  naming it the AI method in advance is fair.
- The two new replicates repeat the first three: v2 confirmed 5 of 5 in
  both and met the goal sooner (41 runs each); AI picks v1 is less steady
  (2 to 5); Optuna alone again no better than random.

### Intersection crossing, a fifth category (pilot, 20 Oct)

`intersection_ego_speed` (10 Hz, ego speed at hand-off x the crossing car's
timing, 49 runs, goal 5 hardest confirmed): one replicate of each of seven
methods, the three newer ones (AI picks v2, Optuna + repeat, Optuna + AI)
added 20 Oct beside the four from 9 Oct, all scored under the current rules
(`METHODS.md`). Confirmed of 5: rules 2, hybrid 2, AI picks 2, random +
repeat 2, Optuna + AI 2, AI picks v2 2, Optuna + repeat 1; no arm reached
the goal. Failures per arm 6-18.

- Every method stops at about two confirmed cases: the study seems to hold
  about two settings that fail reliably, and every method finds them. Like
  pedestrian at 10 Hz (failures easy to find), methods tie; unlike the hard
  study and lane keeping, there is no room for a better chooser to show.
- Enough for coverage (a fifth Euro NCAP-mapped category, AEB C2C crossing,
  where the agent ran the study end to end); not worth more replicates for
  the method comparison.

### Shao's 13 Oct feedback: evidence produced (`CHECKLIST.md`)

- **Self-healing, every study queue** (`figures/cards/self_healing.json`):
  144 failed launches went to the diagnose contract. GPU out of memory
  (two runs at once) 102: RE-RUN 101 (99 then kept, 2 stopped at the
  attempt cap), HALT 1. GPU still held by the previous run 18:
  CLEANUP_ENV 17 (kept), HALT 1. Physically impossible motion 11: HALT 11
  (intended; problem 24). Other simulator crash 11: RE-RUN 10,
  RESTART_CLEANUP 1 (all kept). Launcher lost 2: RESTART_CLEANUP (kept).
  129 of 144 healed with no person.
- **Self-healing ledger, whole campaign to 18 Oct** (`HEALING.md`,
  `harness/healing_ledger.py`, `figures/healing/`): recounted from the
  queues, the 13 Oct cutoff gives the same 4,668 launches, 144 failures, 129
  healed. To 18 Oct: 8,540 runs asked for, 8,775 launches, 323 failed
  launches to the agent: GPU out of memory 219 (RE-RUN 215, HALT 4; 205
  healed), failed the physics check 59 (HALT 59, intended: 11 before 13 Oct are
  problem 24's jolt; after it, 36 speed-report errors (three-knob 20, lane
  keeping 11, pedestrian 2 Hz 5), 8 lane-keeping plans shifted less than
  asked, 4 lane-keeping yaw-rate or acceleration bounds), GPU still busy 24 (CLEANUP_ENV 23), other simulator crash
  19 (18 healed), launcher lost 2 (healed). 248 healed; 248 of 264
  operational failures. 99.2% of runs asked for ended kept. Every retry ran
  the parent's exact settings (323 of 323); every choice passed the code
  check (no production rejection; the check's teeth are shown by the
  exhaustive check and planted faults). Median 8 s of agent time per
  diagnosis.
- **What every kept run contains**, six method studies, all methods
  pooled, exclusive categories in this order: counted failure (split by
  `possible_artifact`), contact begun before the hand-off, rear-ended by a
  replayed car, no contact (`figures/cards/outcome_mix.json`,
  `VALIDITY.md` table). Rear-ended by a replayed car with no other event:
  27-38% of kept runs in the car studies. Contact begun before the hand-off:
  9-17%. Pedestrian 10 Hz: 159 of 301 counted failures with the ego more
  than 3.5 m off the recording (flagged, not removed).
- **Failure types** (`figures/cards/triage_causes.json`), Claude's triage of
  1,252 failed runs in the six studies (every run flagged failed when its
  study ended, some under older definitions): turned_into_actor 589 (47%),
  left_road 197 (16%), other 184 (15%), actor_hit_ego 146 (12%),
  no_brake_for_lead 129 (10%), rendering 7. The studies are braking-shaped;
  two thirds of their failures are steering.
- **Spot check** (`figures/cards/spot/`, seed 20261013, 20 of the kept runs
  of the three 10 Hz studies): 5 counted failures (2 at-fault contacts,
  3 off-road), 10 contacts not counted (rear-ended or begun before the
  hand-off), 5 no contact. S06: a lead car retimed +1.5 s overlaps the ego
  from 1.3 s while it still replays the human (triage: not the policy's).
- **Hardest-case cards** (`figures/cards/hardest/`): 19 confirmed hardest
  settings, all arms pooled at 10 Hz (pedestrian 7, cut-in 6, lead 6).
  Two pedestrian hardest cases are the ego leaving the road and then
  meeting an oncoming car; none involves the pedestrian.
- **Simulation time per run** (runtime log "simulated ... in ... wall
  clock seconds", last 1,469 runs): 2 Hz (24 steps) median 46.7 s, 10 Hz
  (120 steps) 83.5 s, two runs at once. One policy step at 10 Hz about
  460 ms, a warm-up step about 10 ms, the first step about 37 s (model load).
  A whole 10 Hz run is about 3 min; an arm of 54 runs about 2.5-3 h.
- **OpenSCENARIO**: `scenarios/*.xosc` (to_openscenario.py) validate
  against esmini's OpenSCENARIO 1.3 and 1.4 schemas.
- **New proposers** (tests in test_guided.py, test_outer.py):
  `optuna_confirm`, `hybrid_optuna` (Claude among the rules' confirmations
  and up to 3 x per_round Optuna suggestions; offline check on cut-in round
  4: 34 candidates, 9 runs chosen, all on the list), `llm_v2` and
  `hybrid_v2` (OUTER_V2.md: replayed traffic, a prior from these studies,
  live triage of each failure, the tagger's scene facts, notes between
  rounds; offline check: 10 legal runs, reasons cite the triage).
- **Problem 31, retimed cars that freeze** (`held_actors.json`,
  `held_rescore.json`): see the problems table. Pooled over cut-in and lead
  vehicle at both rates with held-actor contacts removed: rules 10 of 60,
  hybrid 25, llm 23, random + confirmation 16 (were 10, 33, 32, 19).
  Mann-Whitney: hybrid vs rules p 0.008, llm vs rules 0.045, hybrid vs
  random 0.09, llm vs random 0.28, hybrid and llm together vs random 0.051
  (one-sided). The advantage over rules holds; over random it is no longer
  clear.
- **Hardest-case cards against the triage**: of the 19 cards, the triage
  says the policy was at fault on 14, not at fault on 3 (cut-in 096988dd: a
  car at 2x hit the ego from behind before the hand-off, then froze in its
  lane; lead vehicle 19f339ba and 0e899dd3: contacts the triage places at
  the start of the run), unclear on 1, none on 1. A person should look at
  these four cards.
- **New studies**: `lane_keeping` (10 Hz; plan shift x ego speed, 12
  straight scenes, 50 runs; 8 methods, one replicate) and
  `car_conflicts_3knobs_2hz` (actor timing x actor speed x ego speed, 10
  cut-in and lead scenes that pass as recorded, 60 runs; 8 methods x 3
  replicates). The planner left `control_timestep_us` out of the 2 Hz
  plan; added by hand (500000) and the plan re-checked.

## Controller A/B, 8 Oct (feasible_best against linear)

Hybrid proposer, pedestrian scenes, pairs with shared seeds. Round 1: 5 pairs,
linear 0 failures, feasible_best 5 (pooled 90% ranges 0-35% and 65-100%,
sign test p 0.06). The study stopped there, its goal met, but every pair was
at one setting (0 s shift, 1.25x pedestrian speed); triage puts none of
feasible_best's failures on the pedestrian: at a RIGHT route command the ego
turns too sharply into parked cars or veers left off the road, 6.7-14 m off
the recording. So feasible_best (or how the uncommitted configuration.py
passes its gains) breaks these scenes whatever the pedestrian does. The goal
now needs 3 settings on 2 scenes (problem 22); the study is continued.
Continued (9 Oct): 10 pairs over 4 knob settings on 4 scenes, linear 0 of 10,
feasible_best 10 of 10 (pooled ranges separate, sign test p 0.002); still
none of feasible_best's failures involves the pedestrian. Will should check
the feasible_best gains (or the uncommitted configuration.py that passes
them) before any tuned-controller claim.

## The policy drifts left, 8-9 Oct (`DRIFT.md`, `COMMANDS.md`)

Found reading the triage: "despite a RIGHT command, the ego drifted left"
in failure after failure. Measured on every kept study run
(`drift_analysis.py`; the ego's signed lateral offset from the recorded
human path, left positive):
- **Closed loop:** 0 at the hand-off (a check: the ego replays its recording
  up to there), then left: median +0.99 m at 2 s, +2.19 m at 3 s, +3.53 m at
  5 s (about one lane), and 88% of the 853 runs end more than 0.5 m left of
  the recording, 1% right. 89% of failures happen left of it, none right.
  Refreshed 10 Oct over all 2428 kept study runs (replicates and ego speed
  settings included): +0.52 m at 2 s, +1.34 m at 3 s, +2.39 m at 5 s (88%
  left, 0% right); at the end 86% left, 1% right; 75% of failures left of
  it, none right. Smaller medians than the first 853, same direction.
- **Not new:** the same in B2 (28 Sep, one scene, +1.0 m, 97% left), S1
  (29 Sep, 100 scenes, +3.2 m at the end, 84% left) and v1 (fresh frames,
  6 Oct, 82% left). So neither the recent changes nor stale frames cause it.
- **Open loop already leans left:** during the warm-up the ego is on its
  recording while VaVAM still plans; its plans end left of where the human
  went: median +0.21-0.24 m at 1-3 s, mean +0.9-1.3 m, 19-31% of 6322 plans
  more than 0.5 m left against 7-14% right. Closed loop compounds the lean.
- **Not an integration bug found:** AlpaSim's command (2 m rule, y left) and
  its map to VaVAM's encoding (RIGHT 0, LEFT 1, STRAIGHT 2) match VaVAM's
  training code; the camera is centred (1.66 m ahead, 1.4 cm right, 1.52 m
  up, within 0.5 deg of nominal) with the field of view VaVAM expects (64
  deg; 1920x1080 scales exactly to 1600x900).
- **Route commands are an effect, not a cause:** 84% of failures happened
  under a RIGHT command, but at the hand-off 194 of 200 runs had STRAIGHT;
  RIGHT builds up as the ego leaves its route to the left, so "ignored a
  RIGHT command" in the triage mostly describes the drift.
  Refreshed 10 Oct over all 2428 kept runs (736 failures): 68% of failures
  under RIGHT, 32% STRAIGHT, 0.4% LEFT (`COMMANDS.md`); the hand-off count
  was not re-checked.
- **Mirror test (9 Oct, `MIRROR.md`, `harness/m1_queue`):** 10 drift-heavy
  scenes x seeds 1111/2222, each run plain and with VaVAM's input and output
  mirrored (camera frames flipped left to right, LEFT/RIGHT commands
  swapped, the plan mirrored back; a switch in a second checkout, checked by
  the gate), traffic replayed; all 40 kept (3 crashed launches retried).
  Plain: 20 of 20 pairs end left of the recording, median +6.4 m. Mirrored:
  18 of 20 end right, median -2.1 m, 2 near the path; at +3 s mirrored runs
  are already 1.0-3.3 m right where they have not failed. The drift turns
  with the mirror. So the lean is in VaVAM itself, between the image and the
  plan: not downstream (the controller and vehicle model see the same world
  in both runs, so a bias there would push both the same way), not the
  traffic side of the scene (a mirrored right-hand scene looks like
  left-hand traffic; a model confused about the traffic side would settle,
  not drift right), and not an asymmetric image pipeline (the principal
  point is the image centre). **Planning rhythm (m2, 9 Oct):** the same 20
  plain configs at 500 ms control steps (VaVAM's training rhythm: a plan
  per fresh frame, 8 frames at 2 Hz; AlpaSim's own VaVAM config also plans
  at 2 Hz) against our 100 ms steps (4 of 5 plans from a reused frame):
  failures 4 against 6 (2 flip to pass, none the other way); median offset
  at the end +3.0 m against +6.4 m, at +3 s +1.5 m against +3.7 m; 17 of 20
  still end left. Our loop about doubles the drift; the lean stays.
  Mirrored runs fail more (16 of 20 against 6):
  drifting right meets the curb and parked cars sooner. A learned lean in
  the model's own frame, e.g. from its training data, is the reading left.
- For the paper: the hardest cases a search finds are mostly places where
  this drift meets other traffic or the road edge; that is a real weakness
  of the policy under test, found by the system, and it should be stated as
  the dominant failure mode.

## Problems met building the loop, and how each was solved (for the paper)

Each one would have made an unattended testing loop produce wrong results
quietly. Sources: LOG.md, the commits named.

| # | Problem | How it showed | Fix | Kind |
|---|---|---|---|---|
| 1 | Docker network pool exhausted by leaked networks | B2's first 8 runs could not start | compose down after every run; machine check before launch; CLEANUP_ENV | environment |
| 2 | A recovery could change what a run measures | Verifier: CONFIGURE of the delay kept a run measuring another condition (28 violations) | the delay and scene are never configurable | gate design |
| 3 | Our own timeout erased the evidence | both model tiers misdiagnosed hangs (CONFIGURE 7/10, 8/10) | the monitor records the machine before stopping a run; then 5/5 right | observability |
| 4 | A crashed read-only script stopped a whole arm | monitor.py native abort (exit -6) at C2 run 32 | rerun once, logged | robustness |
| 5 | The plan-handoff check rejected every delay run | 0.12–0.17 m on delay runs vs 0.05 m bound | match the plan to its source by timestamp, compare in the frame it was made; plan-age check proves the delay was applied | measurement |
| 6 | A requested bias measured 0.91–0.98 m, not 1.0 | offset measured along the ego heading | measure along each waypoint's normal: 0.9999–1.0001 m | measurement |
| 7 | Requested noise measured 0.26 m, not 0.3 | biased per-step std | chi-square-corrected median variance: 0.295–0.306 m | measurement |
| 8 | VaVAM got a new frame only every fifth plan | 4 of 5 plans re-anchored stale images (up to 400 ms at "0 delay") | frames every 100 ms, every fifth in the context; failures 11→6 of 17 | simulator setup |
| 9 | Fresh frames ran out of memory on 12 GB | CUDA OOM in 2 of 12 runs | 24 GB GPU; GPU-release wait in the machine check | hardware |
| 10 | A false "GPU busy" stopped a batch | 8.9 GB free right after the previous teardown; environment halt ends a batch | the machine check waits up to 60 s for memory to free | robustness |
| 11 | The reporter miscounted | "5 of 5" where the table had 4 of 4; "not overlapping" ranges that overlapped | counts only from code; reports with hand-written counts refused; goals checked by code | model output |
| 12 | A one-run pilot "finding" | pilot suggested a clean 100–150 ms break | confirmation study: not confirmed (100 ms 2/4 failed) | statistics |
| 13 | A goal satisfied by a meaningless bracket | surely low at 0 ms and surely high at 400 ms counted as "found" | bracket goals need a resolution (max_gap) | goal design |
| 14 | Three copies of a batch ran at once | stale waiters raced on one queue; a launch failed | one loop per queue (exclusive lock) | orchestration |
| 15 | A pid reused after a reboot could pass for a live run | power cut mid-study | boot id recorded at launch; another boot is never alive | robustness |
| 16 | Every retimed run was rejected | a track id reached Hydra unquoted and came back as a number (17 of 26 halted) | quote ids; compare as strings; study restarted from scratch | configuration |
| 17 | A retiming that matches no actor would silently do nothing | (designed against, not hit) | runs fail unless the runtime logs the requested actor as retimed | gate design |
| 18 | The kinematic controller passes physics on gentle scenes | no jerk statistic separates it from one clean highway run | left to the Auditor (config + same-scene reference); its rule was enacted | gate design |
| 19 | Two runs at once collided | port race at start (both wizards picked the same free ports) and CUDA OOM peaks on 24 GB (about 1 in 5 launches each) | a base port per run name; crashed runs are never kept and the Investigator retries them (RE-RUN) | concurrency |
| 20 | A gate bound too loose to catch its fault | the hand-off speed bound (0.2 m/s + 5%, set from synthetic cases) could not tell 0.8x from 1.0x on a scene recorded at 1 m/s | calibrated on real runs: 298 at scale 1 (worst 0.023 m/s) and the 5-run smoke test (worst 0.004 m/s); bound now 0.05 m/s + 2% | measurement |
| 21 | The random baseline could never meet a top_k goal | it never repeats a setting, so it confirms nothing: 31 failures in 48 runs, 0 of 5 confirmed (pedestrian x ego speed) | random_confirm: random search plus the rules' confirmation (at most half of each round) | evaluation design |
| 22 | A comparison goal met by one setting | the A/B stopped after its first round: 5 pairs, all at one pedestrian timing | a compare goal also needs its pairs to cover 3 knob settings on 2 scenes | goal design |
| 23 | A continued study kept a stale crash analysis | triage ran only when no triage file existed | triage the failures the earlier triage lacks | orchestration |
| 24 | Our own knob produced implausible motion before the policy drove | pedestrian x ego speed, scene 07981e6a at 1.2x: 10.7 m/s^2 at 3.7 s before the hand-off, where the warm-up extrapolated before the recording (extended at the first recorded second's mean velocity, 5.72 m/s) meets the recording (4.65 m/s) | the physics bound halted both runs (not kept); the extrapolation should match the recording's speed at the seam; held until the replicate studies ended (so every replicate saw the same warm-up), applied 10 Oct (`patches/pending-ego-retiming-seam.patch`; unit tests pass); re-checked in a simulation 12 Oct (`studies/seam_check`: 07981e6a at 0.6x-1.4x, all 5 kept by the gate; peak acceleration over the whole run 3.7 m/s^2 at 1.2x, against 10.7 before the fix) | gate catch (simulator setup) |
| 25 | A quarter of the "failures" were not the policy's | the gallery of confirmed hardest cases showed collisions at t = 0 s, collisions while the ego still replayed its recording, and replayed cars rear-ending a slower ego and then overlapping its front (counted "front"): 49 of 200 counted failures (cut-in 32 of 51, lead vehicle 17 of 37; pedestrian x ego speed 0 of 84) | a failure is now off-road, or a front or side collision that begins before any rear contact, counted from the policy's first step (AlpaSim's own eval_relevant warm-up filter; nuPlan's rear-collision rule); the closest approach uses the same window; `failed_any` keeps the broad reading; arms that stopped under it are left out of the method comparison and replaced by a fourth replicate | evaluation design |
| 26 | The rule proposer spent its budget confirming near misses that never fail | lead vehicle: rules 0 failures in 49 runs; rules + corners repeated "confirm S#: near failure" every round after the first (38 runs, 0 failures), while random + confirmation confirmed 5 cases at knob extremes | a rate of 0 is never surely above high_min, and nothing stopped confirmation once a rate was surely below it; rules_v2 stops confirming a setting whose 90% range tops out below high_min (3 straight passes) and then tries the scene's corners; rules and hybrid keep the old rule so their replicates stay comparable | search design |
| 27 | The rule proposer's results mostly reflect where it starts | rules confirmed exactly the settings at the middle of each knob's range: 1.25x and 0 s on cut-in in every replicate, nothing on lead vehicle where the middle (1.25x, 200 ms) is the easy direction (100% of runs at 1.25x, 0 of 6 hard scenes touched) | found by pooling every arm's runs per setting (`where_found.py`, `WHERE.md`); not changed in `rules`, whose replicates are done; a rule design should start at the recording and step in the direction the brief calls harder, or sweep the corners first | search design |
| 28 | A study stopped after a native crash at interpreter exit | pedestrian x ego speed at 2 Hz, hybrid, 12 Oct: archive.py saved the run's ACCEPT, then aborted at exit (signal 6), the first such crash in about 2,500 runs; the inner loop re-runs monitor and analyze after a signal crash but not archive, and archive refused a run already accepted, so the arm stopped after 7 runs | archive.py returns at once for a run already accepted, and the loop re-runs it after a signal crash (`RERUNNABLE`, tests in `test_loop.py`); the arm re-queued and resumed from its queue, nothing lost | robustness |
| 29 | The failure count still included replayed cars running into the ego | cut-in: a replayed car closing on an ego that was braking in its own lane, first contact at the ego's front corner (so the rear rule of problem 25 kept it): 49 of 208 counted collision failures; triage saw it too but judged 28 identical contacts two ways (22 against 6) | a geometric rule from the poses (`who_closed.py`: who closed the gap, was the ego in its lane, two-sided), checked against triage; most such contacts were under way at the hand-off, and once problem 30's fix skips those (and the rule reads the contact outcome counts) none are left at 10 Hz in a 3.3-3.6 m lane, so the 10 Hz method table stands; at 2 Hz cut-in 6 of 55, random + confirmation 4 to 3; `outcome` not changed | evaluation design |
| 30 | Contacts under way at the hand-off counted as the policy's | lead vehicle: 75 of 145 counted collision failures (70 of llm's 74) began in the warm-up, when a lead car slowed to 0.5x met the ego still replaying the human's path, and were still flagged at the policy's first step; cut-in 61 of 208 | collisions now count from the first step after a contact under way at the hand-off step ends (`outer.outcome`, `contact_at_handoff`; the hand-off step counts as the warm-up's, which matters at 2 Hz); arms that had stopped at the old goal re-queued to finish; lead vehicle's winner (llm, 23-30 runs) drops to 3, 1, 3 of 5, no method reaches the goal on lead vehicle or cut-in; pedestrian unchanged | evaluation design |
| 31 | Retimed cars froze in their lane, and the search learned to hit them | the case cards (Shao's visual check, 13 Oct): AlpaSim's actor retiming holds a retimed track's last pose after its new end (by design, `actor_retiming.py`), so a car at 2x speed finishes its recording halfway through the run and stops dead from about 11 m/s in one step; 60 of 203 counted cut-in contacts at 10 Hz and 44 of 145 at 2 Hz are the ego meeting such a car, none on lead vehicle (`held_actors.py`, `held_actors.json`). The AI methods favoured these settings: without them cut-in confirms hybrid 3, 3, 3 (was 4, 5, 4), llm 3, 2, 1 (3, 4, 3), rules 2, 2, 2, random + confirmation 2, 0, 1; at 2 Hz hybrid 2, 2, 1, llm 1, 0, 1 (`held_rescore.json`) | 14 Oct (Will: "pick what you know is best"): the scorer does not count a contact with a road user that stopped dead, held at its last pose after moving faster than 2 m/s (`outer.outcome` `contact_with_held_actor`, `physics.stopped_dead`), the same kind of rule as problem 30; it removes the same 89 and 44 contacts. Ending runs when the retimed car's recording ends was weighed and rejected: VaVAM's 4 s of frame history puts the hand-off near 4.6 s, so at 2x speed little or no policy driving would be left. Extending tracks in the runtime would change src. The three-knob hard study is queued under the rule | evaluation design |
| 32 | A study stopped after a native crash in the diagnosis check | hard study, Optuna + AI, 15 Oct: a retried run (scene 1c45ce3a, ego 1.4x) failed the physics bound (reported speed 1.19 m/s off the measured one; random + repeat met the same bound on the same scene and setting, halted that run and went on); the agent chose HALT, `validate_diagnosis.py` saved its verdict and then aborted at interpreter exit (signal 6, the crash of problem 28), which the loop did not re-run, so the arm stopped after 11 runs | `validate_diagnosis.py` returns a saved rejection at once, and the loop re-runs it after a signal crash (`RERUNNABLE`, tests in `test_loop.py` and `test_validate_diagnosis.py`); the arm re-queued and resumes from its queue | robustness |
| 33 | A study stopped after the same native crash twice in a row | hard study, AI picks v2 replicate 4, 19 Oct: `monitor.py` aborted at exit (signal 6, problems 28 and 32) on run 016 and again on its one rerun, so the loop stopped the arm in round 2. Over the campaign 81 such aborts in roughly 9,000 runs, each healed by one rerun until this one | the loop reruns a signal-killed rerunnable script up to three times (`RERUNS`, `run_rerunning`, test in `test_loop.py`); a script that keeps aborting still stops the arm; the arm re-queued and resumes from its queue | robustness |

## Physics checks, 29 Sep 2026 (Shao: the numbers can look fine while the motion is not)

`harness/physics.py` rebuilds the ego's motion from each run's completed
`rollout.asl` (poses every 100 ms, the vehicle model's reported state, the
recorded human trajectory, other actors). It reads no config file.

Bounds (`harness/rules/physics.json`, each with its physical reason) and
`calibrate_physics.py` (`physics_calibration.txt`):

| Check | Bound | Clean maximum | Silent faults |
|---|---|---|---|
| max acceleration | 10 m/s² | 8.0 | up to 25.5 |
| max yaw rate | 2 rad/s | 0.89 | up to 31 |
| reported vs pose speed | 1 m/s | 0.31 | up to 29 |
| share of steps on the recording | 0.98 | 0.87 | 1.0 (rails) |
| contact with no collision scored | never | — | — |

Flagged: 0 of 150 B2, 0 of 77 S1 (about 70 other scenes), 0 of 6 pilot clean,
6 of 6 silent faults. A jerk bound (30 m/s³) fired on 5 S1 highway-speed runs
whose other signals were normal and was dropped (third differences of 10 Hz
poses; the linear MPC has no rate penalty); S1 is therefore not a pure
held-out set for the final bounds, and the campaign's runs are. The bounds are
off (`enabled: false`) in C1 and on in C2 (`run_campaign.sh`).

Auditor with the config files hidden (`eval_physics_audit.py`,
`physics_audit_eval.txt`), six silent runs, ten clean, one reference: with each
run's motion (`physics.txt`) it caught 6/6 with no false flag, reasoning from
the motion ("max_abs_accel 25.5 m/s2 … impossible vehicle motion"; "frac on
recording 1.0 … VaVAM never drove"). With summary metrics only it caught the 3
rails (distance to the recording 0.00) and missed all 3 kinematic runs.

Contact check, fixed 5 Oct: the first version compared centre distances in a
rough lane and fired live in C2 on a near-miss the simulator measured at 0.21 m
(`diag/c2s_021_a2`). It now overlaps real vehicle boxes from the log (every
actor, the ego included, is logged at its box centre; adding the rear-axle
offset again pushed the ego 1.47 m forward and made 37 false contacts in B2).
Clean runs show corner slivers up to 0.1 m², which the evaluator's rounded
bumpers ignore, and a real crash overlaps by 7 m² (`diag/s1_010`); the
threshold is 0.25 m², set after seeing those slivers. Recalibrated: 0 false of
256 clean runs, 6/6 silent faults.

Held-out check of all current bounds (plan handoff included) on every kept
C1 and C2 run, none of which set the plan-handoff bound
(`campaign_report.txt`): 0 of 202 runs without a silent fault flagged.

Why some kinematic runs pass physics, 6 Oct (`jerk_separation.py`,
`jerk_separation.txt`; every run on disk with a completed rollout, 43
kinematic and 644 others on the night of 6 Oct, rails left out; the script
reads whatever is on disk, so the count grows as C3 and C4 add runs). The kinematic controller peaks at
6.6–9.2 m/s² on gentle scenes, under the 10 m/s² bound, and clean S1 runs reach
8.0. Jerk does not rescue it: p99 jerk is at least 78.8 m/s³ on every kinematic
run but 101 on one clean highway run (`s1_009`, linear MPC, no fault); the
share of steps above 20 m/s³ overlaps on the same run; median jerk separates
with 3.80 against 3.70, too thin to set a bound on. A motion-only check cannot
tell this fault from a jerky clean run, so it is left to the Auditor, which
reads the config and compares with a reference from the same scene.

Plan faults (g2: 4 lateral bias 1.0 m, 4 plan freeze, 2 clean; two scenes),
6 Oct. The gate kept all 10: the motion is possible. The Auditor with configs
hidden caught 0/8 with one reference and with a reference per scene
(`plan_audit_eval_without_handoff.txt`): it is told not to flag bad driving,
and a corrupted plan looks like bad driving. The plan-handoff bound (median
sideways gap between the driver's plan and the controller's, after the
warm-up) separates them: clean runs 0 to 0.008 m over 258 runs, plan faults
0.14 to 1.0 m (`physics_calibration.txt`). Given that number in `physics.txt`,
the Auditor caught 4/8 with one reference (all lateral bias) and 8/8 with a
reference per scene, with no false flag (`plan_audit_eval.txt`); two more
audits of the per-scene condition with new seeds gave 8/8 and 8/8
(`plan_audit_repeat_80.txt`, `plan_audit_repeat_90.txt`). The plan
freeze shows only against a reference from the same scene.

Prediction for g3, written 6 Oct before it ran (4 waypoint noise 0.3 m, 4
lateral bias 0.3 m, 4 clean, on four scenes outside g2; physics live with
the current bounds, tier 1): the plan-handoff bound fails all 8 faulted
launches (0.3 m bias and noise of 0.3 m std both give a median sideways gap
well above 0.05 m) and none of the 4 clean ones. The config-blind Auditor
(`eval_plan_audit.py --queue g3_plan_queue`, chained after g3) catches the
lateral biases with a reference per scene; the waypoint noise is a guess.

Found on the way: the runtime retries a failed rollout inside one run
(`diag/s1_059` holds three rollouts, one complete). Neither the gate nor the
loop sees these retries; a scene that crashes is retried until it does not.

## Code invariants

1. Nonlinear MPC builds its CasADi cost once. Changing Python gain fields afterward
   does nothing. Linear MPC rebuilds Q and R in `update_gains` and sets the QP up on
   every solve. The paper uses linear MPC.
2. Both MPCs default `idx_start_penalty` so the first 1.0 s of a 2.0 s horizon has no
   tracking cost. Setting it to 0 did not fix the nominal crashes (`diag/test_penalty0_run_*`).
3. Nonlinear `set_rterm` penalizes input rate. Linear R penalizes the control itself.
   There is no input-rate penalty on the linear MPC, so nothing in its cost discourages
   chatter. A switching paper on the linear plant has to remember that.
4. Default terminal cost equals stage cost. `terminal_cost: riccati` on the linear
   controller solves the discrete Riccati equation and uses P. Failure falls back to
   stage cost and logs. The fallback means a "riccati" run can silently be a stage run
   if the solve fails.
5. Nonlinear MPC reports solver status from `solver_stats` (`solved`, `max_iter:N`,
   `infeasible`, `unconverged:…`). The controller CSV columns are `solve_time_ms,status`.
6. `controller_gain_schedule` is resolved in `src/runtime/alpasim_runtime/events/controller.py`
   and passed into the controller. A schedule entry applies when the control step index
   is at least `entry.step`. Base gains apply before the first entry.
7. `force_gt` replaces the driver plan with the recorded human trajectory. That is the
   frozen-perception condition for Phase B.
8. Plan fault injection (lateral bias, noise, freeze, horizon truncation) is
   `src/runtime/alpasim_runtime/plan_fault_injection.py`, off unless configured.
9. CATK weights are at `data/trafficsim-models/catk_v120` and run on CPU.
10. Deployed VaVAM verified with inference.context_length=8. Fits in 12 GB VRAM (11,758 MiB used: 5.6 GB driver, 4.4 GB PyCena, ~500 MB Xorg). Requires force_gt_duration_us >= 4000000 us (4.0s) so the FrameCache collects 8 frames at 2 Hz before policy handoff. Failing to set warm-up causes empty trajectory returns and immediate collisions.
11. `open_loop_collision` compares a plan with agents' recorded futures. It is a plan
    quality metric under replay traffic. Under CATK it is not a collision forecast.
12. `kinematic_ideal` does not emit steering and accel. `System._kinematic_ideal_step`
    moves the ego along the plan. It is not a controller plugin in the usual sense.
13. Every wizard run creates the Docker network `<log_dir name>_microservices_network`
    and leaves it, with its stopped containers, when the wizard exits. The default
    Docker pool holds about 30. `run_experiment.py` runs `docker compose down` after
    every run. A run launched any other way must be taken down by hand (`RUNBOOK.md`).

## Prior work the paper has to sit next to

Read before writing a related-work paragraph. Confirm venue and theorem statements;
several IDs were found by search (`researchideas.md` appendix).

| Work | Why it is in the paper |
|---|---|
| AURORA, arXiv 2511.07768 | Agentic supervisory redesign with a dwell-time theorem. Exogenous reference. We do not claim their theorem is false. We claim the exogeneity assumption does not hold for a camera on the car. |
| DiffTune-MPC, arXiv 2312.11384 | Analytical MPC cost tuning. Better than any LLM at choosing floats. We do not tune floats. |
| Poirot, ISSTA 2026; DVCA; CF-RCA | Module-substitution blame. They need interior modules. Cited only to say we are not doing that. |
| Bench2Drive-Robust, arXiv 2605.18059 | Latency benchmark for end-to-end policies. No supervisor, no switching. |

### Novelty check, 29 Sep 2026 (web search; items marked * were only seen as search results)

No paper found with our combination: a Simplex-style deterministic gate around
an LLM that operates a simulation or experiment batch, a finite action menu,
pre- and post-run checks that guarantee dataset validity, and a hand-written
policy as the baseline. "Simplex for LLM agents" itself is in print, so it is
not the claim. Do not write "first runtime assurance for LLM agents".

| Work | Overlap and difference |
|---|---|
| ADMITBench, arXiv 2608.03866 | Deterministic admissibility gate on industrial LLM advice; cites Simplex and Black-Box Simplex. Closest framing. Process plants, and a rule baseline is only future work. |
| From Detection to Action, arXiv 2606.28011 (same group) | LLM proposes recovery as state-machine paths, deterministic check, safety fallback. Closest structure. Physical plant, not an experiment pipeline. |
| Agentic Self-Healing for Data and AI Pipelines, arXiv 2608.01955 | Deterministic checks, LLM diagnosis, bounded remediation in MLOps. No Simplex framing, no rule baseline, no validity guarantee. |
| AgentSpec, ICSE 2026, arXiv 2503.18666* ; ShieldAgent, ICML 2025, arXiv 2503.22738* | Runtime rule enforcement on free-form agent actions; ShieldAgent's checker is itself an LLM. |
| arXiv 2609.06036, 2607.22868 | Runtime-assurance theory for LM planners behind an admission gate. No system. |
| AI Scientist, arXiv 2408.06292* ; Coscientist, Nature 624:570 (2023)* | LLM runs experiments with no verified gate. |
| TrainCheck, OSDI 2025, arXiv 2506.14813 ; RADAR, arXiv 2609.32528 | Silent-failure detection in training and agentic data analysis. Neither checks that a simulation config took effect. |
| PlannerForge, arXiv 2609.08965 ; AutoSimTest, arXiv 2501.11864 | LLM agents across AD/drone simulation testing. No recovery gate. |

Cite for Simplex and runtime assurance: Sha, "Using Simplicity to Control
Complexity", IEEE Software 18(4), 2001, doi:10.1109/MS.2001.936213; Seto et al.,
ACC 1998 (get the DOI); Black-Box Simplex, arXiv 2102.12981; Alshiekh et al.,
shielding, AAAI 2018. Our public `autolab-harness` repo appears in searches for
AlpaSim; check whether IV review is double-blind.

Still novel: runtime assurance moved from physical safety to experimental
validity; LLM versus rules on the same gated menu; a real end-to-end AV
simulation stack; an auditor for failures no rule covers.

## Repos

- This checkout, `/home/willvarner/alpasim`, is the working tree. Research notes live
  in `research/`.
- `/home/willvarner/autolab-harness` is a public snapshot of the old red-team harness.
  Its README describes a project we are not submitting.
