# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 1 of the 5 cases it aimed for, so the goal was not met. The confirmed case is scene 023b7fcc with the cars at their recorded timing and 1.25x speed (S1); every run there failed. In two of those runs the policy drifted left into a car in the next lane, and in the third that car merged into the ego. Scene 09a95ffa is the strongest second candidate (S6 at 0 s, S7 at +0.5 s, both at 1.25x), but neither setting cleared the bar: S7 rests on only two runs, and most failures in this scene come from a replayed car cutting in from behind on the left, so the policy may not be at fault. Almost every setting tested used 1.25x speed and a time shift near 0 s, so this study cannot say how other timings and speeds affect collisions.

## Findings

- Scene 023b7fcc at 0 s shift and 1.25x speed is the only confirmed challenging setting: every run failed, and none were flagged as possible simulator artifacts. In two runs the policy itself drifted or steered left into actor 56 in the next lane, even with the command STRAIGHT. In the third, actor 56 angled into the ego's lane while the ego was running ahead of the recorded human pace, so fault is unclear.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_r2_004, cut_in_merge_2hz_rules_r2_010, cut_in_merge_2hz_rules_r2_019)
- Scene 09a95ffa fails often at 1.25x speed with a 0 s or +0.5 s shift, but neither setting is confirmed above one half. At 0 s, every failure was actor 33 overtaking from the left-rear and cutting across the ego's front-left corner while the ego held its lane. Triage rated these not the policy's fault or unclear, so this scene may say more about replayed traffic ignoring the ego than about the policy.
  - S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 4/5 failed, rate 44%-95% (90%) (cut_in_merge_2hz_rules_r2_007, cut_in_merge_2hz_rules_r2_012, cut_in_merge_2hz_rules_r2_020, cut_in_merge_2hz_rules_r2_028, cut_in_merge_2hz_rules_r2_037)
- At +0.5 s in scene 09a95ffa, both runs failed: once from the policy steering left into a passing car (at fault), and once from a replayed car hitting the ego's left-rear and side while the ego held its lane. Two runs are a hint, not a rate.
  - S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_rules_r2_045, cut_in_merge_2hz_rules_r2_046)
- Moving the timing in scene 09a95ffa to -0.5 s or +1.0 s gave no failure in a single run each, which hints that the failures are confined to a narrow timing window. A single run cannot rule them out.
  - S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r2_036)
  - S8: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r2_054)
- Scene 19f339ba at 0 s and 1.25x speed fails sometimes but not reliably. Both failures came from the slow-moving ego drifting about 1.7 m left over the lane line, against a RIGHT command, into a car passing on its left: a policy fault.
  - S12: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_r2_006, cut_in_merge_2hz_rules_r2_011, cut_in_merge_2hz_rules_r2_021, cut_in_merge_2hz_rules_r2_029, cut_in_merge_2hz_rules_r2_038, cut_in_merge_2hz_rules_r2_048)
- Across the scenes, the most common at-fault failure is the policy drifting left out of its lane into a car alongside, even at 2 Hz planning.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_r2_004, cut_in_merge_2hz_rules_r2_010, cut_in_merge_2hz_rules_r2_019)
  - S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_rules_r2_045, cut_in_merge_2hz_rules_r2_046)
  - S12: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_r2_006, cut_in_merge_2hz_rules_r2_011, cut_in_merge_2hz_rules_r2_021, cut_in_merge_2hz_rules_r2_029, cut_in_merge_2hz_rules_r2_038, cut_in_merge_2hz_rules_r2_048)
- Several scenes looked safe at 1.25x speed and the recorded timing (or -0.5 s for 054b5901): no repeat failed. This holds even for scenes that came within 0.0 m to 0.26 m at baseline (096988dd, 12855a41, 054b5901).
  - S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_r2_018, cut_in_merge_2hz_rules_r2_024, cut_in_merge_2hz_rules_r2_032, cut_in_merge_2hz_rules_r2_041, cut_in_merge_2hz_rules_r2_051)
  - S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_005, cut_in_merge_2hz_rules_r2_015, cut_in_merge_2hz_rules_r2_026, cut_in_merge_2hz_rules_r2_033, cut_in_merge_2hz_rules_r2_043, cut_in_merge_2hz_rules_r2_052)
  - S9: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_001, cut_in_merge_2hz_rules_r2_016, cut_in_merge_2hz_rules_r2_027, cut_in_merge_2hz_rules_r2_035, cut_in_merge_2hz_rules_r2_044, cut_in_merge_2hz_rules_r2_053)
  - S10: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_009, cut_in_merge_2hz_rules_r2_014, cut_in_merge_2hz_rules_r2_023, cut_in_merge_2hz_rules_r2_031, cut_in_merge_2hz_rules_r2_040, cut_in_merge_2hz_rules_r2_050)
  - S11: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_002, cut_in_merge_2hz_rules_r2_013, cut_in_merge_2hz_rules_r2_022, cut_in_merge_2hz_rules_r2_030, cut_in_merge_2hz_rules_r2_039, cut_in_merge_2hz_rules_r2_047)
  - S13: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_003, cut_in_merge_2hz_rules_r2_017, cut_in_merge_2hz_rules_r2_025, cut_in_merge_2hz_rules_r2_034, cut_in_merge_2hz_rules_r2_042, cut_in_merge_2hz_rules_r2_049)

## Open

- Whether scene 09a95ffa is a confirmed case: more repeats at +0.5 s / 1.25x (S7) and at 0 s / 1.25x (S6) would settle it, along with a check on whether the actor-33 cut-ins should count against the policy.
- Whether scene 19f339ba fails reliably at any setting: S12 sits around one third, so nearby timings (±0.5 s) or higher speeds would need to be probed.
- The rest of the knob space went untested: speeds other than 1.25x (0.5x to 2x) and shifts beyond ±1 s. Without them the study cannot answer which timings and speeds cause collisions, and three more distinct scenes are needed to reach the 5 cases.
- How these results compare with the 10 Hz study cut_in_merge, which the brief asks for. Its results are not in this input, so this report cannot say whether 2 Hz planning changes which scenes fail.

## Why the runs failed (triage from the video and log)

actor_hit_ego 6, turned_into_actor 5

- cut_in_merge_2hz_rules_r2_004: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the ego sped up from 4.4 to 6.4 m/s and drifted left over the lane line, about 1.5 m off the recorded path. Its front hit actor 56, which was travelling just ahead in the adjacent left lane. A rear contact was also recorded, but the at-fault front collision began first, caused by the ego's own lateral drift.
- cut_in_merge_2hz_rules_r2_006: turned_into_actor, policy at fault: yes. The ego was moving very slowly (about 4 m/s) on a multi-lane highway, straddling a lane line about 1.7 m off the human path, and its planned path wobbled to the left even though the command was RIGHT. Actor 25 came up from behind in the left lane, and at 12.1 s it is overlapping the ego's front-left corner. The ego drifted into the lane the actor was using to pass, so the contact is a front/side hit, not a rear-end.
- cut_in_merge_2hz_rules_r2_010: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane, speeding up from 4.4 to 6.3 m/s, and ended up about 3 m ahead of where the human was in the recording. Actor 56, in the adjacent left lane just ahead of the ego, angled right into the ego's lane and the two overlapped at the ego's front-left corner (the gap fell from 21 m to 2.7 m in the last half-second). The ego never moved toward actor 56, but it might have avoided the merge if it had matched the human's slower pace or braked.
- cut_in_merge_2hz_rules_r2_012: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane at a steady 8 m/s, close to the recorded path (0.9 m off). Actor 33 came up fast from behind in the lane to the left and moved over across the lane line into the ego's front-left corner, which the metrics count as a front collision. The ego did not brake or move away, but the cut-in came from behind and to the side with almost no warning.
- cut_in_merge_2hz_rules_r2_019: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT, the policy planned a lane change to the left and steered into the adjacent lane. Vehicle 56 was already alongside and slightly ahead there, and at about 6.4 m/s the ego's front corner hit it.
- cut_in_merge_2hz_rules_r2_020: actor_hit_ego, policy at fault: unclear. The ego was cruising straight at about 8 m/s on a multi-lane highway. Actor 33 overtook it from the left-rear and cut in across the ego's front-left corner around 6.1–6.6 s; the gap ahead drops from 30 m to 25 m as it enters. The contact registers as a front collision, but the ego's own path barely changed (0.9 m off the recording), so it looks like the replayed actor sideswiped the ego rather than the policy steering into it.
- cut_in_merge_2hz_rules_r2_028: actor_hit_ego, policy at fault: no. The ego was cruising straight in its lane at about 8 m/s on a multi-lane highway, staying within about 0.9 m of the recorded path. Actor 33 came up from behind in the lane to the left and moved over into the ego's lane, overlapping the ego's front-left corner. That registered as a front collision, even though the vehicle ahead was more than 25 m away the whole time.
- cut_in_merge_2hz_rules_r2_037: actor_hit_ego, policy at fault: unclear. On a multi-lane highway, the ego was going straight at about 8 m/s with clear road ahead (gap about 26 m). Actor 33 came up fast from behind in the lane to the left and passed close to the ego. By 6.6 s it was angled across the ego's front-left corner, which registered as a front collision. The ego was only about 0.9 m left of the recorded human path. That small leftward offset may have turned a close pass in the recording into contact.
- cut_in_merge_2hz_rules_r2_045: turned_into_actor, policy at fault: yes. On a straight multi-lane highway at about 8 m/s, the policy steered left away from its lane, about 1.9 m off the recorded path. It moved into the adjacent left lane and hit vehicle 32, which was passing alongside on the left. The ego never braked, and the 0.5 m gap appeared only once it entered that lane; the camera smear shows up only at the moment of impact.
- cut_in_merge_2hz_rules_r2_046: actor_hit_ego, policy at fault: unclear. On a multi-lane freeway, the ego held its lane at about 8 m/s while the recorded human drifted right; the command turned RIGHT only at the end. Actor 33, a log-replayed car coming up from behind-left, merged into the space the human had left and ran into the ego's left-rear and side, about 2 m from where the recording had the ego. The collision was scored as front/at-fault even though the ego never closed on anything ahead.
- cut_in_merge_2hz_rules_r2_048: turned_into_actor, policy at fault: yes. The ego was creeping along a multi-lane highway at only about 4 m/s. Although the command was RIGHT, it drifted about 1.7 m left of the recorded path until it was straddling the lane line on its left. At 12.1s actor 25, passing in the lane to the left, side-swiped the ego (a side collision).

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_r2_004, cut_in_merge_2hz_rules_r2_010, cut_in_merge_2hz_rules_r2_019)
- S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_r2_018, cut_in_merge_2hz_rules_r2_024, cut_in_merge_2hz_rules_r2_032, cut_in_merge_2hz_rules_r2_041, cut_in_merge_2hz_rules_r2_051)
- S3: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r2_008)
- S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_005, cut_in_merge_2hz_rules_r2_015, cut_in_merge_2hz_rules_r2_026, cut_in_merge_2hz_rules_r2_033, cut_in_merge_2hz_rules_r2_043, cut_in_merge_2hz_rules_r2_052)
- S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r2_036)
- S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 4/5 failed, rate 44%-95% (90%) (cut_in_merge_2hz_rules_r2_007, cut_in_merge_2hz_rules_r2_012, cut_in_merge_2hz_rules_r2_020, cut_in_merge_2hz_rules_r2_028, cut_in_merge_2hz_rules_r2_037)
- S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_rules_r2_045, cut_in_merge_2hz_rules_r2_046)
- S8: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r2_054)
- S9: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_001, cut_in_merge_2hz_rules_r2_016, cut_in_merge_2hz_rules_r2_027, cut_in_merge_2hz_rules_r2_035, cut_in_merge_2hz_rules_r2_044, cut_in_merge_2hz_rules_r2_053)
- S10: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_009, cut_in_merge_2hz_rules_r2_014, cut_in_merge_2hz_rules_r2_023, cut_in_merge_2hz_rules_r2_031, cut_in_merge_2hz_rules_r2_040, cut_in_merge_2hz_rules_r2_050)
- S11: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_002, cut_in_merge_2hz_rules_r2_013, cut_in_merge_2hz_rules_r2_022, cut_in_merge_2hz_rules_r2_030, cut_in_merge_2hz_rules_r2_039, cut_in_merge_2hz_rules_r2_047)
- S12: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_r2_006, cut_in_merge_2hz_rules_r2_011, cut_in_merge_2hz_rules_r2_021, cut_in_merge_2hz_rules_r2_029, cut_in_merge_2hz_rules_r2_038, cut_in_merge_2hz_rules_r2_048)
- S13: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r2_003, cut_in_merge_2hz_rules_r2_017, cut_in_merge_2hz_rules_r2_025, cut_in_merge_2hz_rules_r2_034, cut_in_merge_2hz_rules_r2_042, cut_in_merge_2hz_rules_r2_049)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 19 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
