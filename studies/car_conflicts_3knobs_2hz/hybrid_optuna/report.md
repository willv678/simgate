# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna`: 58 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 7 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 3 of the 5 cases it set out to find, so the goal was not met. Each confirmed case is on a different scene and pairs a fast ego at hand-off (1.2x to 1.4x its recorded speed) with a retimed car. On 19f339ba the car runs 1 s late at 0.5x speed with the ego at 1.4x (S25). On 023b7fcc the car runs 2 s early at 0.5x with the ego at 1.4x (S1). On 096988dd the car keeps its recorded timing at 1.5x with the ego at 1.2x (S2). Every repeat at these three settings failed, and the policy was at fault every time, with no possible simulator artifacts. But each has only four or five runs, so its range only just clears 0.5. On the other six scenes that produced kept runs, nothing failed, and 1c45ce3a produced no kept runs at all.

## Findings

- On 19f339ba, with the car 1 s late at 0.5x and the ego at 1.4x, every repeat failed. Each time, on an open highway with nothing close ahead, the policy braked hard for no visible reason, drifted left and hit actor 1 as it came alongside in the left lane. That car is not the one the study retimed, so the knobs seem to matter mainly through the ego's speed and position, not through a direct conflict with the retimed car. One triage labels the cause 'other', but it describes the same sequence.
  - S25: 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_035, car_conflicts_3knobs_2hz_hybrid_optuna_041, car_conflicts_3knobs_2hz_hybrid_optuna_042, car_conflicts_3knobs_2hz_hybrid_optuna_043, car_conflicts_3knobs_2hz_hybrid_optuna_044)
- On 023b7fcc, with the car 2 s early at 0.5x and the ego at 1.4x, every repeat failed. This is the classic lead-vehicle failure: the policy took over with a short gap to the slow car it was following, braked only lightly, planned a late swerve and hit car 12's rear. The ego was also rear-ended in these runs; that does not count as the policy's failure, and the front hit came first.
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_006, car_conflicts_3knobs_2hz_hybrid_optuna_011, car_conflicts_3knobs_2hz_hybrid_optuna_012, car_conflicts_3knobs_2hz_hybrid_optuna_013)
- On 096988dd, with the car at its recorded timing at 1.5x and the ego at 1.2x, every repeat failed. The policy slowed and drifted left, against the STRAIGHT/RIGHT command and the recorded path, and clipped actor 41 passing in the left lane. That is also not the retimed car. A single run at 2x car speed with the ego at its recorded speed did not fail, which hints that the ego's speed matters here. It is one run, so this is a hint, not a result.
  - S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_003, car_conflicts_3knobs_2hz_hybrid_optuna_014, car_conflicts_3knobs_2hz_hybrid_optuna_015, car_conflicts_3knobs_2hz_hybrid_optuna_016)
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_004)
- In all three confirmed cases the ego was fast at hand-off (1.2x or 1.4x). Ego speed alone is not enough, though: many settings at 1.4x on other scenes did not fail.
  - S25: 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_035, car_conflicts_3knobs_2hz_hybrid_optuna_041, car_conflicts_3knobs_2hz_hybrid_optuna_042, car_conflicts_3knobs_2hz_hybrid_optuna_043, car_conflicts_3knobs_2hz_hybrid_optuna_044)
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_006, car_conflicts_3knobs_2hz_hybrid_optuna_011, car_conflicts_3knobs_2hz_hybrid_optuna_012, car_conflicts_3knobs_2hz_hybrid_optuna_013)
  - S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_003, car_conflicts_3knobs_2hz_hybrid_optuna_014, car_conflicts_3knobs_2hz_hybrid_optuna_015, car_conflicts_3knobs_2hz_hybrid_optuna_016)
  - S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_051, car_conflicts_3knobs_2hz_hybrid_optuna_052, car_conflicts_3knobs_2hz_hybrid_optuna_053, car_conflicts_3knobs_2hz_hybrid_optuna_055, car_conflicts_3knobs_2hz_hybrid_optuna_054_a3)
  - S5: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_037, car_conflicts_3knobs_2hz_hybrid_optuna_045, car_conflicts_3knobs_2hz_hybrid_optuna_046)
  - S9: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_050)
  - S14: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_001, car_conflicts_3knobs_2hz_hybrid_optuna_021, car_conflicts_3knobs_2hz_hybrid_optuna_022)
  - S18: 12855a41 at actor_time_shift_s 1, actor_speed_scale 2, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_002, car_conflicts_3knobs_2hz_hybrid_optuna_019, car_conflicts_3knobs_2hz_hybrid_optuna_020)
- On 19f339ba, the settings near the failing one did not fail: the car at recorded timing at 0.75x with the ego at 1.2x, and the car 0.5 s late at 2x with the ego at 0.8x. So the failure there needs a particular combination of the three knobs; it is not true of the whole scene.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_027, car_conflicts_3knobs_2hz_hybrid_optuna_031, car_conflicts_3knobs_2hz_hybrid_optuna_032)
  - S24: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_010, car_conflicts_3knobs_2hz_hybrid_optuna_023)
  - S25: 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_035, car_conflicts_3knobs_2hz_hybrid_optuna_041, car_conflicts_3knobs_2hz_hybrid_optuna_042, car_conflicts_3knobs_2hz_hybrid_optuna_043, car_conflicts_3knobs_2hz_hybrid_optuna_044)
- The settings tested most thoroughly without a failure are on 09a95ffa (car 2 s early at 1.25x, ego 1.4x) and 12855a41 (car 1.5 s late at 1.5x, ego 1.2x). Each failure range there stays below 0.5, so neither is a challenging case.
  - S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_051, car_conflicts_3knobs_2hz_hybrid_optuna_052, car_conflicts_3knobs_2hz_hybrid_optuna_053, car_conflicts_3knobs_2hz_hybrid_optuna_055, car_conflicts_3knobs_2hz_hybrid_optuna_054_a3)
  - S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_056, car_conflicts_3knobs_2hz_hybrid_optuna_057, car_conflicts_3knobs_2hz_hybrid_optuna_058, car_conflicts_3knobs_2hz_hybrid_optuna_059, car_conflicts_3knobs_2hz_hybrid_optuna_060)
- The strongest unconfirmed candidates, ranked by the study's near-miss (criticality) score, are: 096988dd with the car at 2x and the ego at recorded speed, 19f339ba with the car at 0.75x and the ego at 1.2x, and two settings on 09a95ffa. None of them failed. On 0dbb91dd both settings scored zero criticality and showed no conflict.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_004)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_027, car_conflicts_3knobs_2hz_hybrid_optuna_031, car_conflicts_3knobs_2hz_hybrid_optuna_032)
  - S5: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_037, car_conflicts_3knobs_2hz_hybrid_optuna_045, car_conflicts_3knobs_2hz_hybrid_optuna_046)
  - S6: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_009, car_conflicts_3knobs_2hz_hybrid_optuna_017, car_conflicts_3knobs_2hz_hybrid_optuna_018)
  - S11: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_007)
  - S12: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_030)

## Open

- The two missing cases. Six scenes had kept runs and never failed (09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41, 187e6244), and 1c45ce3a had none. The next runs would search near the near misses: repeat S3 and try nearby ego speeds on 096988dd (that scene already has a confirmed case, so a second one counts only if distinct scenes are relaxed), and probe 09a95ffa and 0e899dd3 around S5, S6 and S13 with the ego at 1.4x and the car slowed.
- Whether the confirmed rates are high or only just above 0.5. Each rests on four or five runs, so a few more repeats of S1, S2 and S25 would tighten their ranges.
- How wide each failure region is. On 023b7fcc only one setting was ever tried, and on 096988dd only two. Neighbouring settings (ego 1.0x to 1.2x, car speed 0.75x to 1x, timing shifted by 0.5 s to 1 s) would show whether these failures depend on the exact setting or hold across a band.
- Whether the retimed car causes the failures on 19f339ba and 096988dd. There the ego hit a different car passing on the left. Running the same ego speeds with the car at its recorded timing and speed would separate the effect of the ego's speed from that of the retiming.
- Scene 1c45ce3a produced no kept runs: every attempt there was halted or needed a re-run, so it is untested.
- The 2 Hz planning rate was assumed from the configuration (control_timestep_us 500000) but not checked in the runs.

## Why the runs failed (triage from the video and log)

turned_into_actor 8, no_brake_for_lead 4, other 1

- car_conflicts_3knobs_2hz_hybrid_optuna_003: turned_into_actor, policy at fault: yes. On a multi-lane highway, the logged human path (and, from 6.7s, the RIGHT command) bore right, but the ego slowed from 6.7 to 4.6 m/s and drifted left onto the lane line. Actor 41 was overtaking in the lane to the left, and the ego's front corner hit its side at 7.7s, about 1.6 m from where the human drove.
- car_conflicts_3knobs_2hz_hybrid_optuna_006: no_brake_for_lead, policy at fault: yes. Going straight on a busy multi-lane road, the ego closed on the slower car ahead in its lane (actor 12) at about 3.6 m/s. After the policy took over at 4.7s with only a 6.8 m gap, it slowed only from 6.0 to 4.4 m/s and planned a late swerve left, and its front hit actor 12 at 5.7s. The ego was rear-ended at some point, but the front collision is what counts as the failure.
- car_conflicts_3knobs_2hz_hybrid_optuna_011: no_brake_for_lead, policy at fault: yes. The ego was following slower lead vehicle 12 in its own lane in slow highway traffic. After handoff at 4.7s the gap was 6.8 m and closing. The policy slowed only gently (6.0 to 4.4 m/s) and began planning a swerve to the left instead of braking firmly, and its front hit the lead's rear at 5.7s. The ego was also rear-ended at some point, but the at-fault front collision came first.
- car_conflicts_3knobs_2hz_hybrid_optuna_012: no_brake_for_lead, policy at fault: yes. The ego was going straight on a busy multi-lane road behind lead car 12 in its own lane, and the gap kept closing (14 m → 4.5 m). After handoff at 4.7 s, the policy braked only lightly (6.0 → 4.4 m/s) and planned a late swerve to the left. It hit the car's rear with its front 1 s later; the rear contact came after this.
- car_conflicts_3knobs_2hz_hybrid_optuna_013: no_brake_for_lead, policy at fault: yes. Going straight on a busy multi-lane road, the ego was closing on slower lead car 12 in its own lane: the gap shrank from 14 m to 6.8 m by the 4.7 s handoff. After taking over, the policy slowed only from 6.0 to 4.4 m/s and started a late plan to swerve left, and its front hit car 12 at 5.7 s. A rear contact also happened at some point, but the front collision started first.
- car_conflicts_3knobs_2hz_hybrid_optuna_014: turned_into_actor, policy at fault: yes. On a multi-lane highway, the route command switched from STRAIGHT to RIGHT and the recorded path moved right, but the policy's planned path drifted left into the next lane. Actor 41 was passing on the left in that lane, and the ego's front corner hit it at 4.4 m/s.
- car_conflicts_3knobs_2hz_hybrid_optuna_015: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy steered the ego left out of its lane and away from the recorded path, while also slowing from 6.6 to 4.8 m/s. Vehicle 41 was coming up in the left lane, behind and to the left of the ego, and the ego's front corner hit it as the two ended up side by side at 7.2s.
- car_conflicts_3knobs_2hz_hybrid_optuna_016: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 6.7 to 4.6 m/s and steered left out of its lane, even though the route command was STRAIGHT and then RIGHT. Actor 41 was passing on the left in the next lane, and the ego's front clipped its rear quarter while the recorded human path stayed to the right.
- car_conflicts_3knobs_2hz_hybrid_optuna_035: turned_into_actor, policy at fault: yes. On an open multi-lane highway with no lead vehicle close by (gap over 43 m), the policy braked hard for no visible reason, from 23.7 to 7.4 m/s, and dropped about 9 m behind the recorded position. Meanwhile its path drifted left, and its front corner hit actor 1, which was catching up in the left lane and was by then alongside the ego.
- car_conflicts_3knobs_2hz_hybrid_optuna_041: turned_into_actor, policy at fault: yes. On a straight highway with nothing close ahead in its lane, the ego braked hard for no clear reason (23.7 to 7.2 m/s) and drifted left toward the lane line, ending about 1.3 m off the recorded path. Its front-left corner then hit actor 1, which was coming up from behind in the left lane and was alongside the ego by 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_optuna_042: turned_into_actor, policy at fault: yes. On an open highway with no close lead, the policy braked hard for no visible reason (23.7 to 7.3 m/s) and drifted left over the lane line. Actor 1 was coming up in the left lane and drew alongside, and the ego's front corner hit it. The ego had also been rear-ended at some point, likely because of the sudden braking.
- car_conflicts_3knobs_2hz_hybrid_optuna_043: other, policy at fault: yes. On a clear highway with no lead vehicle within about 44 m, the policy braked hard for no visible reason, from 23.7 to 7.4 m/s in 3 s, while drifting slightly left of the recorded path. Actor 1, which had been following close behind in the logged trajectory, caught up and pulled alongside on the left, and the ego's front-left corner struck it.
- car_conflicts_3knobs_2hz_hybrid_optuna_044: turned_into_actor, policy at fault: yes. On an open highway with nothing close ahead, the ego braked hard for no clear reason (23.7 to 7.5 m/s) and drifted about 1.5 m left of the recorded path. Actor 1 had been behind it and was passing on its left, and the ego's front-left clipped it as it went by.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_006, car_conflicts_3knobs_2hz_hybrid_optuna_011, car_conflicts_3knobs_2hz_hybrid_optuna_012, car_conflicts_3knobs_2hz_hybrid_optuna_013)
- S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_003, car_conflicts_3knobs_2hz_hybrid_optuna_014, car_conflicts_3knobs_2hz_hybrid_optuna_015, car_conflicts_3knobs_2hz_hybrid_optuna_016)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_004)
- S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_051, car_conflicts_3knobs_2hz_hybrid_optuna_052, car_conflicts_3knobs_2hz_hybrid_optuna_053, car_conflicts_3knobs_2hz_hybrid_optuna_055, car_conflicts_3knobs_2hz_hybrid_optuna_054_a3)
- S5: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_037, car_conflicts_3knobs_2hz_hybrid_optuna_045, car_conflicts_3knobs_2hz_hybrid_optuna_046)
- S6: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_009, car_conflicts_3knobs_2hz_hybrid_optuna_017, car_conflicts_3knobs_2hz_hybrid_optuna_018)
- S7: 09a95ffa at actor_time_shift_s 2, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_024)
- S8: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_040)
- S9: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_050)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_029)
- S11: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_007)
- S12: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_030)
- S13: 0e899dd3 at actor_time_shift_s -2, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_047, car_conflicts_3knobs_2hz_hybrid_optuna_048_a3)
- S14: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_001, car_conflicts_3knobs_2hz_hybrid_optuna_021, car_conflicts_3knobs_2hz_hybrid_optuna_022)
- S15: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_026, car_conflicts_3knobs_2hz_hybrid_optuna_033, car_conflicts_3knobs_2hz_hybrid_optuna_034)
- S16: 12855a41 at actor_time_shift_s -2, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_025)
- S17: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_036)
- S18: 12855a41 at actor_time_shift_s 1, actor_speed_scale 2, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_002, car_conflicts_3knobs_2hz_hybrid_optuna_019, car_conflicts_3knobs_2hz_hybrid_optuna_020)
- S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_056, car_conflicts_3knobs_2hz_hybrid_optuna_057, car_conflicts_3knobs_2hz_hybrid_optuna_058, car_conflicts_3knobs_2hz_hybrid_optuna_059, car_conflicts_3knobs_2hz_hybrid_optuna_060)
- S20: 187e6244 at actor_time_shift_s -2, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_005)
- S21: 187e6244 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_028)
- S22: 187e6244 at actor_time_shift_s 2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_038, car_conflicts_3knobs_2hz_hybrid_optuna_049)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_027, car_conflicts_3knobs_2hz_hybrid_optuna_031, car_conflicts_3knobs_2hz_hybrid_optuna_032)
- S24: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_010, car_conflicts_3knobs_2hz_hybrid_optuna_023)
- S25: 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_035, car_conflicts_3knobs_2hz_hybrid_optuna_041, car_conflicts_3knobs_2hz_hybrid_optuna_042, car_conflicts_3knobs_2hz_hybrid_optuna_043, car_conflicts_3knobs_2hz_hybrid_optuna_044)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_optuna_008: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_008_a2: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_039: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_048: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_048_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_054: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_054_a2: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

0 of 65 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
