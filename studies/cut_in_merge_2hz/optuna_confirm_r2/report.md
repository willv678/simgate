# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `optuna_confirm_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 1 of the 5 cases it was looking for, so the goal was not met. That case is scene 023b7fcc with the cars 1.0 s later and at 1.5x speed (S9), where every run failed. Even there, half of those failures had unclear fault: car 56 moved over into the ego's lane. In the other half, the ego drifted left into car 56. A second scene, 19f339ba with the cars 1.0 s earlier at 1.5x speed (S29), failed in most of its runs, but its range still includes rates below one half, so it is a strong candidate rather than a confirmed case. Across the failures, the main cause was less the retiming than the policy drifting left into the next lane, where it hit a car alongside or was sideswiped from behind. None of the failures was flagged as a possible simulator artifact.

## Findings

- The one confirmed case is scene 023b7fcc with the cars 1.0 s later and at 1.5x speed, where every run failed. In two of these runs the ego drifted left into car 56 (policy at fault). In the other two, car 56 moved into the ego's lane while the ego sped up (fault unclear).
  - S9: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_017, cut_in_merge_2hz_optuna_confirm_r2_019, cut_in_merge_2hz_optuna_confirm_r2_023, cut_in_merge_2hz_optuna_confirm_r2_032)
- Scene 19f339ba with the cars 1.0 s earlier at 1.5x speed failed in most runs, but it is not confirmed above one half. In the triaged failures the ego wandered about 2 m left of its route, into the next lane, and a small car coming up from behind sideswiped it. The policy was at fault, and these were side hits, not rear-end hits.
  - S29: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.5: 3/4 failed, rate 36%-94% (90%) (cut_in_merge_2hz_optuna_confirm_r2_026, cut_in_merge_2hz_optuna_confirm_r2_028, cut_in_merge_2hz_optuna_confirm_r2_037, cut_in_merge_2hz_optuna_confirm_r2_048)
- Scene 023b7fcc also failed in single runs with the cars earlier: 2.0 s earlier at 1.25x, 1.5 s earlier at 0.5x, and 1.0 s earlier at 1.0x. One run each is only a hint. The 1.5 s / 0.5x failure was a late reaction to a lead car that was already close at handover, so the replay or box sizes may have contributed.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_034)
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_033)
  - S3: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_027)
- Other timings on 023b7fcc did not fail in their single runs: 1.0 s earlier at 2x, 0.5 s earlier at 1.5x, 0.5 s and 2.0 s later at 1.0x, and 1.0 s later at 0.5x and 0.75x. So the failures on this scene do not follow a simple trend in timing or speed.
  - S4: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_052)
  - S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_035)
  - S6: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_051)
  - S7: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_053)
  - S8: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_041)
  - S10: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_054)
- Settings repeated without a single failure look unlikely to be challenging: 054b5901 with the cars 0.5 s later at 1.5x, 09a95ffa at 0 s and 0.5x, 0e899dd3 with the cars 0.5 s later at 0.5x, and 12855a41 at 0 s and 2x. Their ranges stay below one half.
  - S13: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_optuna_confirm_r2_002, cut_in_merge_2hz_optuna_confirm_r2_010, cut_in_merge_2hz_optuna_confirm_r2_020, cut_in_merge_2hz_optuna_confirm_r2_029, cut_in_merge_2hz_optuna_confirm_r2_039, cut_in_merge_2hz_optuna_confirm_r2_047)
  - S19: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r2_018, cut_in_merge_2hz_optuna_confirm_r2_021, cut_in_merge_2hz_optuna_confirm_r2_030, cut_in_merge_2hz_optuna_confirm_r2_038, cut_in_merge_2hz_optuna_confirm_r2_046)
  - S23: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_optuna_confirm_r2_024, cut_in_merge_2hz_optuna_confirm_r2_031, cut_in_merge_2hz_optuna_confirm_r2_040, cut_in_merge_2hz_optuna_confirm_r2_049)
  - S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 2.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_optuna_confirm_r2_009, cut_in_merge_2hz_optuna_confirm_r2_012, cut_in_merge_2hz_optuna_confirm_r2_022)
- Most failures came from the ego drifting left into the adjacent lane, not from braking too late for a car cutting in. This is true even at 2 Hz planning, which the brief says halves the left drift.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_034)
  - S3: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_027)
  - S9: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_017, cut_in_merge_2hz_optuna_confirm_r2_019, cut_in_merge_2hz_optuna_confirm_r2_023, cut_in_merge_2hz_optuna_confirm_r2_032)
  - S29: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.5: 3/4 failed, rate 36%-94% (90%) (cut_in_merge_2hz_optuna_confirm_r2_026, cut_in_merge_2hz_optuna_confirm_r2_028, cut_in_merge_2hz_optuna_confirm_r2_037, cut_in_merge_2hz_optuna_confirm_r2_048)

## Open

- Whether 19f339ba with the cars 1.0 s earlier at 1.5x (S29) is reliably above one half: run it a few more times. A further run of failures would confirm it as a second case.
- Scenes 096988dd, 0cf6368d and 1c45ce3a got only one or two runs at a few settings (S16, S17, S22, S32), so whether they can be broken is untested. Search them further: the cut-in scenes 0cf6368d and 1c45ce3a are the only ones besides 12855a41 where the cut-in car is retimed on its own.
- In two of the four S9 failures, car 56 moved into the ego's lane and fault was unclear. More S9 runs would show how often the ego is at fault there.
- The single-run failures on 023b7fcc (S1, S2, S3) were not repeated. They do not matter for the top 5, which allows one case per scene, but they show this scene fails at several timings.
- This report cannot compare with the 10 Hz study cut_in_merge. That needs its results set beside these, scene by scene, especially the share of failures from left drift.

## Why the runs failed (triage from the video and log)

turned_into_actor 7, actor_hit_ego 2, no_brake_for_lead 1

- cut_in_merge_2hz_optuna_confirm_r2_017: actor_hit_ego, policy at fault: unclear. On a multi-lane highway, the recorded human driver moved one lane left. The policy instead kept straight in its own lane and sped up from about 4.5 to 6.7 m/s. Meanwhile actor 56, which had been just behind and to the left of the ego, moved ahead and edged into the ego's lane. At 7.2 s the ego's front-left clipped 56's rear corner, with the gap to 56 at 3.5 m. A trailing actor also struck the ego's rear.
- cut_in_merge_2hz_optuna_confirm_r2_019: actor_hit_ego, policy at fault: unclear. On a busy multi-lane highway, the ego sped up from 4.2 to 6.8 m/s and kept to its own lane. Actor 56, which had been travelling beside it on the left, moved over in front of the ego: the gap to the car ahead fell from 21.8 m to 3.6 m within 0.5 s, and the ego's front clipped 56. The ego was 1.6 m from where the recorded car drove (that car moved left), so the replayed actor merged into a lane the ego still occupied. The ego was speeding up rather than holding back for the car beside it, but it had too little time to avoid the merge.
- cut_in_merge_2hz_optuna_confirm_r2_023: turned_into_actor, policy at fault: yes. The ego was speeding up from 4.5 to 6.7 m/s on a multi-lane road and yawed left (on the map the lanes tilt against its heading), so its front-left hit actor 56, which was travelling next to it in the left adjacent lane. A following vehicle also hit the ego's rear, but the front contact with 56 happened first.
- cut_in_merge_2hz_optuna_confirm_r2_026: turned_into_actor, policy at fault: yes. At about 4 m/s on a multi-lane highway, the ego drifted about 2 m left of its route and the recorded path, even though the command was RIGHT and then STRAIGHT. Actor 29, which was coming up from behind on the left, then sideswiped the ego's left side at 12.1 s. The front gap was over 27 m until the contact, so this was not a lead-vehicle collision.
- cut_in_merge_2hz_optuna_confirm_r2_027: turned_into_actor, policy at fault: yes. On a straight multi-lane highway in slow traffic, the ego sped up from about 4 to 6.4 m/s and drifted about 1.6 m left of the recorded path (the ghost box), so its body crossed toward the lane boundary. It sideswiped actor 56, which was travelling alongside in the adjacent left lane, and the collision was scored as lateral. The lead car stayed about 18 m or more ahead the whole time, so this was not a failure to brake for a lead vehicle.
- cut_in_merge_2hz_optuna_confirm_r2_028: turned_into_actor, policy at fault: yes. On a multi-lane highway the ego slowed for no clear reason (5.3 to 3.3 m/s, lead 22+ m ahead) and drifted about 1.9 m left of the recorded path, partly into the next lane, where small actor 29, overtaking from behind, sideswiped its left-rear side.
- cut_in_merge_2hz_optuna_confirm_r2_032: turned_into_actor, policy at fault: yes. After handoff the ego sped up from 4.5 to 6.7 m/s and drifted left toward the adjacent lane, roughly following the leftward recorded path. Its front hit the rear-right of actor 56, which was just ahead in that left lane. The rear contact from a following actor came after this front collision.
- cut_in_merge_2hz_optuna_confirm_r2_033: no_brake_for_lead, policy at fault: unclear. In slow, dense highway traffic going STRAIGHT, the ego was already closing on lead car 12 in its lane when the policy took over at 4.7 s (gap 5.5 m, closing at about 1.4 m/s). The policy slowed only a little (4.2 to 3.4 m/s) and planned a late swerve left, and its front clipped car 12 at 5.7 s. The ego was only about 0.2 to 0.6 m from where the human drove, so the takeover state was already very tight, and the collision may partly come from the replay or the box sizes.
- cut_in_merge_2hz_optuna_confirm_r2_034: turned_into_actor, policy at fault: yes. On a congested multi-lane highway, the ego was following actor 13 at about 4.5 m/s when the policy's planned path (orange) swung left, away from the straight route. The ego drifted into the left adjacent lane and its front struck actor 61, which was travelling alongside slightly ahead in that lane.
- cut_in_merge_2hz_optuna_confirm_r2_048: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was slowing (4.9→3.5 m/s) and its plan wandered left of the recorded route, until it was about 2.2 m left of where the human drove and straddling the line into the left lane. A small actor (id 29, probably a motorcycle) coming up from behind in that lane hit the ego's left side.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_034)
- S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_033)
- S3: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_027)
- S4: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_052)
- S5: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_035)
- S6: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_051)
- S7: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_053)
- S8: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_041)
- S9: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r2_017, cut_in_merge_2hz_optuna_confirm_r2_019, cut_in_merge_2hz_optuna_confirm_r2_023, cut_in_merge_2hz_optuna_confirm_r2_032)
- S10: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_054)
- S11: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_005)
- S12: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_015)
- S13: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_optuna_confirm_r2_002, cut_in_merge_2hz_optuna_confirm_r2_010, cut_in_merge_2hz_optuna_confirm_r2_020, cut_in_merge_2hz_optuna_confirm_r2_029, cut_in_merge_2hz_optuna_confirm_r2_039, cut_in_merge_2hz_optuna_confirm_r2_047)
- S14: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_014)
- S15: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_008)
- S16: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_050)
- S17: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_003)
- S18: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_004)
- S19: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r2_018, cut_in_merge_2hz_optuna_confirm_r2_021, cut_in_merge_2hz_optuna_confirm_r2_030, cut_in_merge_2hz_optuna_confirm_r2_038, cut_in_merge_2hz_optuna_confirm_r2_046)
- S20: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r2_007, cut_in_merge_2hz_optuna_confirm_r2_011)
- S21: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_006)
- S22: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_043)
- S23: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_optuna_confirm_r2_024, cut_in_merge_2hz_optuna_confirm_r2_031, cut_in_merge_2hz_optuna_confirm_r2_040, cut_in_merge_2hz_optuna_confirm_r2_049)
- S24: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_044)
- S25: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_016)
- S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 2.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_optuna_confirm_r2_009, cut_in_merge_2hz_optuna_confirm_r2_012, cut_in_merge_2hz_optuna_confirm_r2_022)
- S27: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_042)
- S28: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_045)
- S29: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.5: 3/4 failed, rate 36%-94% (90%) (cut_in_merge_2hz_optuna_confirm_r2_026, cut_in_merge_2hz_optuna_confirm_r2_028, cut_in_merge_2hz_optuna_confirm_r2_037, cut_in_merge_2hz_optuna_confirm_r2_048)
- S30: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_036)
- S31: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r2_025)
- S32: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r2_001, cut_in_merge_2hz_optuna_confirm_r2_013)

## Provenance

Plan: `plan.json` (rationale: Copied from studies/cut_in_merge/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scope and settings follow the brief. Traffic is replayed as recorded. Only recorded cars (class automobile) are retimed, using the knobs' full ranges: -2 s to +2 s and 0.5x to 2x speed.

Scene choice: 31 scenes carry the merge_cut_in tag. I kept 9 that passed at 0 delay and have a car identified as a key actor. Scenes that already fail with the recorded timing would fill the top 5 without showing what the retiming does, so I left them out. Three scenes have a car marked as cutting in (0cf6368d track 21, 12855a41 track 31, 1c45ce3a track 14). In those, only that car is retimed. The other six retime every car in the scene: with only a lead or crossing car identified, retiming that car alone could miss the car that actually changes lanes. Several picks already came close at baseline (023b7fcc and 096988dd at 0.0 m, 19f339ba at 0.03 m, 12855a41 at 0.08 m, 054b5901 at 0.26 m), so they are good places to look first.

Budget and stopping rule: 6 rounds of 9 runs gives 54 runs, close to the brief's ~50 and under the cap of 60. The goal is top_k with k=5, one case per scene, failure rate surely above 0.5. A setting needs about 4 failures in 4 runs to clear that bar, so confirming 5 cases costs about 20 to 25 runs. That leaves roughly 30 runs to search, and the study stops early once 5 cases are confirmed.

What this plan cannot do:
- If fewer than 5 scenes break reliably within the budget, the study will report fewer than 5 confirmed cases.
- Near misses can guide the search, but the stopping rule only counts failures, so they are not a checked ranking.
- The tags do not say whether the ego merges or another car cuts in, so the two cases cannot be told apart.
- The 0-delay results were recorded with learned (CATK) traffic, not replay, so the pass/fail used to pick scenes is only a guide.
- Retiming a whole class moves every car in the scene, not only the one changing lanes.
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
