# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `optuna_confirm_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 1 of the 5 cases it was looking for, so the goal was not met. The confirmed case is scene 023b7fcc with the cars shifted 1.5 s earlier at 1.25x speed (S2): every run there failed, and its range sits above one half. Two of those failures are flagged as possible simulator artifacts. Triage still puts every failure at S2 on the policy: the camera view was smeared, but the car ahead stayed visible. On that scene, every setting with the cars earlier (−1.5 s to −0.5 s) at normal or higher speed failed, and every setting with the cars on time or later at changed speed passed. Most of those settings ran only once, so the pattern is a hint, not a rate. The only failure on a second scene is a single run on 09a95ffa (−1.5 s, 1.0x). No other scene failed in the runs it got.

## Findings

- Confirmed challenging case: scene 023b7fcc with the cars 1.5 s earlier at 1.25x speed. Every run failed and the failure rate is surely above one half. Two failures are flagged as possible artifacts, but triage puts all of them on the policy. The ego drifted left out of the recorded path against a RIGHT route command, brushed cars beside it, then drove into the back of the slower actor 56 without braking or turned into it.
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 2 possibly the simulator's (cut_in_merge_optuna_confirm_r3_002, cut_in_merge_optuna_confirm_r3_010, cut_in_merge_optuna_confirm_r3_019, cut_in_merge_optuna_confirm_r3_025, cut_in_merge_optuna_confirm_r3_050)
- On scene 023b7fcc, every other setting with the cars earlier also failed: −1.5 s at 1.0x and 2.0x, −1.0 s at 2.0x, and −0.5 s at 1.5x. Each has only one or two runs, so each is a hint. The failures were the same leftward lane departure into actors 56 or 61, or no braking for the slowing lead car 66.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_optuna_confirm_r3_024, cut_in_merge_optuna_confirm_r3_041)
  - S3: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_051)
  - S4: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_032)
  - S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_043)
- Not every failure on 023b7fcc clearly belongs to the policy. At −1.0 s and 2.0x, the lead car's recorded box already overlapped the ego before handoff, with the ego on the recorded path, so fault is unclear. At −0.5 s and 1.5x, actor 13 jumped onto the ego's front at handoff, which looks like a simulator artifact. The ego still then steered left into actor 61.
  - S4: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_032)
  - S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_043)
- On scene 023b7fcc, single runs with the cars on time or later (0 s to +2 s, at 0.5x to 1.25x) all passed, though some came close. Earlier timing looks like what makes the scene fail, but one run per setting does not show these settings are safe.
  - S6: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_044)
  - S7: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_015)
  - S8: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_006)
  - S9: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_009)
  - S10: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_033)
- Scene 09a95ffa failed once, with the cars 1.5 s earlier at 1.0x speed. The policy bent left toward the next lane while vehicle 33 was passing and hit its side, against a RIGHT command. This is a single run, a candidate rather than a confirmed case.
  - S17: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_054)
- Several repeated settings look unlikely to fail often: 096988dd (+0.5 s, 0.5x), 09a95ffa (−0.5 s, 0.5x), 19f339ba (+0.5 s, 1.5x) and 12855a41 (−1.5 s, 1.25x). Each passed every run, with an upper bound below one half.
  - S16: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_optuna_confirm_r3_005, cut_in_merge_optuna_confirm_r3_011, cut_in_merge_optuna_confirm_r3_020, cut_in_merge_optuna_confirm_r3_029, cut_in_merge_optuna_confirm_r3_038, cut_in_merge_optuna_confirm_r3_046)
  - S18: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_optuna_confirm_r3_014, cut_in_merge_optuna_confirm_r3_021, cut_in_merge_optuna_confirm_r3_028, cut_in_merge_optuna_confirm_r3_039, cut_in_merge_optuna_confirm_r3_048)
  - S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_optuna_confirm_r3_016, cut_in_merge_optuna_confirm_r3_022, cut_in_merge_optuna_confirm_r3_030, cut_in_merge_optuna_confirm_r3_040)
  - S24: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r3_036, cut_in_merge_optuna_confirm_r3_037, cut_in_merge_optuna_confirm_r3_049)
- Scenes 054b5901, 0cf6368d, 0e899dd3, 1c45ce3a and 12855a41 had no failures. Their settings ran only once or twice each, so a failing timing there is not ruled out.
  - S11: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_018)
  - S12: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_017)
  - S13: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_052)
  - S14: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_008)
  - S15: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_001)
  - S20: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_004)
  - S21: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_034)
  - S22: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_045, cut_in_merge_optuna_confirm_r3_047)
  - S23: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_023, cut_in_merge_optuna_confirm_r3_031)
  - S25: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_042)
  - S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_003, cut_in_merge_optuna_confirm_r3_013)
  - S27: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_027)
  - S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_035)
  - S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_007, cut_in_merge_optuna_confirm_r3_012)
  - S31: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_053_a2)
- The failures that were found did not come from another car cutting into the ego's lane. They came from the policy leaving its own lane to the left, often against the route command, or failing to brake for a slower car ahead.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_optuna_confirm_r3_024, cut_in_merge_optuna_confirm_r3_041)
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 2 possibly the simulator's (cut_in_merge_optuna_confirm_r3_002, cut_in_merge_optuna_confirm_r3_010, cut_in_merge_optuna_confirm_r3_019, cut_in_merge_optuna_confirm_r3_025, cut_in_merge_optuna_confirm_r3_050)
  - S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_043)
  - S17: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_054)

## Open

- Four of the five cases are still missing. The best next candidate is 09a95ffa at −1.5 s and 1.0x (S17). About 3 to 4 more runs would show whether its failure rate is surely above one half.
- Earlier cars (−1.5 s) at 1.0x were tried only on 023b7fcc and 09a95ffa. Running that timing, and −2 s, on 096988dd, 19f339ba, 054b5901 and 0cf6368d would show whether earlier traffic also breaks those scenes. Several of the repeats on those scenes went to slow 0.5x settings, which look safe.
- Scene 023b7fcc was never run in replay with the recorded timing (0 s, 1.0x). So it is unknown whether the retiming causes the leftward drift or the scene fails anyway. One or two runs at that setting would settle it.
- On 023b7fcc, the runs at −1.0 s with 2.0x and −0.5 s with 1.5x may be simulator artifacts: a lead car's box was placed wrong, and actor 13 jumped onto the ego at handoff. Repeats would show whether the policy fails there on its own.
- Near misses were not checked as a ranking, so the study cannot rank challenging settings beyond the failures found.
- On 023b7fcc and 09a95ffa every car was retimed, not one marked cut-in car. The study cannot say which car's timing matters.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 6, turned_into_actor 5

- cut_in_merge_optuna_confirm_r3_002: no_brake_for_lead, policy at fault: yes. After taking over, the ego drifted about 3 m left of the recorded path into the lane behind actor 56. It held about 5.8 m/s while the gap to that slower car shrank from 11.9 m to 4.9 m, and it hit the car's rear at 9.4 s. Earlier there was side and rear contact with actor 13 on its right, and the camera view of the lead car was smeared, but the car stayed visible ahead and the ego never slowed for it.
- cut_in_merge_optuna_confirm_r3_010: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego drifted left out of its lane on a busy multi-lane freeway, moving away from the recorded path. It sideswiped actor 61 (lateral contact at about 7.6s), was then hit from behind (about 8.6s), and finally drove into the back of slower actor 56 in the new lane at about 5 m/s, barely braking as the gap shrank from 11.8 m to 4.6 m.
- cut_in_merge_optuna_confirm_r3_019: no_brake_for_lead, policy at fault: yes. With a RIGHT command, the ego drifted left out of the recorded path (about 3.6 m off it) into the next lane, brushing vehicles 13 and 61 on the way. It then held about 5.6 m/s and ran into the back of vehicle 56 ahead in that lane while the gap closed from 15.6 m to 4.5 m, without braking. The camera view was heavily smeared near the other cars, but vehicle 56 was still visible ahead the whole time.
- cut_in_merge_optuna_confirm_r3_024: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego sped up from 4.2 to 5.8 m/s while edging left toward the adjacent lane, roughly along the recorded human lane change. It ran its front into actor 56, which was alongside and slightly ahead in that left lane. The lead vehicle in its own lane was always more than 20 m ahead, so this was not a lead-vehicle collision. The rear contact came after this front collision.
- cut_in_merge_optuna_confirm_r3_025: no_brake_for_lead, policy at fault: yes. The ego was about 4 m left of the recorded path, despite a RIGHT command. It closed on actor 56, a slower car ahead in its lane, as the gap shrank from 17 m to 4 m, and hit 56's rear while barely slowing (5.4 to 5.0 m/s). Actor 61 had touched the ego's rear earlier (7.7–8.7s), and the camera is heavily smeared because the ego is far from the recorded path, but the lead car was visible and the ego had plenty of distance to brake.
- cut_in_merge_optuna_confirm_r3_032: no_brake_for_lead, policy at fault: unclear. The policy took over at 4.7s in slow, dense straight traffic. It sped up slightly (4.2 to 4.4 m/s) while lead vehicle 66 in its lane slowed, and its front clipped 66's rear at 5.6s. But the ego was only 0.1 m off the human's recorded path. It was also already overlapping 66 at 3.6s, before handoff, with a front collision flagged in that frame, so the lead's recorded box is probably placed wrong and the policy's share of the blame is unclear.
- cut_in_merge_optuna_confirm_r3_041: turned_into_actor, policy at fault: yes. After the policy took over, it planned a lane change to the left even though the route command was STRAIGHT and then RIGHT, and the recorded path stayed in the lane. The ego angled left and its front ran into actor 56, which was alongside it in the left lane. The lead vehicle was more than 20 m ahead, so this was not a following problem, and the rear contact came only after this collision.
- cut_in_merge_optuna_confirm_r3_043: turned_into_actor, policy at fault: yes. At handoff (4.8s), actor 13 was already overlapping the ego's front, which looks like a sim artifact or a cut-in: the gap went from 28.5 m to 1.0 m in half a second. The policy then sped up and steered left out of its lane, against the RIGHT/STRAIGHT command, and hit actor 61 in the left lane at 6.8s.
- cut_in_merge_optuna_confirm_r3_050: no_brake_for_lead, policy at fault: yes. The route went right, but the ego stayed in the lane to the left of the recorded path at about 6 m/s and drove into the rear of the slower actor 56 ahead in that lane. The gap closed from 11.8 m to 4.7 m with no braking. Before that, there was lateral contact at 7.4 s, and at 8.4 s actor 13 touched the ego's rear as it went past on the right. The camera view of the cars ahead was heavily smeared but still showed a vehicle there.
- cut_in_merge_optuna_confirm_r3_051: no_brake_for_lead, policy at fault: yes. The ego was going straight in slow freeway traffic. After handoff at 4.7 s it sped up from 4.2 to 4.6 m/s while lead vehicle 66 in its lane slowed, so the gap fell from 8.6 m to contact. Its plan started a leftward swerve toward the gap by vehicle 61 instead of braking, and its front hit 66 at 5.6 s. The rear-end contact came later.
- cut_in_merge_optuna_confirm_r3_054: turned_into_actor, policy at fault: yes. On the multi-lane freeway at about 8 m/s, the policy took over at 4.6 s. Its planned path then bent left toward the adjacent lane while vehicle 33 was passing on the left. By 6.0 s the ego had drifted about 0.8 m off the recorded path, and its front-left corner was overlapping 33's side, even though the route command had changed to RIGHT.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_optuna_confirm_r3_024, cut_in_merge_optuna_confirm_r3_041)
- S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 2 possibly the simulator's (cut_in_merge_optuna_confirm_r3_002, cut_in_merge_optuna_confirm_r3_010, cut_in_merge_optuna_confirm_r3_019, cut_in_merge_optuna_confirm_r3_025, cut_in_merge_optuna_confirm_r3_050)
- S3: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_051)
- S4: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_032)
- S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_043)
- S6: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_044)
- S7: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_015)
- S8: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_006)
- S9: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_009)
- S10: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_033)
- S11: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_018)
- S12: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_017)
- S13: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_052)
- S14: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_008)
- S15: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_001)
- S16: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_optuna_confirm_r3_005, cut_in_merge_optuna_confirm_r3_011, cut_in_merge_optuna_confirm_r3_020, cut_in_merge_optuna_confirm_r3_029, cut_in_merge_optuna_confirm_r3_038, cut_in_merge_optuna_confirm_r3_046)
- S17: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r3_054)
- S18: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_optuna_confirm_r3_014, cut_in_merge_optuna_confirm_r3_021, cut_in_merge_optuna_confirm_r3_028, cut_in_merge_optuna_confirm_r3_039, cut_in_merge_optuna_confirm_r3_048)
- S19: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_026)
- S20: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_004)
- S21: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_034)
- S22: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_045, cut_in_merge_optuna_confirm_r3_047)
- S23: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_023, cut_in_merge_optuna_confirm_r3_031)
- S24: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r3_036, cut_in_merge_optuna_confirm_r3_037, cut_in_merge_optuna_confirm_r3_049)
- S25: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_042)
- S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_003, cut_in_merge_optuna_confirm_r3_013)
- S27: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_027)
- S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_optuna_confirm_r3_016, cut_in_merge_optuna_confirm_r3_022, cut_in_merge_optuna_confirm_r3_030, cut_in_merge_optuna_confirm_r3_040)
- S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_035)
- S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r3_007, cut_in_merge_optuna_confirm_r3_012)
- S31: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r3_053_a2)

## Not kept by the gate

- cut_in_merge_optuna_confirm_r3_053: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scope and settings follow the brief. Traffic is replayed as recorded. Only recorded cars (class automobile) are retimed, using the knobs' full ranges: -2 s to +2 s and 0.5x to 2x speed.

Scene choice: 31 scenes carry the merge_cut_in tag. I kept 9 that passed at 0 delay and have a car identified as a key actor. Scenes that already fail with the recorded timing would fill the top 5 without showing what the retiming does, so I left them out. Three scenes have a car marked as cutting in (0cf6368d track 21, 12855a41 track 31, 1c45ce3a track 14). In those, only that car is retimed. The other six retime every car in the scene: with only a lead or crossing car identified, retiming that car alone could miss the car that actually changes lanes. Several picks already came close at baseline (023b7fcc and 096988dd at 0.0 m, 19f339ba at 0.03 m, 12855a41 at 0.08 m, 054b5901 at 0.26 m), so they are good places to look first.

Budget and stopping rule: 6 rounds of 9 runs gives 54 runs, close to the brief's ~50 and under the cap of 60. The goal is top_k with k=5, one case per scene, failure rate surely above 0.5. A setting needs about 4 failures in 4 runs to clear that bar, so confirming 5 cases costs about 20 to 25 runs. That leaves roughly 30 runs to search, and the study stops early once 5 cases are confirmed.

What this plan cannot do:
- If fewer than 5 scenes break reliably within the budget, the study will report fewer than 5 confirmed cases.
- Near misses can guide the search, but the stopping rule only counts failures, so they are not a checked ranking.
- The tags do not say whether the ego merges or another car cuts in, so the two cases cannot be told apart.
- The 0-delay results were recorded with learned (CATK) traffic, not replay, so the pass/fail used to pick scenes is only a guide.
- Retiming a whole class moves every car in the scene, not only the one changing lanes.
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
