# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `random_confirm_r5`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 5 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed one challenging case out of the five it aimed for. On scene 19f339ba, with the car shifted 2 s earlier, the car's speed at 0.5x and the ego at its recorded speed, every repeat failed, and the 90% range lies above 0.5 (S29). The failure is not the expected cut-in or lead-vehicle conflict. On an open highway with no car close ahead, the policy braked hard for no visible reason. Replayed traffic behind it, which cannot react, then rear-ended it and clipped its front-right corner. That is counted as an at-fault front collision even though the ego never drove into anything, so it is a real phantom-braking fault, but the collision itself depends on non-reactive replay. No other setting on any of the 10 scenes failed. Most were run once or twice, which shows only that failures there are not common, not that they are absent.

## Findings

- The only confirmed failing case is on 19f339ba with the car 2 s earlier, the car at 0.5x speed and the ego at 1.0x. Every repeat failed, and none of the failures was flagged as a possible rendering artifact.
  - S29: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_027, car_conflicts_3knobs_2hz_random_confirm_r5_031, car_conflicts_3knobs_2hz_random_confirm_r5_041)
- The cause in every S29 failure was the policy braking hard on an open highway with no car close ahead. Replayed traffic coming from behind then hit the ego, first in the rear and then at the front-right corner, so the 'front collision' is a consequence of the policy's unneeded braking and not of running into the retimed car.
  - S29: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_027, car_conflicts_3knobs_2hz_random_confirm_r5_031, car_conflicts_3knobs_2hz_random_confirm_r5_041)
- A nearby setting on the same scene, with the car 1.5 s earlier at 0.75x speed, did not fail in its single run. Other settings on 19f339ba did not fail either. So the failure looks tied to the most extreme corner of the car's timing and speed range, but the evidence is thin.
  - S29: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_027, car_conflicts_3knobs_2hz_random_confirm_r5_031, car_conflicts_3knobs_2hz_random_confirm_r5_041)
  - S30: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_056_a2)
  - S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_036)
  - S32: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_049)
- Settings repeated several times without a failure had near misses but no confirmed failures. These are the near-miss candidates the brief ranks next. On 0e899dd3: car 1.5 s later at 0.75x, ego 0.8x. On 096988dd: car 0.5 s earlier at 1.25x, ego 1.0x. On 09a95ffa: car 1 s later at 2x, ego 1.0x. On 023b7fcc: car 0.5 s later at 0.5x, ego 0.6x. On 12855a41: car 0.5 s earlier at 1.0x, ego 1.2x.
  - S22: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_040, car_conflicts_3knobs_2hz_random_confirm_r5_042, car_conflicts_3knobs_2hz_random_confirm_r5_051)
  - S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_006_a2, car_conflicts_3knobs_2hz_random_confirm_r5_013, car_conflicts_3knobs_2hz_random_confirm_r5_022, car_conflicts_3knobs_2hz_random_confirm_r5_033, car_conflicts_3knobs_2hz_random_confirm_r5_052)
  - S11: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_019, car_conflicts_3knobs_2hz_random_confirm_r5_021, car_conflicts_3knobs_2hz_random_confirm_r5_032, car_conflicts_3knobs_2hz_random_confirm_r5_044, car_conflicts_3knobs_2hz_random_confirm_r5_053)
  - S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_004, car_conflicts_3knobs_2hz_random_confirm_r5_011, car_conflicts_3knobs_2hz_random_confirm_r5_023, car_conflicts_3knobs_2hz_random_confirm_r5_034, car_conflicts_3knobs_2hz_random_confirm_r5_045, car_conflicts_3knobs_2hz_random_confirm_r5_055)
  - S26: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_010, car_conflicts_3knobs_2hz_random_confirm_r5_012, car_conflicts_3knobs_2hz_random_confirm_r5_024, car_conflicts_3knobs_2hz_random_confirm_r5_035)
- Two single-run settings came close without failing: 096988dd with the car 2 s later at 1.5x speed, and 1c45ce3a with the car 0.5 s later at 0.75x and the ego at 0.6x. They are hints, not rates.
  - S7: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_037, car_conflicts_3knobs_2hz_random_confirm_r5_043)
  - S33: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_050, car_conflicts_3knobs_2hz_random_confirm_r5_054)
- Scenes 0cf6368d and 0dbb91dd never came close to a conflict at any setting tried. Retiming their key car seems to create little interaction, at least at the settings sampled.
  - S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_038)
  - S14: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_016)
  - S15: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_001)
  - S16: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_026)
  - S17: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_005)
  - S18: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_039)
  - S19: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_008)

## Open

- Whether the S29 failure depends on the knobs at all. The policy braked with no car close ahead, so the scene should be run at the recorded setting and at other timing and speed values on 19f339ba to see whether the phantom braking happens there too.
- Whether S29 would still end in a collision if traffic reacted to the ego. A run with reactive traffic would separate the policy's braking fault from replay traffic that cannot react.
- The other four cases were not found. The best candidates for repeats and local search are S22, S5, S11, S7 and S33, in particular earlier or later timing and more extreme car speeds around those settings.
- 187e6244 got only one kept run (S28), so it was barely searched, even though it came within 0.23 m of another actor as recorded.
- On 1c45ce3a, two runs with the ego at 1.4x halted and were not kept, so high ego speeds on that scene remain untested.
- Many settings had only one run, and the space has 270 cells per scene, so 'no failure' at most settings is weak evidence.

## Why the runs failed (triage from the video and log)

other 2, actor_hit_ego 1

- car_conflicts_3knobs_2hz_random_confirm_r5_027: actor_hit_ego, policy at fault: yes. On an open multi-lane highway with no vehicle ahead, the policy braked hard for no reason, from 16.9 to 5.0 m/s. By the failure it was about 21 m behind where the recorded car was, and a following car had already rear-ended it. At 7.6 s, replayed actor 28 came up from behind on the right and cut into the ego's lane, hitting its front-right corner, which the metrics count as an at-fault front collision.
- car_conflicts_3knobs_2hz_random_confirm_r5_031: other, policy at fault: yes. On a clear multi-lane highway with no lead vehicle (the only gap reading is about 52 m or more), the policy braked hard for no visible reason, from 16.9 to 5.4 m/s after handoff. Replayed traffic coming from behind, which follows the recording and can't react, first hit the ego's rear and then hit it again at 7.6 s: actor 28 caught up and overlapped the ego's front corner while the ego sat about 0.8 m off the recorded path, about 20 m behind where the human car was.
- car_conflicts_3knobs_2hz_random_confirm_r5_041: other, policy at fault: yes. On an open multi-lane highway with no lead vehicle closer than about 50 m, the ego braked hard for no clear reason, from 16.9 to 5.4 m/s, and fell about 21 m behind its recorded position. The replayed vehicles behind it, which do not react to the ego, caught up: one rear-ended it, and then actor 28 ran into its right front corner, which was flagged as an at-fault front collision even though the ego never ran into anything.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_057)
- S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_004, car_conflicts_3knobs_2hz_random_confirm_r5_011, car_conflicts_3knobs_2hz_random_confirm_r5_023, car_conflicts_3knobs_2hz_random_confirm_r5_034, car_conflicts_3knobs_2hz_random_confirm_r5_045, car_conflicts_3knobs_2hz_random_confirm_r5_055)
- S3: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_047)
- S4: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_048)
- S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_006_a2, car_conflicts_3knobs_2hz_random_confirm_r5_013, car_conflicts_3knobs_2hz_random_confirm_r5_022, car_conflicts_3knobs_2hz_random_confirm_r5_033, car_conflicts_3knobs_2hz_random_confirm_r5_052)
- S6: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_003)
- S7: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_037, car_conflicts_3knobs_2hz_random_confirm_r5_043)
- S8: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_046)
- S9: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_007_a2, car_conflicts_3knobs_2hz_random_confirm_r5_015)
- S10: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_030)
- S11: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_019, car_conflicts_3knobs_2hz_random_confirm_r5_021, car_conflicts_3knobs_2hz_random_confirm_r5_032, car_conflicts_3knobs_2hz_random_confirm_r5_044, car_conflicts_3knobs_2hz_random_confirm_r5_053)
- S12: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_017)
- S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_038)
- S14: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_016)
- S15: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_001)
- S16: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_026)
- S17: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_005)
- S18: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_039)
- S19: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_008)
- S20: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_059)
- S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_060)
- S22: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_040, car_conflicts_3knobs_2hz_random_confirm_r5_042, car_conflicts_3knobs_2hz_random_confirm_r5_051)
- S23: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_002)
- S24: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_009, car_conflicts_3knobs_2hz_random_confirm_r5_014, car_conflicts_3knobs_2hz_random_confirm_r5_025)
- S25: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_020)
- S26: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_010, car_conflicts_3knobs_2hz_random_confirm_r5_012, car_conflicts_3knobs_2hz_random_confirm_r5_024, car_conflicts_3knobs_2hz_random_confirm_r5_035)
- S27: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_058)
- S28: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_029)
- S29: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_027, car_conflicts_3knobs_2hz_random_confirm_r5_031, car_conflicts_3knobs_2hz_random_confirm_r5_041)
- S30: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_056_a2)
- S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_036)
- S32: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_049)
- S33: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r5_050, car_conflicts_3knobs_2hz_random_confirm_r5_054)

## Not kept by the gate

- car_conflicts_3knobs_2hz_random_confirm_r5_006: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r5_007: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r5_018: not kept: HALT
- car_conflicts_3knobs_2hz_random_confirm_r5_028: not kept: HALT
- car_conflicts_3knobs_2hz_random_confirm_r5_056: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
