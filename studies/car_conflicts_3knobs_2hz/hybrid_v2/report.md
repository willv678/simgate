# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_v2`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 8 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study met only part of its goal: it confirmed 2 of the 5 cases it was asked for. Both are on different scenes, and every repeat failed at both. The first is 096988dd with no time shift, the car at 1.25x and the ego at 1.2x (S6). The second is 19f339ba with no time shift, the car at 1.25x and the ego at 1.4x (S36). Both are side collisions where the policy was at fault: the ego drifted left out of its lane, against its route, into a car in the next lane. That car was never the retimed car, so the failures seem to come mostly from a faster ego at hand-off, not from the retimed car's timing. On the other eight scenes nothing failed, but most settings there got only one run, which is a hint, not evidence that those scenes are safe.

## Findings

- On 096988dd, with no time shift, the car at 1.25x and the ego at 1.2x, every repeat failed. In each run the policy's path bent left, against a STRAIGHT or RIGHT command, and the ego's front or front-left hit vehicle 41 in the adjacent left lane. The triage puts every one of these on the policy, and none was flagged as a possible rendering artifact.
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_015, car_conflicts_3knobs_2hz_hybrid_v2_021, car_conflicts_3knobs_2hz_hybrid_v2_022, car_conflicts_3knobs_2hz_hybrid_v2_023)
- On 096988dd, single runs at the same car speed with the ego at its recorded speed passed, with the car at 1.25x and at 1.0x. This suggests the ego's speed at hand-off is what tips this scene into failing, but it rests on one run per setting.
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_016)
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_002)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_015, car_conflicts_3knobs_2hz_hybrid_v2_021, car_conflicts_3knobs_2hz_hybrid_v2_022, car_conflicts_3knobs_2hz_hybrid_v2_023)
- On 19f339ba, with no time shift, the car at 1.25x and the ego at 1.4x, every repeat failed. Each time the ego braked hard on an open road, with the lead car 40 m or more ahead, drifted left, and actor 1 coming up in the left lane hit its front-left. One run also took a hit to the rear. The triage puts every one of these on the policy.
  - S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_026, car_conflicts_3knobs_2hz_hybrid_v2_031, car_conflicts_3knobs_2hz_hybrid_v2_032, car_conflicts_3knobs_2hz_hybrid_v2_033)
- On 19f339ba, single runs at the same car speed passed with the ego at 1.2x and 1.0x, and so did a run at the recorded setting. On this scene failure seems to start only at the top of the ego speed range.
  - S33: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_018)
  - S34: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_004)
  - S35: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_017)
  - S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_026, car_conflicts_3knobs_2hz_hybrid_v2_031, car_conflicts_3knobs_2hz_hybrid_v2_032, car_conflicts_3knobs_2hz_hybrid_v2_033)
- The same ego-speed increase did not cause failures on other scenes. With the car at 1.25x and the ego at 1.4x, repeats on 023b7fcc all passed. With the car at 1.5x and the ego at 1.2x, repeats on 1c45ce3a also all passed. The upper end of the 90% range at these two settings is below 0.5.
  - S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_055, car_conflicts_3knobs_2hz_hybrid_v2_056, car_conflicts_3knobs_2hz_hybrid_v2_057)
  - S41: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_051, car_conflicts_3knobs_2hz_hybrid_v2_052, car_conflicts_3knobs_2hz_hybrid_v2_053, car_conflicts_3knobs_2hz_hybrid_v2_054)
- The 0cf6368d scene with the car at its recorded speed and the ego at 1.2x passed every repeat, and so did a single run with the car at 1.25x and the ego at 1.4x, so this scene showed no sign of failing.
  - S16: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_058, car_conflicts_3knobs_2hz_hybrid_v2_059, car_conflicts_3knobs_2hz_hybrid_v2_060)
  - S18: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_035)
  - S19: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_041)
- Several settings that passed came closest to failing and are the best leads for the remaining three cases: 09a95ffa (car 1.5x, ego 1.2x), 0cf6368d (car 1.25x, ego 1.2x), 12855a41 (car 1.25x, ego 1.0x, at no shift and at -0.5 s), and 1c45ce3a (car 1.5x, ego 1.0x). The brief ranks these near misses after outright failures.
  - S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_036_a3)
  - S18: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_035)
  - S27: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_003, car_conflicts_3knobs_2hz_hybrid_v2_027)
  - S25: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_012)
  - S40: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_030)

## Open

- Three of the five cases are still missing. On each of the strongest near-miss scenes (09a95ffa, 0cf6368d, 12855a41, 1c45ce3a), the next step is to raise the ego to 1.4x and run repeats there, since both confirmed failures came from a faster ego.
- The search covered only part of the range. Time shifts went only to ±0.5 s, never out to ±2 s. The car's speed never went below 1.0x, and the ego's speed never went below 1.0x. Whether an earlier or later cut-in, or a slower car or ego, causes failures is untested.
- 096988dd was never run with the ego at 1.4x, and 19f339ba was never run with the ego between 1.2x and 1.4x. Repeats there would show where on each scene failure begins.
- 0dbb91dd, 187e6244 and 0e899dd3 got only one or two settings with one run each, so they are barely explored.
- Both confirmed failures hit a car in the adjacent lane, not the retimed key car. The study cannot tell whether the retimed car's speed of 1.25x matters at all. Repeats at the same ego speed with the car at 1.0x would settle this.
- With the ego above 1.0x, it starts behind its recorded start and is off the recording for the first second or two of warm-up. No run was flagged as a possible artifact, but it is worth checking that the unprompted hard braking on 19f339ba is not caused by that warm-up.
- Some runs at 1c45ce3a (car 1.25x, ego 1.2x; and shift +0.5 s, car 1.5x, ego 1.0x) and at 09a95ffa (car 1.5x, ego 1.2x) were not kept and had to be re-run or halted. Kept runs on 1c45ce3a at both of those settings would fill the gap.
- The 2 Hz planning rate was set with a control timestep of 500 ms but nothing checked it. The claim that the policy fails less at 2 Hz than at 10 Hz was not tested here.

## Why the runs failed (triage from the video and log)

turned_into_actor 7, other 1

- car_conflicts_3knobs_2hz_hybrid_v2_015: turned_into_actor, policy at fault: yes. On a multi-lane highway with a RIGHT command, the ego's output trajectory (orange) bent left, away from the planned route that went right, and the ego slid into the adjacent left lane. Its front-left corner struck vehicle 41, which was travelling alongside in that lane, and the camera shows the white vehicle right against the ego's left side at impact.
- car_conflicts_3knobs_2hz_hybrid_v2_021: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's planned path (orange) bent left out of the ego's lane while the human route (green) went straight. The ego drifted left into actor 41, which was coming up alongside in the left lane, and its front-left clipped that car at 7.2s.
- car_conflicts_3knobs_2hz_hybrid_v2_022: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego's plan bent left out of its lane, against a STRAIGHT and then RIGHT route command, while the recorded human kept going straight. The ego cut into the left lane and its front hit vehicle 41, which was right alongside it in that lane.
- car_conflicts_3knobs_2hz_hybrid_v2_023: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego's planned path bent left, the opposite way from the recorded route and the RIGHT command. It drifted about 1.6 m left into the adjacent lane and its front struck actor 41, a white SUV passing on the left, while the ego was slowing to about 4.6 m/s.
- car_conflicts_3knobs_2hz_hybrid_v2_026: turned_into_actor, policy at fault: yes. On an open highway with no lead vehicle close (gap 40–50 m), the ego braked hard for no clear reason, from 23.7 to 6.7 m/s, and its planned path veered left toward the adjacent lane. Actor 1 had been following just behind on the left and came alongside as the ego slowed, and the ego's front-left drifted into it.
- car_conflicts_3knobs_2hz_hybrid_v2_031: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with the nearest car ahead 40–53 m away, the ego braked hard for no visible reason (23.7 → 6.9 m/s) and drifted left across the lane line. Its front-left then hit actor 1, which was catching up in the left lane after the ego slowed. Meanwhile the recorded human kept going at speed.
- car_conflicts_3knobs_2hz_hybrid_v2_032: turned_into_actor, policy at fault: yes. On an open highway with the lead car 40+ m ahead and pulling away, the ego braked hard for no visible reason, slowing from 23.7 to 6.6 m/s. While braking, it drifted left toward the adjacent lane, and its front hit actor 1, which was coming up alongside on the left.
- car_conflicts_3knobs_2hz_hybrid_v2_033: other, policy at fault: yes. After handoff on an open highway with no close lead (gap 40+ m), the policy braked hard for no visible reason, slowing from 23.7 to 6.6 m/s in 3 s and ending up about 9.6 m behind where the human was at that moment. Replayed traffic that was behind it, including actor 1 in the lane to the left, then caught up: actor 1 drew alongside, the ego's front-left corner, sitting near the left lane line, touched it at 7.6 s, and something also hit the ego's rear.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_001)
- S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_038)
- S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_055, car_conflicts_3knobs_2hz_hybrid_v2_056, car_conflicts_3knobs_2hz_hybrid_v2_057)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_016)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_002)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_015, car_conflicts_3knobs_2hz_hybrid_v2_021, car_conflicts_3knobs_2hz_hybrid_v2_022, car_conflicts_3knobs_2hz_hybrid_v2_023)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_047)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_008)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_019, car_conflicts_3knobs_2hz_hybrid_v2_025)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_024)
- S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_036_a3)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_045)
- S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_046)
- S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_048)
- S15: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_043)
- S16: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_058, car_conflicts_3knobs_2hz_hybrid_v2_059, car_conflicts_3knobs_2hz_hybrid_v2_060)
- S17: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_007)
- S18: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_035)
- S19: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_041)
- S20: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_042)
- S21: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_044)
- S22: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_006)
- S23: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_009)
- S24: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_034)
- S25: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_012)
- S26: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_020)
- S27: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_003, car_conflicts_3knobs_2hz_hybrid_v2_027)
- S28: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_011)
- S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_028)
- S30: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_040)
- S31: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_005)
- S32: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_039)
- S33: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_018)
- S34: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_004)
- S35: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_017)
- S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_026, car_conflicts_3knobs_2hz_hybrid_v2_031, car_conflicts_3knobs_2hz_hybrid_v2_032, car_conflicts_3knobs_2hz_hybrid_v2_033)
- S37: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_014)
- S38: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_049)
- S39: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_010, car_conflicts_3knobs_2hz_hybrid_v2_029)
- S40: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_030)
- S41: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_051, car_conflicts_3knobs_2hz_hybrid_v2_052, car_conflicts_3knobs_2hz_hybrid_v2_053, car_conflicts_3knobs_2hz_hybrid_v2_054)
- S42: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_037)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_v2_013: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_013_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_013_a3: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_v2_036: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_036_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_050: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_050_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_050_a3: not kept: HALT

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

0 of 66 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
