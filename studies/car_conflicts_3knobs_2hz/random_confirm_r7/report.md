# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `random_confirm_r7`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 4 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: only one challenging case is confirmed, on scene 096988dd, where the car runs 0.5 s early at 1.5x speed and the ego starts at 1.4x speed (S5). There, every repeat ended with the policy drifting left and hitting a car driving alongside. A second scene, 19f339ba, gave two candidates (S31, S32), but each has a single failed run. That is a hint, not a confirmed rate. On the other eight scenes, no setting tried produced a failure. Every failure has the same shape: a faster ego (1.2x to 1.4x) with a sped-up car (1.25x to 1.5x) shifted by 0 to -1 s. In each one the policy steered into a neighbouring car, which was not the car the study retimed. All failures were the policy's fault, and none is flagged as a possible simulator artifact.

## Findings

- The one confirmed challenging case is on scene 096988dd at -0.5 s, 1.5x car speed and 1.4x ego speed. Every repeat failed, and its range lies above 0.5. A nearby setting on the same scene (-1.0 s, 1.25x car speed, 1.2x ego speed) also failed, but in a single run.
  - S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_009, car_conflicts_3knobs_2hz_random_confirm_r7_011, car_conflicts_3knobs_2hz_random_confirm_r7_021)
  - S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_039)
- On 096988dd the failure is the policy's own lateral error. On a multi-lane highway, with the command STRAIGHT and then RIGHT, its planned path bent left, away from the recorded path. The ego crossed the lane line and hit actor 41 alongside in the left lane. Actor 41 is not the retimed track 2.
  - S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_039)
  - S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_009, car_conflicts_3knobs_2hz_random_confirm_r7_011, car_conflicts_3knobs_2hz_random_confirm_r7_021)
- Scene 19f339ba is a strong second candidate but is not confirmed. It failed in single runs at -0.5 s / 1.5x car / 1.2x ego and at 0 s / 1.25x car / 1.2x ego. In both, the ego braked hard with a clear lane ahead, drifted left, and clipped actor 1 as that car pulled ahead. The rear contacts in those runs came from a follower and are not counted as the policy's failure.
  - S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_057)
  - S32: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_056_a3)
- On 19f339ba the ego's speed may matter. Runs with the ego at its recorded speed did not fail, including one with the car at 1.5x and 0 s shift. These were single runs, so this is only a hint.
  - S33: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_059_a2)
  - S34: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_060)
  - S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_057)
  - S32: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_056_a3)
- No failure appeared on scenes 023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41, 187e6244 or 1c45ce3a at any setting tried. Even the most repeated settings there have ranges whose upper ends do not rule out a moderate failure rate.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_048)
  - S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_027, car_conflicts_3knobs_2hz_random_confirm_r7_031, car_conflicts_3knobs_2hz_random_confirm_r7_042, car_conflicts_3knobs_2hz_random_confirm_r7_052)
  - S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_017)
  - S6: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_038)
  - S7: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_049, car_conflicts_3knobs_2hz_random_confirm_r7_053)
  - S8: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_020, car_conflicts_3knobs_2hz_random_confirm_r7_022, car_conflicts_3knobs_2hz_random_confirm_r7_034, car_conflicts_3knobs_2hz_random_confirm_r7_045)
  - S9: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_004, car_conflicts_3knobs_2hz_random_confirm_r7_015)
  - S10: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_019, car_conflicts_3knobs_2hz_random_confirm_r7_023, car_conflicts_3knobs_2hz_random_confirm_r7_033, car_conflicts_3knobs_2hz_random_confirm_r7_044, car_conflicts_3knobs_2hz_random_confirm_r7_055)
  - S11: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_006)
  - S12: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_005)
  - S13: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_002)
  - S14: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_050)
  - S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_047)
  - S16: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_028)
  - S17: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_016)
  - S18: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_003)
  - S19: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_046)
  - S20: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_058)
  - S21: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_040, car_conflicts_3knobs_2hz_random_confirm_r7_041, car_conflicts_3knobs_2hz_random_confirm_r7_051)
  - S22: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_026)
  - S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_001, car_conflicts_3knobs_2hz_random_confirm_r7_013, car_conflicts_3knobs_2hz_random_confirm_r7_024)
  - S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_018)
  - S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_030, car_conflicts_3knobs_2hz_random_confirm_r7_032, car_conflicts_3knobs_2hz_random_confirm_r7_043, car_conflicts_3knobs_2hz_random_confirm_r7_054)
  - S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_029)
  - S27: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_010_a2)
  - S28: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_008, car_conflicts_3knobs_2hz_random_confirm_r7_014)
  - S29: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_037)
  - S30: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_036)
  - S35: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_007, car_conflicts_3knobs_2hz_random_confirm_r7_012, car_conflicts_3knobs_2hz_random_confirm_r7_025, car_conflicts_3knobs_2hz_random_confirm_r7_035)
- The near misses the brief ranks next are concentrated on 023b7fcc (0.5 s, 1.0x car, 0.6x ego), 0e899dd3 (1.5 s, 0.75x car, 0.6x ego), 09a95ffa (-1.0 s, 0.75x car, 1.2x ego) and 19f339ba (1.0 s, 0.5x car, 1.0x ego). None of their runs failed.
  - S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_027, car_conflicts_3knobs_2hz_random_confirm_r7_031, car_conflicts_3knobs_2hz_random_confirm_r7_042, car_conflicts_3knobs_2hz_random_confirm_r7_052)
  - S21: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_040, car_conflicts_3knobs_2hz_random_confirm_r7_041, car_conflicts_3knobs_2hz_random_confirm_r7_051)
  - S7: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_049, car_conflicts_3knobs_2hz_random_confirm_r7_053)
  - S34: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_060)
- Scene 0dbb91dd scored zero criticality at every setting. Either nothing came close there, or the near-miss measure did not register on this scene.
  - S11: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_006)
  - S12: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_005)
  - S13: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_002)
  - S14: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_050)
  - S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_047)
  - S16: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_028)
  - S17: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_016)
  - S18: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_003)

## Open

- Confirm or reject the two 19f339ba candidates by repeating S31 and S32 about four more times each. If either holds up, it would be the second confirmed scene.
- Find out whether retiming the key car matters at all. Every collision was with a neighbouring car, not the retimed one. Re-run 096988dd and 19f339ba at the recorded car timing (0 s, 1.0x) with the ego at 1.2x to 1.4x. If those runs fail, the ego's speed at hand-off is the real driver.
- Find out whether ego speed is needed on 096988dd. Re-run the S5 car setting with the ego at 1.0x.
- Three more confirmed scenes are needed, and the eight scenes with no failures have barely been searched: most settings ran once in a large three-knob grid. Search them with fast-ego and fast-car combinations around the settings with the highest criticality (S2, S21, S7, S25), then repeat any setting that fails.
- Check why criticality is zero everywhere on 0dbb91dd, which came within 0.23 m of another actor as recorded.
- Four runs were not kept and had to be re-run. Their settings are covered by S27, S32 and S33, but the reason the gate rejected them is not recorded here.

## Why the runs failed (triage from the video and log)

turned_into_actor 6

- car_conflicts_3knobs_2hz_random_confirm_r7_009: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy's planned path drifted left toward the lane with actors 35 and 41, while the recorded human path went straight and slightly right and the route command changed to RIGHT. The ego crossed into the left lane while slowing and its front hit vehicle 41, which was alongside on the left.
- car_conflicts_3knobs_2hz_random_confirm_r7_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (RIGHT in the last frame), the ego drifted left out of its lane, away from the recorded path, which stayed straight to slightly right. It moved over the lane line and hit the side of actor 41, which was alongside in the left lane.
- car_conflicts_3knobs_2hz_random_confirm_r7_021: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT and then RIGHT, the policy's planned path bent left toward the next lane while the recorded path stayed in lane. The ego slid about 1.5 m left of the recorded path and side-swiped vehicle 41, which was driving alongside in the left lane.
- car_conflicts_3knobs_2hz_random_confirm_r7_039: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (RIGHT by the last frame), the policy's planned path bent left, away from the recorded path. The ego drifted left into the next lane and its front-left hit actor 41, which was driving alongside in that lane.
- car_conflicts_3knobs_2hz_random_confirm_r7_057: turned_into_actor, policy at fault: yes. On an open highway with nothing ahead, the ego braked hard for no reason (20.3 to 8.5 m/s) while the recorded human drove on, and its planned path veered left into the next lane. Actor 1 had been beside it on the left and pulled ahead as the ego slowed, and the ego's front corner hit it as the ego drifted left. The later rear contact was most likely a follower hitting the ego after the needless braking.
- car_conflicts_3knobs_2hz_random_confirm_r7_056_a3: turned_into_actor, policy at fault: yes. With a clear lane ahead (about 40–50 m gap), the ego braked hard for no visible reason, slowing from 20 to 7.6 m/s, while the recorded human car kept going. Its planned path then drifted left toward the next lane. Actor 1, which had been beside it in that left lane, moved ahead as the ego slowed, and the ego's front clipped it. Separately, a vehicle behind rear-ended the braking ego at some point.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_048)
- S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_027, car_conflicts_3knobs_2hz_random_confirm_r7_031, car_conflicts_3knobs_2hz_random_confirm_r7_042, car_conflicts_3knobs_2hz_random_confirm_r7_052)
- S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_017)
- S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_039)
- S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_009, car_conflicts_3knobs_2hz_random_confirm_r7_011, car_conflicts_3knobs_2hz_random_confirm_r7_021)
- S6: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_038)
- S7: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_049, car_conflicts_3knobs_2hz_random_confirm_r7_053)
- S8: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_020, car_conflicts_3knobs_2hz_random_confirm_r7_022, car_conflicts_3knobs_2hz_random_confirm_r7_034, car_conflicts_3knobs_2hz_random_confirm_r7_045)
- S9: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_004, car_conflicts_3knobs_2hz_random_confirm_r7_015)
- S10: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_019, car_conflicts_3knobs_2hz_random_confirm_r7_023, car_conflicts_3knobs_2hz_random_confirm_r7_033, car_conflicts_3knobs_2hz_random_confirm_r7_044, car_conflicts_3knobs_2hz_random_confirm_r7_055)
- S11: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_006)
- S12: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_005)
- S13: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_002)
- S14: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_050)
- S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_047)
- S16: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_028)
- S17: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_016)
- S18: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_003)
- S19: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_046)
- S20: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_058)
- S21: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_040, car_conflicts_3knobs_2hz_random_confirm_r7_041, car_conflicts_3knobs_2hz_random_confirm_r7_051)
- S22: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_026)
- S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_001, car_conflicts_3knobs_2hz_random_confirm_r7_013, car_conflicts_3knobs_2hz_random_confirm_r7_024)
- S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_018)
- S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_030, car_conflicts_3knobs_2hz_random_confirm_r7_032, car_conflicts_3knobs_2hz_random_confirm_r7_043, car_conflicts_3knobs_2hz_random_confirm_r7_054)
- S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_029)
- S27: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_010_a2)
- S28: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_008, car_conflicts_3knobs_2hz_random_confirm_r7_014)
- S29: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_037)
- S30: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_036)
- S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_057)
- S32: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_056_a3)
- S33: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_059_a2)
- S34: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_060)
- S35: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r7_007, car_conflicts_3knobs_2hz_random_confirm_r7_012, car_conflicts_3knobs_2hz_random_confirm_r7_025, car_conflicts_3knobs_2hz_random_confirm_r7_035)

## Not kept by the gate

- car_conflicts_3knobs_2hz_random_confirm_r7_010: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r7_056: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r7_059: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r7_056_a2: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

0 of 64 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
