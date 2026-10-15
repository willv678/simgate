# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `random_confirm`: 59 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 2 of the 5 cases it was after, so the goal was not met. Both confirmed cases failed on every kept run. Each range lies just above 0.5, so they are confirmed, but only narrowly. The first is scene 023b7fcc with the lead car moved 1.5 s earlier at 0.5x speed and the ego at its recorded speed (S1). Here the policy takes over already close behind a slow lead car and does not brake hard enough. The second is scene 096988dd with the car at its recorded timing, 1.5x car speed and the ego at 1.4x (S7). Here the policy drifts left out of its lane and sideswipes a car beside it, which is not the retimed car. A third case on 096988dd failed the same way but ran only once, so it is a hint rather than a rate (S5). No setting on the other seven scenes that ran failed, and one scene in the plan was never run.

## Findings

- On 023b7fcc, moving the lead car 1.5 s earlier at 0.5x speed, with the ego at its recorded speed, makes the policy hit the lead car's rear on every run, and the range lies above 0.5. The triage reads this as a failure to brake: the ego takes over a few metres behind a slower car, eases off only gently and runs into it. A rear hit from the car behind came after the front collision each time. For one run, triage marked the policy's fault as unclear, because the gap at hand-off was about 1 m.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_026, car_conflicts_3knobs_2hz_random_confirm_031, car_conflicts_3knobs_2hz_random_confirm_041)
- On 023b7fcc this failure looks sensitive to the car's timing. At 1.0 s earlier, with the same car speed and ego speed, the single run did not fail and did not come close. One run is not enough to locate the edge.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_026, car_conflicts_3knobs_2hz_random_confirm_031, car_conflicts_3knobs_2hz_random_confirm_041)
  - S2: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_058)
- On 096988dd, a faster car (1.5x) at its recorded timing combined with a faster ego (1.4x) fails on every run, and the range lies above 0.5. In each run the policy steered left of its route into the next lane and hit actor 41 front-on or side-on. Actor 41 is not the retimed car (track 2), so the policy's lane keeping caused these failures, not the retimed car's cut-in.
  - S7: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_005, car_conflicts_3knobs_2hz_random_confirm_011, car_conflicts_3knobs_2hz_random_confirm_021)
- 096988dd also failed in its single run with the car 2 s earlier at 1.25x and the ego at its recorded speed, in the same way (drifting left into actor 41). With a slower car and a slower ego (0.5x, 0.8x) it did not fail but came close. This suggests the drift-left failure happens across much of this scene, not just at one combination.
  - S5: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_038)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_060)
  - S7: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_005, car_conflicts_3knobs_2hz_random_confirm_011, car_conflicts_3knobs_2hz_random_confirm_021)
- Several repeated settings on other scenes did not fail on any run, and their ranges lie below 0.5. These include 09a95ffa (car 0.5 s later, 1.5x, ego 0.8x), 12855a41 (recorded timing, ego 1.4x; and car 0.5x, ego 0.6x), 19f339ba (car 2 s later at 0.75x or 1.25x), 0e899dd3 (car 1 s earlier; car 2 s later at 1.25x with ego 1.2x) and 0cf6368d (car 1 s later at 2x, ego 1.4x).
  - S11: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_003, car_conflicts_3knobs_2hz_random_confirm_013, car_conflicts_3knobs_2hz_random_confirm_034, car_conflicts_3knobs_2hz_random_confirm_045)
  - S27: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_006, car_conflicts_3knobs_2hz_random_confirm_014, car_conflicts_3knobs_2hz_random_confirm_024)
  - S28: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_027, car_conflicts_3knobs_2hz_random_confirm_032, car_conflicts_3knobs_2hz_random_confirm_044, car_conflicts_3knobs_2hz_random_confirm_052)
  - S32: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_036, car_conflicts_3knobs_2hz_random_confirm_042, car_conflicts_3knobs_2hz_random_confirm_051)
  - S33: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_009, car_conflicts_3knobs_2hz_random_confirm_012, car_conflicts_3knobs_2hz_random_confirm_023, car_conflicts_3knobs_2hz_random_confirm_033)
  - S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_004, car_conflicts_3knobs_2hz_random_confirm_015, car_conflicts_3knobs_2hz_random_confirm_025)
  - S25: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_040, car_conflicts_3knobs_2hz_random_confirm_043, car_conflicts_3knobs_2hz_random_confirm_053)
  - S15: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_029, car_conflicts_3knobs_2hz_random_confirm_035, car_conflicts_3knobs_2hz_random_confirm_055)
- The closest calls without a collision were on 19f339ba, 096988dd, 09a95ffa and 0e899dd3. By the brief's ranking these near misses come next after the two confirmed cases.
  - S32: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_036, car_conflicts_3knobs_2hz_random_confirm_042, car_conflicts_3knobs_2hz_random_confirm_051)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_060)
  - S31: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_046)
  - S33: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_009, car_conflicts_3knobs_2hz_random_confirm_012, car_conflicts_3knobs_2hz_random_confirm_023, car_conflicts_3knobs_2hz_random_confirm_033)
  - S12: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_017, car_conflicts_3knobs_2hz_random_confirm_054)
  - S25: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_040, car_conflicts_3knobs_2hz_random_confirm_043, car_conflicts_3knobs_2hz_random_confirm_053)
- On 0dbb91dd the ego never came close to another actor in any setting tried, even though as recorded it came within 0.23 m. The ranges for single runs are wide, so this scene is not cleared.
  - S16: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_050)
  - S17: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_008)
  - S18: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_007)
  - S19: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_030)

## Open

- Three more confirmed cases on different scenes are still missing. Scene 187e6244 is in the plan but was never run. 1c45ce3a had only one kept run; a second (car 1.5 s later, 2x, ego 1.4x) halted and was not kept.
- Whether the single failure on 096988dd (car 2 s earlier, 1.25x, ego 1.0x) repeats. Repeating it would only add a second case on the same scene, so it would not count towards the goal. Running 096988dd at the recorded car timing and speed with ego 1.4x would show whether the ego's speed alone causes the drift left into actor 41.
- Where the failure edge lies on 023b7fcc between the car 1.5 s and 1.0 s earlier, and whether the faster ego speeds fail too. Repeats at -1.0 s and at -1.5 s with ego 1.2x would show this.
- Whether the near misses on 19f339ba (car 0.5x, ego 1.2x), 09a95ffa (car 1.5 s later, 1.25x, ego 1.2x) and 0e899dd3 tip into failure at harsher neighbouring settings, such as an earlier car timing or a faster ego. Each needs several repeats before it can count as confirmed.

## Why the runs failed (triage from the video and log)

turned_into_actor 4, no_brake_for_lead 3

- car_conflicts_3knobs_2hz_random_confirm_005: turned_into_actor, policy at fault: yes. On a multi-lane highway, the route said RIGHT, but the policy's planned path (orange) kept heading left of the route line, and the ego drifted left into the next lane. Actor 41 was coming up on the left from behind, and the ego's front struck it at about 5 m/s. By then the ego was 1.9 m off the recorded human path.
- car_conflicts_3knobs_2hz_random_confirm_011: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from about 7.9 to 5.4 m/s and drifted left toward the left lane, roughly where the recorded human changed lanes. That put it alongside actor 41, which was coming up from behind in that lane, and the two had a side collision at 7.2 s.
- car_conflicts_3knobs_2hz_random_confirm_021: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a STRAIGHT and then RIGHT route command, the policy's own trajectory (orange) kept heading left. The ego drifted about 1.5 m left of the recorded path into the next lane and sideswiped vehicle 41, which was travelling alongside on its left.
- car_conflicts_3knobs_2hz_random_confirm_026: no_brake_for_lead, policy at fault: yes. In slow, dense traffic going straight, the ego took over at 4.7 s already close behind lead car 12, going about 4.2 m/s and closing on it. It barely slowed (4.2 to 4.0 m/s in the first 0.5 s) and ran into 12's rear at 5.7 s. Actor 56 also hit the ego from behind, but that came after the front collision.
- car_conflicts_3knobs_2hz_random_confirm_031: no_brake_for_lead, policy at fault: yes. The ego was following slower car 12 in its lane in slow highway traffic, closing at about 1.4 m/s. After handoff at 4.7 s, with a 5.5 m gap, the policy only eased from 4.2 to 3.4 m/s and planned a late swerve to the left instead of braking firmly, and its front hit car 12 at 5.7 s. The rear contact flagged in the data came after this front collision.
- car_conflicts_3knobs_2hz_random_confirm_038: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the policy steered left away from the recorded straight path into the next lane. Its front struck actor 41, which was holding its own lane just ahead-left of the ego, at about 4.7 m/s.
- car_conflicts_3knobs_2hz_random_confirm_041: no_brake_for_lead, policy at fault: unclear. In slow freeway traffic, the policy took over at 4.7 s already very close behind the slower lead vehicle 12 in the same lane (about 1 m bumper to bumper, closing at about 1.4 m/s). It only slowed gently, from 4.2 to 3.4 m/s, and ran into 12's rear about 1 s later, at 5.7 s. Separately, vehicle 56 behind also hit the ego's rear at some point.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_026, car_conflicts_3knobs_2hz_random_confirm_031, car_conflicts_3knobs_2hz_random_confirm_041)
- S2: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_058)
- S3: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_049)
- S4: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_048)
- S5: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_038)
- S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_060)
- S7: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_005, car_conflicts_3knobs_2hz_random_confirm_011, car_conflicts_3knobs_2hz_random_confirm_021)
- S8: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_047)
- S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_059)
- S10: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_020, car_conflicts_3knobs_2hz_random_confirm_022)
- S11: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_003, car_conflicts_3knobs_2hz_random_confirm_013, car_conflicts_3knobs_2hz_random_confirm_034, car_conflicts_3knobs_2hz_random_confirm_045)
- S12: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_017, car_conflicts_3knobs_2hz_random_confirm_054)
- S13: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_001)
- S14: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_019)
- S15: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_029, car_conflicts_3knobs_2hz_random_confirm_035, car_conflicts_3knobs_2hz_random_confirm_055)
- S16: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_050)
- S17: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_008)
- S18: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_007)
- S19: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_030)
- S20: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_057)
- S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_004, car_conflicts_3knobs_2hz_random_confirm_015, car_conflicts_3knobs_2hz_random_confirm_025)
- S22: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_039)
- S23: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_010)
- S24: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_002)
- S25: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_040, car_conflicts_3knobs_2hz_random_confirm_043, car_conflicts_3knobs_2hz_random_confirm_053)
- S26: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_016)
- S27: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_006, car_conflicts_3knobs_2hz_random_confirm_014, car_conflicts_3knobs_2hz_random_confirm_024)
- S28: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_027, car_conflicts_3knobs_2hz_random_confirm_032, car_conflicts_3knobs_2hz_random_confirm_044, car_conflicts_3knobs_2hz_random_confirm_052)
- S29: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_028)
- S30: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_018)
- S31: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_046)
- S32: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_036, car_conflicts_3knobs_2hz_random_confirm_042, car_conflicts_3knobs_2hz_random_confirm_051)
- S33: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_009, car_conflicts_3knobs_2hz_random_confirm_012, car_conflicts_3knobs_2hz_random_confirm_023, car_conflicts_3knobs_2hz_random_confirm_033)
- S34: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_056)

## Not kept by the gate

- car_conflicts_3knobs_2hz_random_confirm_037: not kept: HALT

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

0 of 60 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
