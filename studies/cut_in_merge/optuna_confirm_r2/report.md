# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `optuna_confirm_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed five settings on five different scenes where the policy fails in most runs. Four of them move the other cars earlier: 09a95ffa at -2 s and 1.5x (S10), 023b7fcc at -2 s and 2x (S1), 0e899dd3 at -1.5 s and 2x (S19) and 054b5901 at -1.5 s and 0.75x (S3). The fifth is 19f339ba at +0.5 s and the recorded speed (S26). Every kept run at these five settings failed. The 90% ranges for most of them only just clear one half, though, so they are confirmed as likely failures but not ranked against each other. All the failures at S10 and S3 are flagged as possible simulator artifacts, because the ego was over 3.5 m from the recorded path. Triage still blames the policy in each case: it drifted left against a RIGHT route command, then either ran into a slower car ahead or drove onto a median. In all five scenes every car was retimed, not one marked cut-in car, so the study can't say which car's timing causes the failure.

## Findings

- On scene 09a95ffa, moving the cars 2 s earlier at 1.5x speed made every run fail. Each time the ego drifted a lane left of the recorded path, against a RIGHT command, and hit the slower car 87 ahead of it without braking enough. All of these failures are flagged as possible rendering artifacts because the ego was far off the path, but triage judged the policy at fault in each one.
  - S10: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (cut_in_merge_optuna_confirm_r2_004, cut_in_merge_optuna_confirm_r2_010, cut_in_merge_optuna_confirm_r2_020, cut_in_merge_optuna_confirm_r2_023)
- On scene 023b7fcc, moving the cars 2 s earlier at 2x speed made every run fail the same way: the ego kept its speed and ran into lead car 66, which had nearly stopped. In one of those runs it is unclear whether the policy was at fault, because the replayed car 66 may not have moved as it did in the real drive. On the same scene, +0.5 s at the recorded speed did not fail in its runs.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_027, cut_in_merge_optuna_confirm_r2_028, cut_in_merge_optuna_confirm_r2_037)
  - S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_017, cut_in_merge_optuna_confirm_r2_022)
- On scene 054b5901, moving the cars 1.5 s earlier at 0.75x speed made every run leave the road. The ego stayed in a left lane, against a RIGHT command, and drove onto the nose of the median island. No other car was involved. All of these failures are flagged as possible artifacts, though one triage notes a clean camera view. The other settings tried on this scene did not fail in their single or paired runs.
  - S3: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_optuna_confirm_r2_015, cut_in_merge_optuna_confirm_r2_021, cut_in_merge_optuna_confirm_r2_030)
  - S4: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_005)
  - S5: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_035)
  - S6: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_002, cut_in_merge_optuna_confirm_r2_011)
  - S7: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_008)
- On scene 0e899dd3, moving the cars 1.5 s earlier at 2x speed made every run fail. In slow freeway traffic the ego's plan wobbled left and its front-left corner clipped car 23 in the next lane. The other settings tried on this scene, including the recorded timing, did not fail in their single runs.
  - S19: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_034, cut_in_merge_optuna_confirm_r2_038, cut_in_merge_optuna_confirm_r2_046)
  - S18: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_024)
  - S20: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_052)
  - S21: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_033)
- On scene 19f339ba, +0.5 s at the recorded speed made every run fail. The ego braked hard on a clear highway for no visible reason, drifted left and sideswiped car 1 in the next lane. The rear-end hits on the ego that followed are out of scope. Settings close to this one (-0.5 s, 0 s at 1.25x, +1 s) did not fail in their single runs, so the failure may depend closely on timing, but one run at each neighbour cannot show that.
  - S26: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_018, cut_in_merge_optuna_confirm_r2_019, cut_in_merge_optuna_confirm_r2_029)
  - S24: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_050)
  - S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_051)
  - S27: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_054)
- The one failure on scene 09a95ffa at -1.5 s and 0.5x was not the policy's fault: the collision with the lead car was already unavoidable when the policy took over.
  - S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r2_042)
- Scene 12855a41 at -2 s and 0.5x is the setting most clearly shown to be low-risk: its 90% range stays below one half. Scene 096988dd at +1 s and 0.75x and scene 1c45ce3a at -1.5 s and 1.5x also did not fail, with ranges below one half. No setting on 12855a41, 096988dd, 1c45ce3a or 0cf6368d failed.
  - S22: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_optuna_confirm_r2_025, cut_in_merge_optuna_confirm_r2_031, cut_in_merge_optuna_confirm_r2_040, cut_in_merge_optuna_confirm_r2_047)
  - S9: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r2_003, cut_in_merge_optuna_confirm_r2_012, cut_in_merge_optuna_confirm_r2_049)
  - S31: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r2_032_a2, cut_in_merge_optuna_confirm_r2_039, cut_in_merge_optuna_confirm_r2_048)
  - S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_009, cut_in_merge_optuna_confirm_r2_013)
  - S8: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_041)
  - S30: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_053)
  - S32: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_001_a2, cut_in_merge_optuna_confirm_r2_016)
  - S16: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_026)
  - S17: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_036)

## Open

- The five cases are confirmed but not ranked: most ranges barely clear one half and overlap. More repeats at S1, S3, S19 and S26 (and S10) would be needed to order them.
- For S10 and S3, all failures are flagged as possible artifacts because the ego was more than 3.5 m off the recorded path. Separating a real policy drift from a rendering effect would need runs that check rendering quality away from the recorded path, or a scene where the drift happens closer to it.
- The study can't say whether retiming caused these failures. The recorded timing (0 s, 1.0x) under replay traffic was run only on 0e899dd3 (S20, one run). Running the recorded timing a few times on 023b7fcc, 054b5901, 09a95ffa and 19f339ba would show whether those scenes fail anyway.
- S26's neighbours each had only one run. Repeats at 0 s and +1 s at 1.0x on 19f339ba would show whether the failure depends closely on timing.
- In all five confirmed scenes every car was retimed, so the study can't name the car whose timing matters, or tell cut-in from merge. Retiming only the lane-changing car, once it is identified, would settle this.
- Scenes 0cf6368d, 12855a41, 1c45ce3a and 096988dd had no failures, but most of their settings had one or two runs. They are not shown to be safe across the ranges of the two knobs.
- Near misses guided the search but were not ranked, so the brief's 'near misses rank next' is not answered.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 7, turned_into_actor 6, left_road 3, other 1

- cut_in_merge_optuna_confirm_r2_004: no_brake_for_lead, policy at fault: yes. The ego ended up about 5 m left of the recorded path, even though the command was RIGHT, and kept driving in that lane behind the slower vehicle 87. It only eased from 5.6 to 3.8 m/s while the gap shrank from 11.4 m to 4.6 m, and its front hit 87. The lead car looked smeared in the camera because the ego was far from where the real car drove, but it was still visible and clearly ahead in the lane.
- cut_in_merge_optuna_confirm_r2_010: no_brake_for_lead, policy at fault: yes. After handoff, the ego drifted about 4.6 m left of its recorded path, which went right (command RIGHT), and ended up in the lane behind slow actor 87. It eased off only from 5.6 to 4.2 m/s while the gap shrank from 11.9 to 4.7 m, and its front hit 87's rear. The lead car was smeared in the camera view but still clearly visible.
- cut_in_merge_optuna_confirm_r2_015: left_road, policy at fault: yes. The route command was RIGHT and the recorded path went into the right-hand lanes, but after handoff the ego stayed about 7–8 m left of it in a left lane. Its plan kept drifting further left, and at 10.6 s it ran onto the edge of the median island at about 5.8 m/s. No actor was hit; the nearest car ahead was still 27 m away. The left side of the camera view smears because the ego is so far from where the real car drove.
- cut_in_merge_optuna_confirm_r2_018: turned_into_actor, policy at fault: yes. After the policy took over at 4.6 s, the ego braked hard on a clear highway (16.8 to 8.1 m/s) while the gap to the lead car (18) was growing, and its planned path veered left toward the adjacent lane. Because it slowed down, the ego fell back alongside actor 1 in the left lane, and its leftward drift caused a side collision with that car at 6.5 s; the ego was also rear-ended because of the sudden braking.
- cut_in_merge_optuna_confirm_r2_019: turned_into_actor, policy at fault: yes. After handoff the ego braked hard for no clear reason (17→8 m/s with the lead pulling away), falling about 10 m behind the recorded position. At the same time its plan drifted left, and it sideswiped actor 1, which was driving in the left lane and had come alongside because the ego slowed.
- cut_in_merge_optuna_confirm_r2_020: no_brake_for_lead, policy at fault: yes. The ego drifted about 5 m left of the recorded path (a RIGHT command, while the logged car was one lane to the right) and stayed in that lane behind slower actor 87. The gap to 87 shrank from 11.5 m to 4.4 m while the ego only slowed from 5.5 to 4.0 m/s, and its front hit 87. Actor 87 was smeared in the camera view but still clearly visible, so the policy should have braked.
- cut_in_merge_optuna_confirm_r2_021: left_road, policy at fault: yes. Approaching a signalized intersection with a RIGHT command, the ego stayed in the leftmost lane next to the raised median, about 7–8 m left of where the human drove (several lanes to the right). Its planned path then bent further left, and at 10.0 s it clipped the nose of the median island at about 6 m/s while slowing.
- cut_in_merge_optuna_confirm_r2_023: no_brake_for_lead, policy at fault: yes. The ego drove about 5 m to the left of the recorded path, in the lane of slower vehicle 87, and closed on it from 8.8 m to 4.4 m. It only slowed gently (5.0 to 3.8 m/s), its planned path ran straight into 87, and it hit 87's rear with its front at 11.0 s.
- cut_in_merge_optuna_confirm_r2_027: no_brake_for_lead, policy at fault: yes. Driving straight in its lane, the ego held about 4.2 m/s while the lead vehicle (actor 66) slowed to near a stop, and the gap closed from about 10.7 m to contact. After the policy took over at 4.7 s with about 8.6 m of gap, it barely slowed (4.2 to 4.1 m/s) and hit actor 66's rear with its front.
- cut_in_merge_optuna_confirm_r2_028: no_brake_for_lead, policy at fault: yes. The ego was going straight on a multi-lane arterial at about 4.2 m/s. The lead car in its lane (actor 66) slowed to nearly a stop, and the gap fell from 10.7 m to 4.3 m over about 1.5 s. After taking over at 4.7 s, the policy kept the same speed and planned a move into the left lane instead of braking, and its front ran into actor 66 at 5.6 s.
- cut_in_merge_optuna_confirm_r2_029: turned_into_actor, policy at fault: yes. After handoff on the highway, the ego braked hard for no clear reason, from 16.8 to 8.1 m/s, even though the gap to lead vehicle 18 was growing. At the same time it drifted left off the recorded path, which went slightly right, and sideswiped vehicle 1 as that car came alongside in the left lane. The hard braking also likely caused the separate rear contact.
- cut_in_merge_optuna_confirm_r2_030: left_road, policy at fault: yes. With a RIGHT command, the ego stayed in a left through lane about 4–8 m left of the recorded path, which went toward the right-side lanes. Its plan then bent further left, and while slowing (8→6 m/s) it ran onto the nose of the median island before the intersection at 10.0 s. The camera view was clean, and lead car 9 was 34 m or more ahead, so nothing outside the policy forced this.
- cut_in_merge_optuna_confirm_r2_034: turned_into_actor, policy at fault: yes. In slow freeway traffic (about 1–2 m/s), the ego's planned path (orange) swung left toward the adjacent left lane, even though the route command was RIGHT. The ego edged left and its front-left corner clipped actor 23, which was travelling alongside in that lane, at 9.6 s. The nearest car ahead in the ego's lane was about 21 m away, so this was not a rear-end of a lead vehicle.
- cut_in_merge_optuna_confirm_r2_037: no_brake_for_lead, policy at fault: unclear. Driving straight at about 4.2 m/s, the ego closed on actor 66, which had stopped in its lane: the gap fell from 10.7 m to 4.3 m between 4.1 s and 5.6 s. The policy took over at 4.7 s, kept its speed without braking (its plan swerved left toward actor 61 instead) and hit 66 with its front 0.9 s later. The ego was only 0.2 m off the recorded human path, so the replayed actor 66 probably didn't move as it did in the real drive, and the ego was also rear-ended at some point.
- cut_in_merge_optuna_confirm_r2_038: turned_into_actor, policy at fault: yes. The ego was slowing in slow highway traffic (3.4 to 1.1 m/s) and its planned path kept wobbling to the left. It edged over the left lane line, about 1.4 m off the recorded path, and its front-left corner hit vehicle 23, which was alongside in the adjacent left lane. The lead car was still about 20 m ahead, so this was not a following-distance collision.
- cut_in_merge_optuna_confirm_r2_042: other, policy at fault: no. The ego was replaying the logged trajectory at about 8 m/s and closing on lead vehicle 1 in the same lane, which was slower. The policy took over at 4.6 s, when the boxes were nearly touching, and the front collision was logged 0.2 s later even though the ego had started braking (7.9 to 7.4 m/s). The collision was already unavoidable at handoff, and the lead actor in the sim had probably drifted from where it was in the recorded drive.
- cut_in_merge_optuna_confirm_r2_046: turned_into_actor, policy at fault: yes. The ego was slowing in heavy freeway traffic (4.1 to 1.5 m/s) when its planned path wiggled left, toward actor 23 in the next lane to the left. By 9.4 s the ego had drifted about 1.4 m off the recorded human path and its front-left corner hit that car while the lane ahead was clear (lead vehicle 10 was about 21 m away). The left-side camera view of 23 was smeared but still readable as a car, and the rear-end contact came later.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_027, cut_in_merge_optuna_confirm_r2_028, cut_in_merge_optuna_confirm_r2_037)
- S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_017, cut_in_merge_optuna_confirm_r2_022)
- S3: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_optuna_confirm_r2_015, cut_in_merge_optuna_confirm_r2_021, cut_in_merge_optuna_confirm_r2_030)
- S4: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_005)
- S5: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_035)
- S6: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_002, cut_in_merge_optuna_confirm_r2_011)
- S7: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_008)
- S8: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_041)
- S9: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r2_003, cut_in_merge_optuna_confirm_r2_012, cut_in_merge_optuna_confirm_r2_049)
- S10: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (cut_in_merge_optuna_confirm_r2_004, cut_in_merge_optuna_confirm_r2_010, cut_in_merge_optuna_confirm_r2_020, cut_in_merge_optuna_confirm_r2_023)
- S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_optuna_confirm_r2_042)
- S12: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_014)
- S13: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_007)
- S14: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_006)
- S15: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_043)
- S16: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_026)
- S17: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_036)
- S18: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_024)
- S19: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_034, cut_in_merge_optuna_confirm_r2_038, cut_in_merge_optuna_confirm_r2_046)
- S20: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_052)
- S21: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_033)
- S22: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_optuna_confirm_r2_025, cut_in_merge_optuna_confirm_r2_031, cut_in_merge_optuna_confirm_r2_040, cut_in_merge_optuna_confirm_r2_047)
- S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_009, cut_in_merge_optuna_confirm_r2_013)
- S24: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_050)
- S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_051)
- S26: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_optuna_confirm_r2_018, cut_in_merge_optuna_confirm_r2_019, cut_in_merge_optuna_confirm_r2_029)
- S27: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_054)
- S28: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_044)
- S29: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_045)
- S30: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_optuna_confirm_r2_053)
- S31: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_optuna_confirm_r2_032_a2, cut_in_merge_optuna_confirm_r2_039, cut_in_merge_optuna_confirm_r2_048)
- S32: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_optuna_confirm_r2_001_a2, cut_in_merge_optuna_confirm_r2_016)

## Not kept by the gate

- cut_in_merge_optuna_confirm_r2_001: not kept: RE-RUN
- cut_in_merge_optuna_confirm_r2_032: not kept: RE-RUN

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 28 s; every count above is computed from the queue, not written by the model.

56 of 56 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
