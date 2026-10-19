# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna_r5`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 6 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 2 of the 5 cases it set out to find. Two combinations, on two different scenes, make the policy collide at a rate surely above 0.5: in 096988dd, the car 1.5 s early at recorded speed with the ego at 1.2x (S4); and in 19f339ba, the car 1 s late at 1.5x speed with the ego at 1.4x (S26). Every repeat at both settings failed. Every failure was the policy's fault and none looks like a simulator artifact. In each one the ego drifted left out of its lane and its front hit a car driving alongside in the next lane. That car was not the one the study retimed, so the knobs probably make an existing weakness show up rather than set up the conflict. None of the other 8 scenes failed at any setting tried. Most of those settings ran only once or twice, so they are hints, not rates, and the goal of 5 confirmed cases was not met.

## Findings

- In scene 096988dd, with the cut-in/lead car 1.5 s early at recorded speed and the ego at 1.2x speed at hand-off, every repeat collided. The route command was straight then right, but the policy's plan bent left, and the ego's front hit a pickup (actor 41) in the adjacent left lane.
  - S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_001, car_conflicts_3knobs_2hz_hybrid_optuna_r5_011, car_conflicts_3knobs_2hz_hybrid_optuna_r5_012)
- In scene 19f339ba, with the car 1 s late at 1.5x speed and the ego at 1.4x, every repeat collided. On an open highway the ego braked hard for no visible reason with the car ahead pulling away, drifted left, and its front hit actor 1, which was catching up in the left lane.
  - S26: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_002, car_conflicts_3knobs_2hz_hybrid_optuna_r5_013, car_conflicts_3knobs_2hz_hybrid_optuna_r5_014_a3)
- Scene 096988dd also failed at a quite different setting (car 0.5 s late at 2x speed, ego at recorded speed), the same way: a left drift into actor 41. That was a single run, so it is a hint, not a rate. It suggests this scene's weakness depends little on the exact knob values. It does not add a distinct confirmed case.
  - S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_010)
  - S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_001, car_conflicts_3knobs_2hz_hybrid_optuna_r5_011, car_conflicts_3knobs_2hz_hybrid_optuna_r5_012)
- All failures were the policy's fault (turned_into_actor). None was flagged as a possible rendering or off-trajectory artifact. In each one the car that was hit was a neighbour in the next lane, not the car the study retimed (track 2 in 096988dd, track 18 in 19f339ba).
  - S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_001, car_conflicts_3knobs_2hz_hybrid_optuna_r5_011, car_conflicts_3knobs_2hz_hybrid_optuna_r5_012)
  - S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_010)
  - S26: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_002, car_conflicts_3knobs_2hz_hybrid_optuna_r5_013, car_conflicts_3knobs_2hz_hybrid_optuna_r5_014_a3)
- The settings repeated most without a failure stay below 0.5 even at the top of their range, so they are not challenging cases: 023b7fcc (car 1.5 s late, ego 1.2x), 0e899dd3 (car 1 s late at 1.5x, ego 1.2x), 12855a41 (car 0.5 s early at 2x speed) and 1c45ce3a (car 1.5 s early at recorded speed).
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_048, car_conflicts_3knobs_2hz_hybrid_optuna_r5_054, car_conflicts_3knobs_2hz_hybrid_optuna_r5_055, car_conflicts_3knobs_2hz_hybrid_optuna_r5_056)
  - S17: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_022, car_conflicts_3knobs_2hz_hybrid_optuna_r5_031, car_conflicts_3knobs_2hz_hybrid_optuna_r5_032, car_conflicts_3knobs_2hz_hybrid_optuna_r5_033)
  - S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_044, car_conflicts_3knobs_2hz_hybrid_optuna_r5_045, car_conflicts_3knobs_2hz_hybrid_optuna_r5_057, car_conflicts_3knobs_2hz_hybrid_optuna_r5_058)
  - S27: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_050, car_conflicts_3knobs_2hz_hybrid_optuna_r5_051, car_conflicts_3knobs_2hz_hybrid_optuna_r5_053, car_conflicts_3knobs_2hz_hybrid_optuna_r5_052_a2)
- The closest calls without a collision, which the brief ranks next, were on 12855a41 (the cut-in car 0.5 s early at 2x speed), 187e6244 (the car 1 s early at 2x speed with the ego slowed to 0.6x), 09a95ffa (car 1.5 s early at 1.5x, ego 1.2x) and 023b7fcc (car 1.5 s late, ego 1.2x).
  - S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_044, car_conflicts_3knobs_2hz_hybrid_optuna_r5_045, car_conflicts_3knobs_2hz_hybrid_optuna_r5_057, car_conflicts_3knobs_2hz_hybrid_optuna_r5_058)
  - S22: 187e6244 at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_007, car_conflicts_3knobs_2hz_hybrid_optuna_r5_015, car_conflicts_3knobs_2hz_hybrid_optuna_r5_016)
  - S6: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_024, car_conflicts_3knobs_2hz_hybrid_optuna_r5_036, car_conflicts_3knobs_2hz_hybrid_optuna_r5_037)
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_048, car_conflicts_3knobs_2hz_hybrid_optuna_r5_054, car_conflicts_3knobs_2hz_hybrid_optuna_r5_055, car_conflicts_3knobs_2hz_hybrid_optuna_r5_056)
- Scene 0dbb91dd showed no conflict at all at either setting tried, even with the ego at 1.4x.
  - S12: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_025)
  - S13: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_003)

## Open

- Three of the five cases are still missing. To fill them, repeat the strongest near-miss settings (S18 on 12855a41, S22 on 187e6244, S6 on 09a95ffa, S20 on 12855a41) and search near them, especially at the extremes of ego speed and car timing.
- Whether the knobs matter in 096988dd and 19f339ba is not settled, because the car that was hit was never the retimed one. Repeating each scene at the recorded knob values with the same ego speed (and nearby settings, e.g. S26 with the ego at 1.0x) would show whether ego speed alone triggers the left drift.
- Only one run on 096988dd at car 0.5 s late, 2x speed (S5) failed. Repeating it would show whether that scene fails across a broad region.
- Most settings on 0cf6368d, 187e6244, 0dbb91dd, 0e899dd3 and 023b7fcc ran once or twice. Their upper bounds are too wide to rule out a high failure rate.
- Two runs on 1c45ce3a with the ego at 1.4x (r5_004 and r5_028) were halted and not kept. It is unknown whether that scene fails at high ego speed; it needs re-running at those settings.
- The 2 Hz planning rate came from the configuration (control_timestep_us 500000), not from a knob the study varied or checked. Nothing here compares 2 Hz with 10 Hz.

## Why the runs failed (triage from the video and log)

turned_into_actor 7

- car_conflicts_3knobs_2hz_hybrid_optuna_r5_001: turned_into_actor, policy at fault: yes. The route command was STRAIGHT and then RIGHT, but the ego's plan bent left and it drifted into the lane on its left. Its front hit actor 41, a white pickup that was driving in that lane next to and just ahead of the ego. The recorded human stayed in the original lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_002: turned_into_actor, policy at fault: yes. On a straight, open highway, the ego braked hard for no reason, from 23.7 to 7 m/s, while the gap to the car ahead grew from 34 to 53 m, so it fell behind the recorded car. It then drifted left toward the next lane and its front hit actor 1, which was catching up in that lane alongside the ego's left.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_010: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (RIGHT at the end), the policy's planned path bent left. The ego drifted left out of its lane at about 5 m/s, against the recorded path, and its front-left hit actor 41, which was travelling alongside it in the adjacent left lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_011: turned_into_actor, policy at fault: yes. The route command switched to RIGHT and the recorded path kept the ego in its lane. Instead, the policy's planned path bent left, and the ego drifted into the adjacent left lane. Its front struck the white pickup (actor 41), which was travelling alongside and slightly ahead in that lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_012: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT and then RIGHT command, the ego slowed from about 6.7 to 4.3 m/s and its planned path drifted left toward the next lane, about 1.6 m off the human trajectory. Actor 41, a pickup passing on the left, moved alongside and ahead, and the ego's front corner ran into it while the ego was edging into that lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_013: turned_into_actor, policy at fault: yes. On an open highway with the car ahead pulling away, the ego braked hard (23.7 to 7.1 m/s) for no reason while drifting left toward the lane line. Because it slowed so much, actor 1 in the left lane caught up, and the ego's front-left corner hit it.
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_014_a3: turned_into_actor, policy at fault: yes. On an open highway with the nearest car ahead 40+ m away, the ego braked hard for no clear reason (18 → 4 m/s) and drifted left off the recorded path toward the next lane. Actor 1 was passing on the left in that lane, and at 8.6 s the ego's front clipped it. Actor 28 also closed in behind the slowing ego (a rear contact was recorded).

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_039)
- S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_048, car_conflicts_3knobs_2hz_hybrid_optuna_r5_054, car_conflicts_3knobs_2hz_hybrid_optuna_r5_055, car_conflicts_3knobs_2hz_hybrid_optuna_r5_056)
- S3: 023b7fcc at actor_time_shift_s 2, actor_speed_scale 1.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_027, car_conflicts_3knobs_2hz_hybrid_optuna_r5_038)
- S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_001, car_conflicts_3knobs_2hz_hybrid_optuna_r5_011, car_conflicts_3knobs_2hz_hybrid_optuna_r5_012)
- S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_010)
- S6: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_024, car_conflicts_3knobs_2hz_hybrid_optuna_r5_036, car_conflicts_3knobs_2hz_hybrid_optuna_r5_037)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_009, car_conflicts_3knobs_2hz_hybrid_optuna_r5_020)
- S8: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_049, car_conflicts_3knobs_2hz_hybrid_optuna_r5_060)
- S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_005, car_conflicts_3knobs_2hz_hybrid_optuna_r5_030)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_029)
- S11: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_040)
- S12: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_025)
- S13: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_003)
- S14: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_046, car_conflicts_3knobs_2hz_hybrid_optuna_r5_047_a2)
- S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_021)
- S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_006, car_conflicts_3knobs_2hz_hybrid_optuna_r5_019, car_conflicts_3knobs_2hz_hybrid_optuna_r5_059)
- S17: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_022, car_conflicts_3knobs_2hz_hybrid_optuna_r5_031, car_conflicts_3knobs_2hz_hybrid_optuna_r5_032, car_conflicts_3knobs_2hz_hybrid_optuna_r5_033)
- S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_044, car_conflicts_3knobs_2hz_hybrid_optuna_r5_045, car_conflicts_3knobs_2hz_hybrid_optuna_r5_057, car_conflicts_3knobs_2hz_hybrid_optuna_r5_058)
- S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_008, car_conflicts_3knobs_2hz_hybrid_optuna_r5_017, car_conflicts_3knobs_2hz_hybrid_optuna_r5_018)
- S20: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_026, car_conflicts_3knobs_2hz_hybrid_optuna_r5_034, car_conflicts_3knobs_2hz_hybrid_optuna_r5_035)
- S21: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_042)
- S22: 187e6244 at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_007, car_conflicts_3knobs_2hz_hybrid_optuna_r5_015, car_conflicts_3knobs_2hz_hybrid_optuna_r5_016)
- S23: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_041)
- S24: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_043)
- S25: 187e6244 at actor_time_shift_s 1, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_023)
- S26: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_002, car_conflicts_3knobs_2hz_hybrid_optuna_r5_013, car_conflicts_3knobs_2hz_hybrid_optuna_r5_014_a3)
- S27: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r5_050, car_conflicts_3knobs_2hz_hybrid_optuna_r5_051, car_conflicts_3knobs_2hz_hybrid_optuna_r5_053, car_conflicts_3knobs_2hz_hybrid_optuna_r5_052_a2)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_optuna_r5_004: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_014: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_014_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_028: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_047: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r5_052: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: these are the scenes tagged merge_cut_in or lead_vehicle that did not fail in the earlier run at the recorded setting, have a recorded car the study can retime (lead_vehicle or cut_in), and drove far enough for a conflict to develop. Most of them already came close to another actor as recorded: 023b7fcc came within 0.02 m, 096988dd 0.01 m, 19f339ba 0.03 m, 12855a41 0.08 m, and 0dbb91dd and 187e6244 0.23 m. Those are the most promising places to look for rare failures.

Left out:
- Scenes that were nearly stationary (0fa7060f, 15dd433e, 0ac02819, 10d64934) or very slow (01d503d4, 098e2482, 11fce928, 1bfd39ec).
- Scenes with no car the study can retime (for example 04749bb9, 05f35348, 0ce6f2a3, 166fe701).
- Scenes whose only key actor is a crossing vehicle at an intersection (02eadd92, 054b5901).

Note that 01d503d4 appears twice in the scene list.

Retiming and settings:
- Traffic is replay, as the brief asks, with retime_class automobile.
- Each scene retimes only its key car. In 12855a41 that is the cut-in car 31 rather than the lead car 5.
- All three knobs span exactly the ranges in the brief: timing ±2 s, car speed 0.5x to 2x, ego speed 0.6x to 1.4x.
- The controller is linear MPC.

Goal: top_k with k=5, distinct scenes, high_min 0.5. This matches the request for the 5 most challenging cases, each confirmed by repeats.

Limits:
- The budget is tight. With 90% ranges, a setting needs roughly 5 failures out of 5 runs to lie surely above 0.5. Confirming 5 cases therefore takes about 25 runs, which leaves about 35 runs to search a 270-cell grid on 10 scenes. If failures are as rare as the brief expects, the study may end with fewer than 5 confirmed cases. It would then report the strongest candidates and the near misses, which the brief ranks next.
- The 2 Hz planning rate is not a knob in this interface. The plan assumes the runs use VaVAM's 2 Hz rhythm as configured; nothing here sets it or checks it. planner_delay_us, lateral_bias_m and waypoint_noise_std stay at their defaults.
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

0 of 64 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
