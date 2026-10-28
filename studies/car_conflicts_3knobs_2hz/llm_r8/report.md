# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `llm_r8`: 59 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 9 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Repeats confirmed only two of the five challenging cases the brief asked for, each on a different scene: 096988dd with the car at its recorded timing and speed and the ego at 1.4x (S13), and 19f339ba with the car as recorded and the ego at 1.2x (S43). In both, the trigger was the faster ego at hand-off, not the retimed car. Every failure was the policy's fault and none looks like a simulator artifact: the ego braked or slowed, drifted left out of its lane and hit a car driving alongside in the next lane, which was never the car the study retimed. A third setting on 096988dd (S12: car 1 s earlier and 1.5x, ego 1.2x) failed every time, but it shares a scene with S13 and has only two runs, so it is a strong hint rather than a separate case. The 90% ranges for the two confirmed settings only just clear 0.5, and no other scene produced a failure in the budget.

## Findings

- On 096988dd, raising only the ego's speed at hand-off to 1.4x (car at recorded timing and speed) made the policy fail on every repeat. Each time it slowed and angled left, and its front-left corner hit actor 41 in the left lane while the lead truck stayed well ahead. This is a confirmed case, with the policy at fault.
  - S13: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_001_a2, car_conflicts_3knobs_2hz_llm_r8_011, car_conflicts_3knobs_2hz_llm_r8_012_a2)
- On 19f339ba, raising only the ego's speed to 1.2x (car as recorded) made the policy fail on every repeat. It braked hard with no close lead, its path bent left, and it clipped actor 1 in the left lane. Getting rear-ended came after the hard braking and is not what made these failures. This is a confirmed case, with the policy at fault.
  - S43: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_005, car_conflicts_3knobs_2hz_llm_r8_013, car_conflicts_3knobs_2hz_llm_r8_014)
- On 096988dd, also moving the car 1 s earlier at 1.5x with the ego at 1.2x failed in both runs, in the same way: a left drift into actor 41. This suggests that on this scene the faster ego does the work and the car's retiming does not matter, but two runs are not a confirmed rate.
  - S12: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_002, car_conflicts_3knobs_2hz_llm_r8_015)
  - S13: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_001_a2, car_conflicts_3knobs_2hz_llm_r8_011, car_conflicts_3knobs_2hz_llm_r8_012_a2)
- The same ego-only change (car as recorded, ego at 1.4x) did not fail on the other scenes tried. Each of those settings has a single run, so this is only a hint that the left-drift failure belongs to the scene.
  - S9: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_003)
  - S17: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_031)
  - S24: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_033)
  - S25: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_010)
  - S29: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_032)
  - S33: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_007)
  - S41: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_009_a2)
- The two settings repeated most without a failure were near misses with a slowed car and a fast ego: 023b7fcc with the car at 0.75x and the ego at 1.4x, and 12855a41 with the car at 0.5x and the ego at 1.4x. Their failure rates are bounded well below 0.5, so these are near misses, not failure cases.
  - S8: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_llm_r8_044, car_conflicts_3knobs_2hz_llm_r8_051, car_conflicts_3knobs_2hz_llm_r8_052, car_conflicts_3knobs_2hz_llm_r8_053, car_conflicts_3knobs_2hz_llm_r8_054, car_conflicts_3knobs_2hz_llm_r8_055)
  - S31: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_llm_r8_036, car_conflicts_3knobs_2hz_llm_r8_056, car_conflicts_3knobs_2hz_llm_r8_057, car_conflicts_3knobs_2hz_llm_r8_058, car_conflicts_3knobs_2hz_llm_r8_059, car_conflicts_3knobs_2hz_llm_r8_060)
- Retiming the cut-in or lead car (earlier and faster, or later and slower) produced no failure on 023b7fcc, 09a95ffa, 0cf6368d, 0e899dd3, 12855a41 or 187e6244, though most of those settings ran only once.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_024)
  - S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_004)
  - S3: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_016_a2)
  - S4: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_017)
  - S5: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_025)
  - S6: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_046_a3)
  - S7: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_035)
  - S10: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_045)
  - S11: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_038)
  - S14: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_029)
  - S15: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_039_a2)
  - S16: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_049_a2)
  - S18: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_022)
  - S19: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_llm_r8_020, car_conflicts_3knobs_2hz_llm_r8_021)
  - S20: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_037)
  - S21: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_023)
  - S22: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_048)
  - S23: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_047)
  - S26: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_028)
  - S27: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_040)
  - S28: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_050)
  - S30: 12855a41 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_018)
  - S32: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_043)
  - S34: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_041)
  - S35: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_042)
  - S36: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_008)
  - S37: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_026)
  - S38: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_027)
  - S39: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_030)
  - S40: 187e6244 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_019)
  - S42: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_006)

## Open

- Three more confirmed cases on other scenes are still needed. The next candidates are the closest near misses without a failure, all on 023b7fcc and 12855a41 (S10, S7, S34, S32). Each ran once and is worth repeating at several runs, possibly with the ego pushed to its 1.4x limit and the car's timing shifted further.
- Whether S12 on 096988dd is a separate failure from S13: more repeats would put its rate surely above 0.5, but it would still not count as a different scene.
- Whether 19f339ba also fails at ego 1.4x, and 096988dd at ego 1.2x with the car as recorded. Neither was run, so where ego speed starts to cause failure on these scenes is unknown.
- Whether the left-drift into an adjacent car depends on ego speed alone. The retimed key car was never the one hit, so a study that varies ego speed only, or retimes the adjacent cars (actor 41 on 096988dd, actor 1 on 19f339ba), would test this directly.
- 1c45ce3a produced no kept run (its run halted), and 0dbb91dd was tried only once. Both scenes are effectively unexplored.
- This interface did not check the 2 Hz planning rate (control_timestep_us of 500000 was set, but not verified), so the comparison with the 10 Hz results in HZ.md rests on that assumption.

## Why the runs failed (triage from the video and log)

turned_into_actor 8

- car_conflicts_3knobs_2hz_llm_r8_002: turned_into_actor, policy at fault: yes. On a wet multi-lane freeway with the command switching to RIGHT, the ego slowed from 6.7 to 4.4 m/s and drifted left toward the lane line instead of holding its lane or moving right. Its front hit actor 41, which was passing in the left lane, about 1.7 m left of the recorded human path.
- car_conflicts_3knobs_2hz_llm_r8_005: turned_into_actor, policy at fault: yes. On a straight highway with a STRAIGHT command, the ego braked hard for no clear reason (20.6 to 8.6 m/s, with the lead pulling away) and turned left toward the next lane. Its front-left corner hit actor 1, which was just ahead in that left lane. The ego was also rear-ended at some point, likely because of the sudden braking.
- car_conflicts_3knobs_2hz_llm_r8_001_a2: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego's plan (orange path) kept angling left toward the next lane while it slowed from about 7.9 to 4.6 m/s. Actor 41 was coming up alongside in that left lane, and the ego's front-left corner swiped it at 7.2 s, about 1.3 m off the recorded human path; the lead truck stayed 17–22 m ahead the whole time and was not involved.
- car_conflicts_3knobs_2hz_llm_r8_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT (RIGHT in the last frame), the policy's planned path bent left, away from the recorded path, which stays in the lane. The ego slowed from 7.9 to 4.6 m/s while it angled into the lane to its left. At 7.2 s its front corner hit vehicle 41, which was travelling alongside in that lane.
- car_conflicts_3knobs_2hz_llm_r8_013: turned_into_actor, policy at fault: yes. After handoff on a straight highway, the ego braked hard (20.6 to 8.3 m/s) with no close lead, the gap ahead having opened to about 50 m. Actor 1 in the left adjacent lane drew alongside and moved ahead. The ego's path then bent left, about 1.1 m off the recorded trajectory, and its front-left corner clipped actor 1.
- car_conflicts_3knobs_2hz_llm_r8_014: turned_into_actor, policy at fault: yes. After handoff, the ego braked hard for no clear reason, from about 20 to 8 m/s, even though the lead car was pulling away. Its planned path also bent left toward the adjacent lane. Actor 1, which had been beside the ego on the left, moved ahead as the ego slowed, and the ego's front-left corner hit actor 1's rear-right corner. Being rear-ended afterwards is a result of the sudden braking.
- car_conflicts_3knobs_2hz_llm_r8_015: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy's planned path (orange) bent left toward the next lane, while the recorded human path stayed straight and later curved right, with the command switching to RIGHT. The ego slowed from 6.7 to 5.0 m/s and drifted left into actor 41, which was driving alongside in the left lane, so the ego's front-left hit it at 7.2 s, about 1.4 m off the recorded path.
- car_conflicts_3knobs_2hz_llm_r8_012_a2: turned_into_actor, policy at fault: yes. While slowing behind the truck on a multi-lane highway, the ego drifted left into the next lane, against its recorded path and the later RIGHT command. Its front-left hit car 41, which was driving alongside in that lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_024)
- S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_004)
- S3: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_016_a2)
- S4: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_017)
- S5: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_025)
- S6: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_046_a3)
- S7: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_035)
- S8: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_llm_r8_044, car_conflicts_3knobs_2hz_llm_r8_051, car_conflicts_3knobs_2hz_llm_r8_052, car_conflicts_3knobs_2hz_llm_r8_053, car_conflicts_3knobs_2hz_llm_r8_054, car_conflicts_3knobs_2hz_llm_r8_055)
- S9: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_003)
- S10: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_045)
- S11: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_038)
- S12: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_002, car_conflicts_3knobs_2hz_llm_r8_015)
- S13: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_001_a2, car_conflicts_3knobs_2hz_llm_r8_011, car_conflicts_3knobs_2hz_llm_r8_012_a2)
- S14: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_029)
- S15: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_039_a2)
- S16: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_049_a2)
- S17: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_031)
- S18: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_022)
- S19: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_llm_r8_020, car_conflicts_3knobs_2hz_llm_r8_021)
- S20: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_037)
- S21: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_023)
- S22: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_048)
- S23: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_047)
- S24: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_033)
- S25: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_010)
- S26: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_028)
- S27: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_040)
- S28: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_050)
- S29: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_032)
- S30: 12855a41 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_018)
- S31: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_llm_r8_036, car_conflicts_3knobs_2hz_llm_r8_056, car_conflicts_3knobs_2hz_llm_r8_057, car_conflicts_3knobs_2hz_llm_r8_058, car_conflicts_3knobs_2hz_llm_r8_059, car_conflicts_3knobs_2hz_llm_r8_060)
- S32: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_043)
- S33: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_007)
- S34: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_041)
- S35: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_042)
- S36: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_008)
- S37: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_026)
- S38: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_027)
- S39: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_030)
- S40: 187e6244 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_019)
- S41: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_009_a2)
- S42: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r8_006)
- S43: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r8_005, car_conflicts_3knobs_2hz_llm_r8_013, car_conflicts_3knobs_2hz_llm_r8_014)

## Not kept by the gate

- car_conflicts_3knobs_2hz_llm_r8_001: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_009: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_012: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_016: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_034: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r8_039: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_046: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_049: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_r8_046_a2: not kept: RE-RUN

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

0 of 68 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
