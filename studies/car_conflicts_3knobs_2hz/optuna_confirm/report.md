# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm`: 60 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Two settings on two different scenes were confirmed as challenging, and only one of them is a clear policy failure. On 096988dd, the car 1 s early at 2x speed with the ego at 1.2x (S5) failed every run: the policy drifted left out of its lane into car 41 alongside it. On 1c45ce3a, the car 2 s late at 2x speed with the ego at 0.8x (S34) also failed every run, but triage blames a replayed car (24) cutting into the slowed ego, so that failure comes from replay rather than from a clear policy mistake. The strongest third candidate is 187e6244 with the lead car 1.5 s late at 0.75x and the ego at 0.8x (S31). The policy drove into the lead car there, but the range still straddles 0.5, so it is not confirmed. The other six scenes never failed, though most of their settings got only one run, which is a hint and not a rate.

## Findings

- The 096988dd case is confirmed and the policy is at fault. At 1 s early, 2x car speed and 1.2x ego speed, every run failed the same way: under a STRAIGHT or RIGHT command the planned path bent left and the ego's front corner hit car 41 passing in the left lane.
  - S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_029, car_conflicts_3knobs_2hz_optuna_confirm_031, car_conflicts_3knobs_2hz_optuna_confirm_041)
- On 096988dd the left drift into car 41 shows up across very different car timings and speeds, so the retimed car (track 2) does not seem to drive it. Where it fails, the ego is at 1.0x or faster. Runs with the ego at 0.6x or 0.8x did not fail, but each of those settings got only a single run.
  - S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_029, car_conflicts_3knobs_2hz_optuna_confirm_031, car_conflicts_3knobs_2hz_optuna_confirm_041)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_059)
  - S7: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_030)
  - S8: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_006, car_conflicts_3knobs_2hz_optuna_confirm_012_a2, car_conflicts_3knobs_2hz_optuna_confirm_021)
  - S11: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_027, car_conflicts_3knobs_2hz_optuna_confirm_037)
  - S9: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_047)
  - S10: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_050)
  - S12: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_038)
- The 1c45ce3a case (2 s late, 2x, ego 0.8x) failed every run, but none of these failures is clearly the policy's. In each one the ego stayed within 0.5 m of its recorded path, about 20 m behind the human car, and replayed car 24 overtook on the right and merged into the ego's front-right corner. Triage marks policy fault 'unclear' or 'no'.
  - S34: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_028, car_conflicts_3knobs_2hz_optuna_confirm_032, car_conflicts_3knobs_2hz_optuna_confirm_042)
- 187e6244 with the lead car 1.5 s late at 0.75x and the ego at 0.8x is the best unconfirmed candidate, and the policy is at fault there. The ego took over about 2 m behind lead car 48, did not slow enough and hit it from behind. It then swerved left against a RIGHT command and scraped car 7. Its range still reaches below 0.5.
  - S31: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/5 failed, rate 27%-86% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_018, car_conflicts_3knobs_2hz_optuna_confirm_023, car_conflicts_3knobs_2hz_optuna_confirm_033, car_conflicts_3knobs_2hz_optuna_confirm_043, car_conflicts_3knobs_2hz_optuna_confirm_051)
- None of 023b7fcc, 09a95ffa, 0cf6368d, 0e899dd3, 12855a41 or 19f339ba failed in any setting tried. Only a few settings were repeated: 19f339ba at 1.5 s early, 0.75x, ego 1.4x; 12855a41 at 1.5 s late, 0.75x, ego 1.4x; and a few others with 3 runs. Those keep their failure rates below 0.5.
  - S1: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_008, car_conflicts_3knobs_2hz_optuna_confirm_013_a2, car_conflicts_3knobs_2hz_optuna_confirm_054)
  - S20: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_004, car_conflicts_3knobs_2hz_optuna_confirm_014, car_conflicts_3knobs_2hz_optuna_confirm_055)
  - S23: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_020, car_conflicts_3knobs_2hz_optuna_confirm_024, car_conflicts_3knobs_2hz_optuna_confirm_045)
  - S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_005, car_conflicts_3knobs_2hz_optuna_confirm_011, car_conflicts_3knobs_2hz_optuna_confirm_035, car_conflicts_3knobs_2hz_optuna_confirm_053)
  - S32: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_017, car_conflicts_3knobs_2hz_optuna_confirm_022, car_conflicts_3knobs_2hz_optuna_confirm_034, car_conflicts_3knobs_2hz_optuna_confirm_044, car_conflicts_3knobs_2hz_optuna_confirm_052)
- These scenes produced the closest calls without a failure (high criticality), so they are the near misses the brief ranks next: 187e6244 at recorded timing with the car at 0.5x; 19f339ba at 1.5 s early, 0.75x, ego 1.4x; and 12855a41 at 1 s late, 2x, ego 1.2x.
  - S29: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_060)
  - S32: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_017, car_conflicts_3knobs_2hz_optuna_confirm_022, car_conflicts_3knobs_2hz_optuna_confirm_034, car_conflicts_3knobs_2hz_optuna_confirm_044, car_conflicts_3knobs_2hz_optuna_confirm_052)
  - S24: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_056)
- No failure was flagged as a possible rendering or off-trajectory artifact. The two runs the gate did not keep were re-runs and are not counted.
  - S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_029, car_conflicts_3knobs_2hz_optuna_confirm_031, car_conflicts_3knobs_2hz_optuna_confirm_041)
  - S31: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/5 failed, rate 27%-86% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_018, car_conflicts_3knobs_2hz_optuna_confirm_023, car_conflicts_3knobs_2hz_optuna_confirm_033, car_conflicts_3knobs_2hz_optuna_confirm_043, car_conflicts_3knobs_2hz_optuna_confirm_051)
  - S34: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_028, car_conflicts_3knobs_2hz_optuna_confirm_032, car_conflicts_3knobs_2hz_optuna_confirm_042)

## Open

- Confirm or reject 187e6244 at 1.5 s late, 0.75x, ego 0.8x (S31) with a few more repeats. This is the only candidate where the retimed car itself causes a policy failure.
- Find out whether the 1c45ce3a case (S34) is a replay artifact. Re-run it with reactive traffic, or with the ego at 1.0x so it stays level with the human car, and see whether car 24 still merges into it.
- On 096988dd, test whether the left drift into car 41 depends on the knobs at all. Repeat the ego-speed boundary (0.8x vs 1.0x) at fixed car timing and speed, and re-check the recorded setting, to decide whether this is a scene-wide lane-keeping weakness rather than a cut-in or lead-vehicle failure.
- Three more confirmed scenes are still needed. Spend repeats near the closest calls on 187e6244 (recorded timing, 0.5x), 19f339ba and 12855a41, and give the single-run settings on 09a95ffa, 0cf6368d and 1c45ce3a's other corners a second run.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, actor_hit_ego 3, no_brake_for_lead 2

- car_conflicts_3knobs_2hz_optuna_confirm_021: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a STRAIGHT command, the ego (about 5 m/s) drifted left out of its lane, about 1.3 m off the recorded path, and its front corner hit actor 41, which was passing in the adjacent left lane. There was no lead-vehicle problem; the ego moved sideways into a car that was already alongside it.
- car_conflicts_3knobs_2hz_optuna_confirm_023: no_brake_for_lead, policy at fault: yes. The ego was in slow freeway traffic and followed lead vehicle 48 only 2–4 m back. It sped up from 3 to 5.5 m/s instead of holding back and made front contact with 48 by 6.2 s. It then edged left and also scraped vehicle 7 beside it at 8.2 s. Something also hit the ego's rear at some point, but the front contact came first.
- car_conflicts_3knobs_2hz_optuna_confirm_027: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT and then RIGHT, the policy's planned path bent left, away from the recorded path. The ego drifted at about 5 m/s into the lane on its left and its front struck the side of actor 41, which was driving alongside in that lane.
- car_conflicts_3knobs_2hz_optuna_confirm_028: actor_hit_ego, policy at fault: unclear. Actor 24 overtook the ego on the right between 7.2 s and 8.2 s, then moved left into the ego's lane right beside it. At 9.2 s the ego's front-right corner touched the actor's left side while the ego was easing off from 8.6 to 7.4 m/s and staying within 0.5 m of the recorded path. The ego was about 21 m behind where the human car was at that moment, so the replayed cut-in, which happened ahead of the human car in the real drive, landed on the ego. The ego's slow pace and its planned path bending slightly right toward the merging car played a part, but the main cause is the cut-in.
- car_conflicts_3knobs_2hz_optuna_confirm_029: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's planned path kept bending left. The ego slowed from 6.7 to 5.0 m/s and drifted left across the lane line into the next lane, where vehicle 41 was coming up alongside from behind on its left. The ego's front-left corner hit 41.
- car_conflicts_3knobs_2hz_optuna_confirm_030: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the policy's planned path (orange) bent left toward the next lane while the ego slowed from 7.9 to 5.2 m/s. The ego drifted about 1.4 m left of the recorded trajectory and over the lane line, and sideswiped actor 41, which was coming up alongside in the left lane.
- car_conflicts_3knobs_2hz_optuna_confirm_031: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 6.7 to 4.8 m/s while vehicle 41 came up from behind in the lane to its left. The ego drifted left toward the lane line, following the recorded path's leftward shift, and its front clipped the side of 41 as 41 drew alongside.
- car_conflicts_3knobs_2hz_optuna_confirm_032: actor_hit_ego, policy at fault: unclear. The ego was going straight on a highway, staying in its lane and slowing gently from 8.6 to 7.7 m/s, which left it about 20 m behind where the human drove. Actor 24, a replayed car, came up from behind in the lane to the right, drew level and then drifted left into the ego's front-right corner, presumably merging into a spot that was clear in the real drive; the camera smear only shows up at impact.
- car_conflicts_3knobs_2hz_optuna_confirm_033: no_brake_for_lead, policy at fault: yes. The policy took over only 2.2 m behind lead vehicle 48 at 4.4 m/s and slowed only to about 3.2 m/s, so by 5.7s it had driven into 48's rear (front collision). It then swerved left off its planned path, against a RIGHT route command, sped back up and made side contact with actor 7 in the lane to its left at 7.7s.
- car_conflicts_3knobs_2hz_optuna_confirm_037: turned_into_actor, policy at fault: yes. On a multi-lane freeway the route command was RIGHT, but the policy's planned path (orange) bent left, away from the recorded route (green). The ego drifted into the lane on its left and its front hit vehicle 41, which was alongside in that lane, at about 5 m/s.
- car_conflicts_3knobs_2hz_optuna_confirm_041: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 6.7 to 4.5 m/s and drifted left toward the lane line, off the recorded path, even though the command was STRAIGHT and then RIGHT. Vehicle 41 was passing in the left lane, and at 7.7 s the ego's front-left corner, now over the lane line, hit it.
- car_conflicts_3knobs_2hz_optuna_confirm_042: actor_hit_ego, policy at fault: no. The ego kept to its lane at a steady ~8 m/s, within 0.5 m of the recorded path. Actor 24 came up from behind in the right lane, passed the ego and cut left across the lane line into the ego's front-right corner at 9.2 s; the ego also took a rear contact during the run. Because the actor merged into the side of the ego, the hit counted as a front collision, but the ego had little room to avoid it.
- car_conflicts_3knobs_2hz_optuna_confirm_043: turned_into_actor, policy at fault: yes. After taking over 2.2 m behind lead actor 48 (and overlapping it with a front contact from about 5.7s), the policy steered left, against a RIGHT route command and off the recorded path, while speeding up. At 7.7s it side-swiped actor 7 in the lane to its left.
- car_conflicts_3knobs_2hz_optuna_confirm_059: turned_into_actor, policy at fault: yes. On a multi-lane highway the policy's plan drifted left despite a RIGHT route command, pulling the ego about 1.5 m off the recorded path into the adjacent left lane. Its front struck vehicle 41, which was passing on the left as the ego slowed.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_008, car_conflicts_3knobs_2hz_optuna_confirm_013_a2, car_conflicts_3knobs_2hz_optuna_confirm_054)
- S2: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_010)
- S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_009)
- S4: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_046)
- S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_029, car_conflicts_3knobs_2hz_optuna_confirm_031, car_conflicts_3knobs_2hz_optuna_confirm_041)
- S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_059)
- S7: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_030)
- S8: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_006, car_conflicts_3knobs_2hz_optuna_confirm_012_a2, car_conflicts_3knobs_2hz_optuna_confirm_021)
- S9: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_047)
- S10: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_050)
- S11: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_027, car_conflicts_3knobs_2hz_optuna_confirm_037)
- S12: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_038)
- S13: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_049)
- S14: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_026)
- S15: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_040)
- S16: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_036)
- S17: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_002)
- S18: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_003)
- S19: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_058)
- S20: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_004, car_conflicts_3knobs_2hz_optuna_confirm_014, car_conflicts_3knobs_2hz_optuna_confirm_055)
- S21: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_001, car_conflicts_3knobs_2hz_optuna_confirm_025)
- S22: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_019)
- S23: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_020, car_conflicts_3knobs_2hz_optuna_confirm_024, car_conflicts_3knobs_2hz_optuna_confirm_045)
- S24: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_056)
- S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_005, car_conflicts_3knobs_2hz_optuna_confirm_011, car_conflicts_3knobs_2hz_optuna_confirm_035, car_conflicts_3knobs_2hz_optuna_confirm_053)
- S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_016)
- S27: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_048)
- S28: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_007, car_conflicts_3knobs_2hz_optuna_confirm_015)
- S29: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_060)
- S30: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_039)
- S31: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/5 failed, rate 27%-86% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_018, car_conflicts_3knobs_2hz_optuna_confirm_023, car_conflicts_3knobs_2hz_optuna_confirm_033, car_conflicts_3knobs_2hz_optuna_confirm_043, car_conflicts_3knobs_2hz_optuna_confirm_051)
- S32: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_017, car_conflicts_3knobs_2hz_optuna_confirm_022, car_conflicts_3knobs_2hz_optuna_confirm_034, car_conflicts_3knobs_2hz_optuna_confirm_044, car_conflicts_3knobs_2hz_optuna_confirm_052)
- S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_057)
- S34: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_028, car_conflicts_3knobs_2hz_optuna_confirm_032, car_conflicts_3knobs_2hz_optuna_confirm_042)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_012: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_013: not kept: RE-RUN

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

0 of 62 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
