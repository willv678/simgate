# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna_r3`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 5 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only two of the five cases were confirmed: scene 19f339ba with the car at its recorded timing, 2x speed and the ego at 1.4x (S25), and scene 096988dd with the car 2 s early, 1.25x speed and the ego at 1.2x (S5). Every repeat at those two settings failed, and both ranges lie above 0.5. Even so, the retimed car did not seem to cause either failure. In every failure the ego slowed for no reason, drifted left and hit a different car in the next lane, with no conflict ahead. The policy was at fault each time, and none of the failures look like simulator artifacts. On the other eight scenes nothing failed. Most of those settings ran only once or twice, so they are hints, not proof that the scenes are safe.

## Findings

- On scene 19f339ba, with the car at its recorded timing, 2x speed and the ego at 1.4x, every kept run failed, and the failure rate is confirmed above 0.5.
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_004, car_conflicts_3knobs_2hz_hybrid_optuna_r3_014, car_conflicts_3knobs_2hz_hybrid_optuna_r3_015, car_conflicts_3knobs_2hz_hybrid_optuna_r3_016)
- On scene 096988dd, with the car 2 s early, 1.25x speed and the ego at 1.2x, every kept run failed, and the failure rate is confirmed above 0.5.
  - S5: 096988dd at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_009, car_conflicts_3knobs_2hz_hybrid_optuna_r3_011, car_conflicts_3knobs_2hz_hybrid_optuna_r3_013, car_conflicts_3knobs_2hz_hybrid_optuna_r3_012_a2)
- Both confirmed cases fail the same way, and it isn't a cut-in or lead-vehicle conflict. There was no car close ahead. The ego braked or slowed for no reason and drifted left across the lane line. Its front then hit a car passing in the left lane: actor 1 on 19f339ba and actor 41 on 096988dd, neither of them the car the study retimed. The triage puts the policy at fault every time and flags no rendering artifacts.
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_004, car_conflicts_3knobs_2hz_hybrid_optuna_r3_014, car_conflicts_3knobs_2hz_hybrid_optuna_r3_015, car_conflicts_3knobs_2hz_hybrid_optuna_r3_016)
  - S5: 096988dd at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_009, car_conflicts_3knobs_2hz_hybrid_optuna_r3_011, car_conflicts_3knobs_2hz_hybrid_optuna_r3_013, car_conflicts_3knobs_2hz_hybrid_optuna_r3_012_a2)
- The best-repeated settings on the other scenes never failed, and their ranges stay below 0.5. They are scene 023b7fcc with the car 1.5 s late at recorded speed and the ego at 1.4x, 09a95ffa at two settings, and 1c45ce3a with the car 2 s early at 1.5x and the ego at 1.2x.
  - S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_025, car_conflicts_3knobs_2hz_hybrid_optuna_r3_033, car_conflicts_3knobs_2hz_hybrid_optuna_r3_043, car_conflicts_3knobs_2hz_hybrid_optuna_r3_058, car_conflicts_3knobs_2hz_hybrid_optuna_r3_059, car_conflicts_3knobs_2hz_hybrid_optuna_r3_060)
  - S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_040, car_conflicts_3knobs_2hz_hybrid_optuna_r3_051, car_conflicts_3knobs_2hz_hybrid_optuna_r3_052, car_conflicts_3knobs_2hz_hybrid_optuna_r3_053, car_conflicts_3knobs_2hz_hybrid_optuna_r3_054)
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_026, car_conflicts_3knobs_2hz_hybrid_optuna_r3_031, car_conflicts_3knobs_2hz_hybrid_optuna_r3_032, car_conflicts_3knobs_2hz_hybrid_optuna_r3_042)
  - S26: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_037, car_conflicts_3knobs_2hz_hybrid_optuna_r3_041, car_conflicts_3knobs_2hz_hybrid_optuna_r3_056, car_conflicts_3knobs_2hz_hybrid_optuna_r3_057, car_conflicts_3knobs_2hz_hybrid_optuna_r3_055_a3)
- The closest near misses without a failure, which the brief ranks next, were on 023b7fcc (car 1.5 s late, ego 1.4x), 09a95ffa (car 1.5 s late at 1.5x, ego 1.2x) and 187e6244 (car 2 s early at 0.5x, ego 1.4x). All three had the ego above its recorded speed.
  - S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_025, car_conflicts_3knobs_2hz_hybrid_optuna_r3_033, car_conflicts_3knobs_2hz_hybrid_optuna_r3_043, car_conflicts_3knobs_2hz_hybrid_optuna_r3_058, car_conflicts_3knobs_2hz_hybrid_optuna_r3_059, car_conflicts_3knobs_2hz_hybrid_optuna_r3_060)
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_026, car_conflicts_3knobs_2hz_hybrid_optuna_r3_031, car_conflicts_3knobs_2hz_hybrid_optuna_r3_032, car_conflicts_3knobs_2hz_hybrid_optuna_r3_042)
  - S22: 187e6244 at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_002, car_conflicts_3knobs_2hz_hybrid_optuna_r3_017, car_conflicts_3knobs_2hz_hybrid_optuna_r3_018)
- On scene 0dbb91dd, every setting tried, all with the car at 2x, had no close approach at all. The search found nothing there to follow.
  - S13: 0dbb91dd at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_003)
  - S14: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_039)
  - S15: 0dbb91dd at actor_time_shift_s 2, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_050)

## Open

- Does the retimed car matter at all? Both confirmed failures were collisions with a different car in the adjacent lane. Re-run 19f339ba and 096988dd with that car at its recorded timing and speed, keeping the same ego speed (1.4x and 1.2x), to see whether ego speed alone brings on the drift and braking.
- Where does the failure begin on each knob? Step the ego speed down toward 1.0x on 19f339ba and 096988dd, with a few repeats per step.
- Three more cases are still missing. The best places to look are the near-miss settings on 187e6244 (S22) and 12855a41 (S19), with more runs near them. Each new candidate needs about five repeats to clear 0.5.
- Most settings on 0cf6368d, 0e899dd3, 12855a41, 187e6244 and 1c45ce3a ran only once or twice. No-failure there is a hint, not a rate.
- Two runs on 1c45ce3a halted and were not kept: car on time at 1.25x with the ego at 1.4x, and car 0.5 s early at 2x with the ego at 1.4x. Those settings remain untested and should be re-run.

## Why the runs failed (triage from the video and log)

turned_into_actor 8

- car_conflicts_3knobs_2hz_hybrid_optuna_r3_004: turned_into_actor, policy at fault: yes. On an open highway with nothing close ahead (lead gap over 43 m), the ego braked hard from 24 to 7 m/s for no reason and drifted left over the lane line. Its front clipped actor 1, which had been behind it in the left lane and was now alongside after the ego slowed.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_009: turned_into_actor, policy at fault: yes. On a multi-lane highway in the rain, the ego slowed from 6.7 to 4.6 m/s and drifted left, ending up 1.7 m off the recorded path, even though the route command had changed to RIGHT. Actor 41 passed it in the left lane, and the ego's front hit 41's right rear as the ego crossed into that lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's plan (orange) kept bending left, away from the route (green). At about 5 m/s the ego drifted into the left lane and its front hit actor 41, which was driving alongside in that lane. There was no lead-vehicle conflict: the gap ahead was about 20 m.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_013: turned_into_actor, policy at fault: yes. After handoff, the ego slowed from about 6.6 to 4.6 m/s and drifted left toward the adjacent lane, roughly following the human's left lane-change path, while actor 41 came up from behind-left in that lane. At 7.2 s the ego's front-left corner clipped 41 as it drew level, about 1.3 m off the recorded path. The ego was slower than the human, which probably let 41 reach its side.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_014: turned_into_actor, policy at fault: yes. On an open multi-lane highway with no lead within about 45 m, the ego braked hard for no visible reason, from 22 to 6 m/s. At the same time its planned path drifted left toward the left lane line. Vehicle 1 was overtaking in the left lane, and the ego's front-left clipped it as it went by (front collision at 8.1 s). The hard braking likely also explains the later rear contact.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_015: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no lead vehicle within about 43 m, the ego braked hard for no visible reason, slowing from 23.7 to 7.5 m/s and falling well behind its recorded position. At the same time it drifted left toward the lane line and side-swiped actor 1, which was coming up in the adjacent left lane.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_016: turned_into_actor, policy at fault: yes. On an open highway with no lead vehicle within about 43 m, the ego braked hard for no visible reason, slowing from 23.7 to 7.1 m/s, while drifting about 1.2 m left of the recorded path. Actor 1 had been behind in the left lane and drew alongside because the ego slowed, and the ego's front-left corner hit it across the lane line.
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_012_a2: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded path bore right, but the ego drifted left toward the line into the next lane while slowing from 6.7 to 4.6 m/s. Its front-left corner hit actor 41, which was passing it on the left in that lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_006, car_conflicts_3knobs_2hz_hybrid_optuna_r3_030)
- S2: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_047)
- S3: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_024)
- S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_025, car_conflicts_3knobs_2hz_hybrid_optuna_r3_033, car_conflicts_3knobs_2hz_hybrid_optuna_r3_043, car_conflicts_3knobs_2hz_hybrid_optuna_r3_058, car_conflicts_3knobs_2hz_hybrid_optuna_r3_059, car_conflicts_3knobs_2hz_hybrid_optuna_r3_060)
- S5: 096988dd at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_009, car_conflicts_3knobs_2hz_hybrid_optuna_r3_011, car_conflicts_3knobs_2hz_hybrid_optuna_r3_013, car_conflicts_3knobs_2hz_hybrid_optuna_r3_012_a2)
- S6: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_001, car_conflicts_3knobs_2hz_hybrid_optuna_r3_020)
- S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_040, car_conflicts_3knobs_2hz_hybrid_optuna_r3_051, car_conflicts_3knobs_2hz_hybrid_optuna_r3_052, car_conflicts_3knobs_2hz_hybrid_optuna_r3_053, car_conflicts_3knobs_2hz_hybrid_optuna_r3_054)
- S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_026, car_conflicts_3knobs_2hz_hybrid_optuna_r3_031, car_conflicts_3knobs_2hz_hybrid_optuna_r3_032, car_conflicts_3knobs_2hz_hybrid_optuna_r3_042)
- S9: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_023)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_035, car_conflicts_3knobs_2hz_hybrid_optuna_r3_049)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_034)
- S12: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_005)
- S13: 0dbb91dd at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_003)
- S14: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_039)
- S15: 0dbb91dd at actor_time_shift_s 2, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_050)
- S16: 0e899dd3 at actor_time_shift_s -2, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_038)
- S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_028)
- S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_008, car_conflicts_3knobs_2hz_hybrid_optuna_r3_019)
- S19: 12855a41 at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_022, car_conflicts_3knobs_2hz_hybrid_optuna_r3_048)
- S20: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_007, car_conflicts_3knobs_2hz_hybrid_optuna_r3_029)
- S21: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_036)
- S22: 187e6244 at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_002, car_conflicts_3knobs_2hz_hybrid_optuna_r3_017, car_conflicts_3knobs_2hz_hybrid_optuna_r3_018)
- S23: 187e6244 at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_046)
- S24: 187e6244 at actor_time_shift_s 1, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_027)
- S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_004, car_conflicts_3knobs_2hz_hybrid_optuna_r3_014, car_conflicts_3knobs_2hz_hybrid_optuna_r3_015, car_conflicts_3knobs_2hz_hybrid_optuna_r3_016)
- S26: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_037, car_conflicts_3knobs_2hz_hybrid_optuna_r3_041, car_conflicts_3knobs_2hz_hybrid_optuna_r3_056, car_conflicts_3knobs_2hz_hybrid_optuna_r3_057, car_conflicts_3knobs_2hz_hybrid_optuna_r3_055_a3)
- S27: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_045)
- S28: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r3_010)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_optuna_r3_012: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_021: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_044: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_055: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r3_055_a2: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 26 s; every count above is computed from the queue, not written by the model.

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
