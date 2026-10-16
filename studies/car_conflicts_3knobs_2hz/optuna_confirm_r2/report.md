# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r2`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 7 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

Only one combination is confirmed as challenging, so the goal of 5 was not met. On scene 19f339ba, with the car 0.5 s earlier, the car at 1.25x speed and the ego at 1.4x (S26), every run failed. In each one the policy braked hard on an open highway for no visible reason, drifted left and struck a car coming up in the left lane. Three more scenes each have a strong candidate whose range does not yet clear 0.5: 187e6244 (S23), 023b7fcc (S1) and 1c45ce3a (S28, resting on only two runs). On 023b7fcc and 187e6244 the policy drifted left into the next lane against a RIGHT command. Most failures on 1c45ce3a were replayed cars cutting into a gap the human had already cleared, so they may not be the policy's fault. No scene gave a lead-vehicle braking failure or a departure from the road, and the other six scenes did not fail in the few runs each got.

## Findings

- The one confirmed challenging case: on 19f339ba, with the car 0.5 s earlier at 1.25x and the ego at 1.4x, every run failed. In every run the policy was at fault. It braked hard with no lead car within about 45 m, drifted left and hit actor 1 coming up in the left lane.
  - S26: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_038, car_conflicts_3knobs_2hz_optuna_confirm_r2_041, car_conflicts_3knobs_2hz_optuna_confirm_r2_051)
- On 187e6244, the car 0.5 s later at 0.75x with the ego at 0.8x failed in most runs, but the range's lower end sits just under 0.5. Most of these failures were the policy steering left out of its lane against a RIGHT command and sideswiping car 7. One was car 7 drifting into the ego's left rear, where fault is unclear.
  - S23: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 4/5 failed, rate 44%-95% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_017, car_conflicts_3knobs_2hz_optuna_confirm_r2_021, car_conflicts_3knobs_2hz_optuna_confirm_r2_031, car_conflicts_3knobs_2hz_optuna_confirm_r2_043, car_conflicts_3knobs_2hz_optuna_confirm_r2_053)
- On 023b7fcc, the car 0.5 s earlier at 1.0x with the ego slowed to 0.6x failed in most runs, but it is not yet confirmed above 0.5. Every failure was the policy's fault. The ego sped up, drifted about 2 m left of the human path against a RIGHT command, and made side contact with actor 56 in the left lane.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_006, car_conflicts_3knobs_2hz_optuna_confirm_r2_014, car_conflicts_3knobs_2hz_optuna_confirm_r2_023, car_conflicts_3knobs_2hz_optuna_confirm_r2_033, car_conflicts_3knobs_2hz_optuna_confirm_r2_044, car_conflicts_3knobs_2hz_optuna_confirm_r2_054)
- The same knob values did not fail on 187e6244, so the 023b7fcc failure depends on the scene, not just the setting.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_006, car_conflicts_3knobs_2hz_optuna_confirm_r2_014, car_conflicts_3knobs_2hz_optuna_confirm_r2_023, car_conflicts_3knobs_2hz_optuna_confirm_r2_033, car_conflicts_3knobs_2hz_optuna_confirm_r2_044, car_conflicts_3knobs_2hz_optuna_confirm_r2_054)
  - S21: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_007, car_conflicts_3knobs_2hz_optuna_confirm_r2_013)
- On 1c45ce3a, failures appeared at several settings with the ego at 0.8x, but triage puts little of the blame on the policy. In most of them a replayed car (actor 24, once actor 14) cut across the lane line into the ego's front-right corner, at a moment when the slowed ego sat about 8–20 m behind where the human had been. Triage rated fault unclear or not the policy's. S28 failed in both of its runs, but that is a hint, not a rate.
  - S28: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_048_a2, car_conflicts_3knobs_2hz_optuna_confirm_r2_052)
  - S30: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_026_a2, car_conflicts_3knobs_2hz_optuna_confirm_r2_032)
  - S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_005, car_conflicts_3knobs_2hz_optuna_confirm_r2_011, car_conflicts_3knobs_2hz_optuna_confirm_r2_022, car_conflicts_3knobs_2hz_optuna_confirm_r2_042)
- No failures appeared on 096988dd, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3 or 12855a41. Most of their settings got a single run, so they are only lightly searched, not shown safe. The one well-repeated setting there, 12855a41 with the car 1.5 s later at 1.0x and the ego at 0.8x, did not fail and its range stays low.
  - S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_058)
  - S6: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_050)
  - S7: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_059)
  - S8: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_002)
  - S9: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_028)
  - S10: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_056)
  - S11: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_047, car_conflicts_3knobs_2hz_optuna_confirm_r2_055)
  - S12: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_003, car_conflicts_3knobs_2hz_optuna_confirm_r2_025, car_conflicts_3knobs_2hz_optuna_confirm_r2_035)
  - S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_060)
  - S14: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_039)
  - S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_008)
  - S16: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_049)
  - S17: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_037_a2)
  - S18: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_009, car_conflicts_3knobs_2hz_optuna_confirm_r2_012)
  - S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_001, car_conflicts_3knobs_2hz_optuna_confirm_r2_015, car_conflicts_3knobs_2hz_optuna_confirm_r2_024, car_conflicts_3knobs_2hz_optuna_confirm_r2_034, car_conflicts_3knobs_2hz_optuna_confirm_r2_045_a2)
  - S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_020)
- Across scenes, the at-fault failures are lateral: the policy drifts or steers into a car in the adjacent lane. None is a failure to brake for a lead car, and no run left the road. Every failing setting has the ego off its recorded speed (0.6x, 0.8x or 1.4x).
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_006, car_conflicts_3knobs_2hz_optuna_confirm_r2_014, car_conflicts_3knobs_2hz_optuna_confirm_r2_023, car_conflicts_3knobs_2hz_optuna_confirm_r2_033, car_conflicts_3knobs_2hz_optuna_confirm_r2_044, car_conflicts_3knobs_2hz_optuna_confirm_r2_054)
  - S23: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 4/5 failed, rate 44%-95% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_017, car_conflicts_3knobs_2hz_optuna_confirm_r2_021, car_conflicts_3knobs_2hz_optuna_confirm_r2_031, car_conflicts_3knobs_2hz_optuna_confirm_r2_043, car_conflicts_3knobs_2hz_optuna_confirm_r2_053)
  - S26: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_038, car_conflicts_3knobs_2hz_optuna_confirm_r2_041, car_conflicts_3knobs_2hz_optuna_confirm_r2_051)
  - S28: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_048_a2, car_conflicts_3knobs_2hz_optuna_confirm_r2_052)
  - S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_005, car_conflicts_3knobs_2hz_optuna_confirm_r2_011, car_conflicts_3knobs_2hz_optuna_confirm_r2_022, car_conflicts_3knobs_2hz_optuna_confirm_r2_042)

## Open

- Four more confirmed cases are still needed. A few more repeats at S23 (187e6244) and S1 (023b7fcc) would show whether their ranges clear 0.5. These are the cheapest next confirmations.
- S28 on 1c45ce3a rests on two runs, and its failures may come from the replayed traffic rather than the policy. Repeats there, plus a run of the same setting with reactive traffic or with the ego at 1.0x, would show whether actor 24's cut-in is a replay artifact (the replayed car merging into a gap the human had cleared, now taken by a slower ego).
- The 1c45ce3a failures involve actor 24 (and once actor 14), while the retimed track is 14. Failures appear across different car timings and speeds, which suggests the ego's 0.8x speed drives them, not the retimed car. A sweep of ego speed alone on that scene would test this.
- Neighbouring settings around S26 on 19f339ba are untested (e.g. ego 1.2x, or the car at 1.0x or 1.5x). Those runs would show how wide the failure region is and whether the unexplained hard braking is the main cause.
- Six scenes (096988dd, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41) got mostly single runs at scattered settings. A fifth distinct scene with a confirmed case would need more search there. Settings with the ego off its recorded speed are the best bet, since every failing setting had that. 0dbb91dd showed no approach to other actors at all (criticality 0).
- The 2 Hz planning rate was assumed from configuration, not checked. The run logs should be checked to confirm the policy actually planned every 500 ms.
- Several runs were re-run or halted by the gate (mostly on 1c45ce3a) and are not counted. Why that scene halts at high ego speed (1.4x) is unknown.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, actor_hit_ego 7, other 1

- car_conflicts_3knobs_2hz_optuna_confirm_r2_005: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane at about 8 m/s, roughly 20 m behind where the human drove, while log-replayed cars passed it on the right. Actor 24 moved left from the right lane into the ego's lane (about 1 m of lateral shift between 8.2 s and 9.2 s) and its side met the ego's front-right corner, which counts as a front collision. The ego itself moved only about 0.5 m off the recorded path.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_011: actor_hit_ego, policy at fault: unclear. On a straight highway, the ego slowed from 8.7 to 7.0 m/s in its lane while vehicles came up from behind on the right; actor 14 passed and cut in about 10 m ahead, then actor 24 came alongside and leaned across the lane line into the ego's front-right corner. The ego was only 0.4 m off the recorded human path, and its planned path and heading tilted slightly right, so it may have helped close the gap. It's unclear whether the policy or actor 24 was mostly to blame.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_014: turned_into_actor, policy at fault: yes. On a multi-lane arterial with the command changing to RIGHT, the ego sped up from 2.5 to 5.9 m/s. Instead of following its planned path to the right, it yawed and drifted about 2 m left of the recorded trajectory, onto the left lane line. There it made side contact with actor 56, which was coming up in the adjacent left lane just behind it; 56 also struck the ego's rear.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_017: turned_into_actor, policy at fault: yes. The ego was following slow car 48 on a multi-lane highway at about 4 m/s. Instead of following its route, which bore right (command RIGHT), it steered left toward the next lane and its side hit car 7, which was coming up from behind in that lane. The ego was about 2 m off the recorded path at impact, and car 7 also made contact with the ego's rear.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_021: turned_into_actor, policy at fault: yes. On the multi-lane highway, the ego crept left out of its lane behind the slow white car (48), ending up about 1.9 m left of the recorded path. Its side then hit car 7, which was coming up from behind in the left adjacent lane (lateral collision at 8.2 s). The route command was RIGHT and the planned path pointed right, but the ego's actual motion kept drifting left.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_026_a2: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane on a highway at about 8 m/s and stayed within 0.45 m of the human's path. Actor 24 came up from the right rear and cut left across the lane line into the ego's front-right corner, which counted as a front collision at 9.2 s. The ego was about 20 m behind where the human was at that time, so the replayed actor merged into space the human had already cleared.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_033: turned_into_actor, policy at fault: yes. After handoff, the ego sped up from 2.5 to 6 m/s. It steered left into the next lane, while the recorded human path and the RIGHT command went straight or right. At 7.7 s it made side contact with actor 56, which was driving alongside and slightly behind it in that lane. No vehicle was close ahead, so this was a bad lane change by the ego, not a failure to brake.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_038: turned_into_actor, policy at fault: yes. On a straight multi-lane highway with no lead vehicle within about 45 m, the policy braked hard for no clear reason (23.7 to 7.4 m/s) and drifted left toward the lane line. Actor 1, which had been behind on the left, came up alongside, and the ego's front-left corner struck it.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_041: other, policy at fault: yes. After handoff the ego braked hard on an open highway, from 22 to 6.4 m/s, with no lead within about 45–50 m, and fell 13.5 m behind its recorded position. Actor 1, a replayed vehicle from the lane to the left that expected the ego to be further ahead, drew level and cut into the ego's lane just in front, so the ego's front struck it; the ego was also rear-ended by traffic behind.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_042: actor_hit_ego, policy at fault: no. The ego kept straight in its lane on a multi-lane arterial, within 0.3 m of the recorded path, but eased off from 9.8 to 8.3 m/s, so by 7.7 s it was about 8 m behind where the human was at that time. Actor 14 came up from behind on the right and passed the ego. Its replayed path then merged into the ego's lane, into the space the logged car had already left, and it hit the ego's front-right corner. The ego could not have avoided this.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_043: turned_into_actor, policy at fault: yes. On the highway behind lead car 48, the ego steered left out of its lane (orange path), away from the recorded route, which went straight and then RIGHT. It sideswiped actor 7, which was coming up from behind in the left lane (lateral collision at 8.2 s).
- car_conflicts_3knobs_2hz_optuna_confirm_r2_044: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego sped up from 2.5 to 6 m/s and drifted about 2 m to the side of the recorded human path, into the edge of the neighboring lane. There it made side contact with actor 56, which was alongside and just behind it (lateral collision, with rear contact also recorded); the cars ahead were never close.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_048_a2: actor_hit_ego, policy at fault: unclear. The ego was going straight in its freeway lane at about 8 m/s, within 0.4 m of the recorded path laterally. Actor 24 came up from behind in the lane to the right and moved left across the lane line, so its rear clipped the ego's front-right corner. The ego was about 20 m behind where the human car was at that moment (the faint box ahead on the map). The other car is a replay of the real drive, so it cut into a gap that held the human car but now held the ego.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_051: turned_into_actor, policy at fault: yes. On an open highway, with the nearest vehicle ahead about 45–50 m away, the ego braked hard for no visible reason (23.7 to 7.5 m/s) and drifted left toward the lane line. Actor 1, coming up in the left lane from behind, drew alongside, and the ego's front-left clipped it. This counts as an at-fault front collision; the ego was also rear-ended at some point.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_052: actor_hit_ego, policy at fault: unclear. The ego was going straight at about 8 m/s in its lane when actor 24 came up from behind in the lane to its right, passed it, and closed in on its front-right corner, clipping it at 9.2 s. The ego had drifted only about 0.65 m right of the recorded human path, so the contact mostly comes from the replayed actor sweeping across the lane line, with a small contribution from the ego's rightward drift.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_053: actor_hit_ego, policy at fault: unclear. On the freeway, the recorded human driver moved right toward car 48's lane. The ego instead held its lane at about 4–5 m/s, with its plan bending slightly left. Car 7 came from behind-left and drifted right into the space the human had left, so it hit the ego's left rear side at 8.2 s, which is a lateral contact that also counts as being rear-ended.
- car_conflicts_3knobs_2hz_optuna_confirm_r2_054: turned_into_actor, policy at fault: yes. On a multi-lane road with a RIGHT command, the ego sped up from 2.5 to 5.7 m/s and drifted about 2 m to the left of the recorded human path, across the lane line. Its side hit actor 56, which was travelling alongside on the left-rear in the next lane, so the result was a lateral collision rather than a lead-vehicle impact.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_006, car_conflicts_3knobs_2hz_optuna_confirm_r2_014, car_conflicts_3knobs_2hz_optuna_confirm_r2_023, car_conflicts_3knobs_2hz_optuna_confirm_r2_033, car_conflicts_3knobs_2hz_optuna_confirm_r2_044, car_conflicts_3knobs_2hz_optuna_confirm_r2_054)
- S2: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_036)
- S3: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_029)
- S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_040)
- S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_058)
- S6: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_050)
- S7: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_059)
- S8: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_002)
- S9: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_028)
- S10: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_056)
- S11: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_047, car_conflicts_3knobs_2hz_optuna_confirm_r2_055)
- S12: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_003, car_conflicts_3knobs_2hz_optuna_confirm_r2_025, car_conflicts_3knobs_2hz_optuna_confirm_r2_035)
- S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_060)
- S14: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_039)
- S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_008)
- S16: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_049)
- S17: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_037_a2)
- S18: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_009, car_conflicts_3knobs_2hz_optuna_confirm_r2_012)
- S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_001, car_conflicts_3knobs_2hz_optuna_confirm_r2_015, car_conflicts_3knobs_2hz_optuna_confirm_r2_024, car_conflicts_3knobs_2hz_optuna_confirm_r2_034, car_conflicts_3knobs_2hz_optuna_confirm_r2_045_a2)
- S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_020)
- S21: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_007, car_conflicts_3knobs_2hz_optuna_confirm_r2_013)
- S22: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_004)
- S23: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 4/5 failed, rate 44%-95% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_017, car_conflicts_3knobs_2hz_optuna_confirm_r2_021, car_conflicts_3knobs_2hz_optuna_confirm_r2_031, car_conflicts_3knobs_2hz_optuna_confirm_r2_043, car_conflicts_3knobs_2hz_optuna_confirm_r2_053)
- S24: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_010)
- S25: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_057)
- S26: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_038, car_conflicts_3knobs_2hz_optuna_confirm_r2_041, car_conflicts_3knobs_2hz_optuna_confirm_r2_051)
- S27: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_016)
- S28: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_048_a2, car_conflicts_3knobs_2hz_optuna_confirm_r2_052)
- S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_019)
- S30: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_026_a2, car_conflicts_3knobs_2hz_optuna_confirm_r2_032)
- S31: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_030_a2)
- S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_005, car_conflicts_3knobs_2hz_optuna_confirm_r2_011, car_conflicts_3knobs_2hz_optuna_confirm_r2_022, car_conflicts_3knobs_2hz_optuna_confirm_r2_042)
- S33: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r2_027)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r2_018: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r2_026: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r2_030: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r2_037: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r2_045: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r2_046: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r2_048: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 34 s; every count above is computed from the queue, not written by the model.

0 of 65 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
