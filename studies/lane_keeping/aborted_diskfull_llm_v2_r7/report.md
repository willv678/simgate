# In straight lane-following scenes with other vehicles nearby, which combinations of sideways plan error and ego speed at hand-off make VaVAM leave its lane and hit someone or leave the road, and which 5 such cases, each on a different scene, are hardest?

Study `llm_v2_r7`: 0 kept runs on 0 scenes, varying lateral_bias_m, ego_speed_scale; 50 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The study cannot answer the question. The validity gate kept no runs, so there is no evidence about which combinations of plan bias and hand-off speed make the ego leave its lane, and none of the 5 challenging cases was confirmed, as the goal status says. Every run was rejected. The first runs (+0.5 m at 1.4x on the first five scenes) stopped with HALT, and every later run was rejected with no reason recorded. That includes the unperturbed baseline runs (0 m, 1.0x), which these scenes passed when they were chosen, so the cause is probably the run setup, not the policy. Also, every rejected run lists its controller as "linear", not VaVAM. So even if these runs had been kept, they would not have tested the policy the question asks about.

## Findings


## Open

- Why the gate rejected every run: the early +0.5 m / 1.4x runs halted, and the rest, including the 0 m / 1.0x baselines on several scenes, were rejected without a recorded reason. This needs fixing before any rerun, because baselines failing the gate point to a setup or pipeline fault rather than to the bias and speed settings.
- The controller recorded for every run is "linear", not VaVAM. Confirm that the study is configured to run VaVAM, or the results will not answer the question.
- Once 0 m / 1.0x baseline runs pass the gate on each scene, rerun the corner search at ±0.3 to ±0.5 m bias and 1.2x to 1.4x speed across the 12 scenes. Then repeat any setting that fails until its 90% range clears 0.5, so the 5 hardest cases (one per scene) can be confirmed.
- Whether any setting causes a side or front collision or leaving the road, and the ranking of near misses by closest approach, are both still unknown.

## Every setting


## Not kept by the gate

- lane_keeping_llm_v2_r7_001: not kept: HALT
- lane_keeping_llm_v2_r7_002: not kept: HALT
- lane_keeping_llm_v2_r7_003: not kept: HALT
- lane_keeping_llm_v2_r7_004: not kept: HALT
- lane_keeping_llm_v2_r7_005: not kept: HALT
- lane_keeping_llm_v2_r7_006: not kept: None
- lane_keeping_llm_v2_r7_007: not kept: None
- lane_keeping_llm_v2_r7_008: not kept: None
- lane_keeping_llm_v2_r7_009: not kept: None
- lane_keeping_llm_v2_r7_010: not kept: None
- lane_keeping_llm_v2_r7_011: not kept: None
- lane_keeping_llm_v2_r7_012: not kept: None
- lane_keeping_llm_v2_r7_013: not kept: None
- lane_keeping_llm_v2_r7_014: not kept: None
- lane_keeping_llm_v2_r7_015: not kept: None
- lane_keeping_llm_v2_r7_016: not kept: None
- lane_keeping_llm_v2_r7_017: not kept: None
- lane_keeping_llm_v2_r7_018: not kept: None
- lane_keeping_llm_v2_r7_019: not kept: None
- lane_keeping_llm_v2_r7_020: not kept: None
- lane_keeping_llm_v2_r7_021: not kept: None
- lane_keeping_llm_v2_r7_022: not kept: None
- lane_keeping_llm_v2_r7_023: not kept: None
- lane_keeping_llm_v2_r7_024: not kept: None
- lane_keeping_llm_v2_r7_025: not kept: None
- lane_keeping_llm_v2_r7_026: not kept: None
- lane_keeping_llm_v2_r7_027: not kept: None
- lane_keeping_llm_v2_r7_028: not kept: None
- lane_keeping_llm_v2_r7_029: not kept: None
- lane_keeping_llm_v2_r7_030: not kept: None
- lane_keeping_llm_v2_r7_031: not kept: None
- lane_keeping_llm_v2_r7_032: not kept: None
- lane_keeping_llm_v2_r7_033: not kept: None
- lane_keeping_llm_v2_r7_034: not kept: None
- lane_keeping_llm_v2_r7_035: not kept: None
- lane_keeping_llm_v2_r7_036: not kept: None
- lane_keeping_llm_v2_r7_037: not kept: None
- lane_keeping_llm_v2_r7_038: not kept: None
- lane_keeping_llm_v2_r7_039: not kept: None
- lane_keeping_llm_v2_r7_040: not kept: None
- lane_keeping_llm_v2_r7_041: not kept: None
- lane_keeping_llm_v2_r7_042: not kept: None
- lane_keeping_llm_v2_r7_043: not kept: None
- lane_keeping_llm_v2_r7_044: not kept: None
- lane_keeping_llm_v2_r7_045: not kept: None
- lane_keeping_llm_v2_r7_046: not kept: None
- lane_keeping_llm_v2_r7_047: not kept: None
- lane_keeping_llm_v2_r7_048: not kept: None
- lane_keeping_llm_v2_r7_049: not kept: None
- lane_keeping_llm_v2_r7_050: not kept: None

## Provenance

Plan: `plan.json` (rationale: **Scenes.** All 12 scenes have recorded turn "none" and passed at 0 delay, so any failure can be attributed to the bias and speed settings. Each is tagged lead_vehicle and/or merge_cut_in, which means a vehicle ahead or alongside. Each also had the ego actually driving (roughly 35 to 250 m, up to 6 to 30 m/s). Most came within about 1.3 m of another actor, so a sideways shift has someone to meet.

**Scenes left out:**
- scenes that already failed at 0 delay
- scenes that turn
- scenes where the ego barely moved (a few metres)
- scenes tagged mainly pedestrian_crossing

**Fixed settings.**
- Traffic is replayed as recorded, so the other actors follow their recorded tracks, like the scripted vehicles in Euro NCAP LSS. No actor knob is varied, so no retime_class is set.
- Planner delay stays at 0 and waypoint noise at 0, the defaults.

**Budget and goal.** Budget is 5 rounds × 10 runs = 50, as the brief asks. The goal is top_k with k=5, distinct scenes and high_min 0.5. It stops early once 5 scenes each have a setting whose 90% range lies above 0.5, which takes about 3 to 5 failing repeats per setting. That leaves roughly half the budget for searching the 9 bias × 5 speed grid.

**What this plan cannot answer:**
- The tags cannot tell whether a vehicle is in an adjacent, oncoming or overtaking lane, or ahead in the ego's own lane. So the LSS oncoming and overtaking cases cannot be chosen on purpose, only found if they happen.
- There is no separate lane-departure measure. Drifting out of the lane only counts when it ends in a collision or going off the road.
- Near misses are not part of the stopping goal. They can only be ranked from the reported closest approach.
- With speed scales above 1, the ego starts behind its recorded start, off the recording for the first second or two of the warm-up.
- Replayed traffic cannot react to the ego. Rear-end hits are excluded, so a slow ego (0.6x) may look safer than it would among reactive traffic.
- 50 runs over 12 scenes and 45 settings is a sparse search. It may miss hard cases and cannot map the full grid.). Report written by claude-opus-5-5 from `results` in 10 s; every count above is computed from the queue, not written by the model.

0 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
