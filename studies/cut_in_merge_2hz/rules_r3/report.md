# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

Only one of the five cases was confirmed, so the goal was not met. Scene 023b7fcc with the cars at recorded timing and 1.25x speed failed every run, and its range sits above one half (S1). The best second candidate is scene 09a95ffa with the cars 0.5 s later at 1.25x. Every run there failed, but there were only two runs, so its range still reaches below one half (S7). Every policy-caused failure in this study had the same cause: the ego drifted left into a car travelling alongside in the next lane, even though the route command was STRAIGHT or RIGHT. None was a missed brake for a car cutting in. On the other seven scenes, cars at recorded timing and 1.25x speed caused no failures. The search also tried almost nothing else: every setting ran at 1.25x speed, with time shifts only from -0.5 s to +1.0 s. So most of the timing and speed range is still unexplored, and the study cannot say which timings and speeds are dangerous in general.

## Findings

- Scene 023b7fcc at 0 s shift and 1.25x speed is a confirmed challenging case. Every run failed, and its range is above one half. In each run the policy steered left out of its lane against a STRAIGHT/RIGHT command and hit the front-left of actor 56 in the next lane. The policy was at fault every time, and no failure was flagged as a possible rendering artifact.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_r3_004, cut_in_merge_2hz_rules_r3_010, cut_in_merge_2hz_rules_r3_019)
- Scene 09a95ffa at +0.5 s shift and 1.25x speed failed every run, the same way: the ego drifted left into actor 33 coming up alongside. With only two runs this is a strong hint, not a confirmed rate.
  - S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_rules_r3_045, cut_in_merge_2hz_rules_r3_046)
- On scene 09a95ffa at 0 s shift and 1.25x speed, the failures were mixed and mostly not the policy's fault. One was the policy drifting left into actor 33. In the other two, the ego held its lane and actor 33 overtook fast and cut across into the ego's front-left corner. This setting does not show a policy weakness the way S7 does.
  - S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/5 failed, rate 27%-86% (90%) (cut_in_merge_2hz_rules_r3_007, cut_in_merge_2hz_rules_r3_011, cut_in_merge_2hz_rules_r3_020, cut_in_merge_2hz_rules_r3_028, cut_in_merge_2hz_rules_r3_037)
- On scene 09a95ffa, the single runs at -0.5 s and +1.0 s shift (1.25x speed) did not fail. These are single runs and say little.
  - S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_036)
  - S8: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_054)
- Cars at recorded timing and 1.25x speed caused no failure on scenes 096988dd, 0cf6368d, 0e899dd3, 12855a41, 19f339ba and 1c45ce3a. Each range stays below one half, so these settings look safe. That says nothing about other timings or speeds on these scenes.
  - S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_005, cut_in_merge_2hz_rules_r3_012, cut_in_merge_2hz_rules_r3_023, cut_in_merge_2hz_rules_r3_031, cut_in_merge_2hz_rules_r3_040, cut_in_merge_2hz_rules_r3_049)
  - S9: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_001, cut_in_merge_2hz_rules_r3_016, cut_in_merge_2hz_rules_r3_027, cut_in_merge_2hz_rules_r3_034, cut_in_merge_2hz_rules_r3_044, cut_in_merge_2hz_rules_r3_053)
  - S10: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_009, cut_in_merge_2hz_rules_r3_015, cut_in_merge_2hz_rules_r3_024, cut_in_merge_2hz_rules_r3_032, cut_in_merge_2hz_rules_r3_041, cut_in_merge_2hz_rules_r3_050)
  - S11: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_002, cut_in_merge_2hz_rules_r3_014, cut_in_merge_2hz_rules_r3_022, cut_in_merge_2hz_rules_r3_030, cut_in_merge_2hz_rules_r3_039, cut_in_merge_2hz_rules_r3_048)
  - S12: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_006, cut_in_merge_2hz_rules_r3_013, cut_in_merge_2hz_rules_r3_021, cut_in_merge_2hz_rules_r3_029, cut_in_merge_2hz_rules_r3_038, cut_in_merge_2hz_rules_r3_047)
  - S13: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_003, cut_in_merge_2hz_rules_r3_017, cut_in_merge_2hz_rules_r3_026, cut_in_merge_2hz_rules_r3_035, cut_in_merge_2hz_rules_r3_043, cut_in_merge_2hz_rules_r3_052)
- Scene 054b5901 did not fail at -0.5 s or 0 s shift with 1.25x speed. The -0.5 s setting had enough runs to look safe; the 0 s setting had a single run.
  - S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_r3_018, cut_in_merge_2hz_rules_r3_025, cut_in_merge_2hz_rules_r3_033, cut_in_merge_2hz_rules_r3_042, cut_in_merge_2hz_rules_r3_051)
  - S3: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_008)

## Open

- Is scene 09a95ffa at +0.5 s, 1.25x reliably failing? Two or three more runs at S7 would settle whether it becomes the second confirmed case.
- Speed was never varied from 1.25x, and time shifts never went beyond -0.5 s to +1.0 s. Single-run probes at 0.5x, 1.5x and 2x, and at ±1.5 s and ±2 s, on the scenes that look safe (096988dd, 12855a41, 19f339ba, 054b5901, 0e899dd3, 0cf6368d, 1c45ce3a) are needed before the study can say which timings and speeds are dangerous, or fill the remaining top-5 slots.
- Every policy-caused failure was a left drift into a car alongside, not a reaction to a cut-in. Is that a reaction to the retimed cars, or the drift the planning-rate note describes? Running 023b7fcc and 09a95ffa at the recorded speed (1.0x, 0 s) would show it.
- The study cannot say whether 2 Hz planning fails less often than 10 Hz. That would need these exact settings set side by side with the same settings in the 10 Hz cut_in_merge study.
- The tags do not say whether the ego merges or another car cuts in, so the two kinds of scene cannot be told apart here.

## Why the runs failed (triage from the video and log)

turned_into_actor 6, actor_hit_ego 2

- cut_in_merge_2hz_rules_r3_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (RIGHT in the last frame), the policy steered left out of its lane, away from the recorded path, and moved into the adjacent left lane. Its front-left hit vehicle 56, which was traveling alongside in that lane, while the ego sped up from 4.4 to 6.4 m/s.
- cut_in_merge_2hz_rules_r3_010: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy drifted left out of its lane toward actor 56, which was travelling alongside in the next lane to the left. It did this even though the route command was STRAIGHT and then RIGHT, and the recorded path went the other way, to the right. Speeding up from 4.4 to 6.5 m/s, the ego hit 56 with its front corner at 7.2s; the rear contact flagged in the run came after this.
- cut_in_merge_2hz_rules_r3_011: turned_into_actor, policy at fault: yes. After handoff, the policy's plan (orange) steered the ego left out of its lane while the recorded path stayed straight. Actor 33 was overtaking in the left lane, and at 6.6 s the ego's front hit it at about 8.4 m/s. The lead vehicle was more than 25 m ahead the whole time, so following distance played no part.
- cut_in_merge_2hz_rules_r3_019: turned_into_actor, policy at fault: yes. After handoff, the ego sped up from 4.4 to 6.6 m/s and its plan (the orange line) veered left into the adjacent lane. It moved about 1.5 m left of the recorded path and its front-left hit actor 56, which was driving in that lane right beside and slightly ahead of it. The route command was STRAIGHT and then RIGHT, so nothing called for a move left; the later rear contact came after this front collision.
- cut_in_merge_2hz_rules_r3_020: actor_hit_ego, policy at fault: no. On the highway, the ego held its lane at a steady ~8 m/s with a big gap (~26 m) to the car ahead. Actor 33 came up fast from behind in the left lane, drew level and drifted right over the lane line into the ego's front-left corner at 6.6 s. The camera smear on the left of the last frame is the contact itself, not the cause.
- cut_in_merge_2hz_rules_r3_037: actor_hit_ego, policy at fault: no. The ego was cruising straight in its lane at about 8 m/s. Actor 33 came up fast from behind in the left lane, passed the ego within about a second and cut across into the ego's lane, so the ego's front-left corner clipped its right rear at 6.6 s. The ego stayed in its lane (0.85 m off the recorded path) and had little chance to react to the fast cut-in. The camera smear at impact is just the actor being close.
- cut_in_merge_2hz_rules_r3_045: turned_into_actor, policy at fault: yes. After handoff, at about 8 m/s on a multi-lane freeway, the ego slowly drifted left off the recorded path (1.8 m off by 7.1 s) and into the next lane on the left, even though the route command was STRAIGHT and then RIGHT. There it ran into actor 33, which was coming up alongside in that lane.
- cut_in_merge_2hz_rules_r3_046: turned_into_actor, policy at fault: yes. With the command STRAIGHT on a multi-lane freeway, the policy planned and drove a drift into the left lane at about 8 m/s while the human stayed in its lane. Vehicle 33 was coming up alongside in that lane, and the ego hit it with its front-left (about 1.9 m off the recorded path).

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_r3_004, cut_in_merge_2hz_rules_r3_010, cut_in_merge_2hz_rules_r3_019)
- S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_r3_018, cut_in_merge_2hz_rules_r3_025, cut_in_merge_2hz_rules_r3_033, cut_in_merge_2hz_rules_r3_042, cut_in_merge_2hz_rules_r3_051)
- S3: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_008)
- S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_005, cut_in_merge_2hz_rules_r3_012, cut_in_merge_2hz_rules_r3_023, cut_in_merge_2hz_rules_r3_031, cut_in_merge_2hz_rules_r3_040, cut_in_merge_2hz_rules_r3_049)
- S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_036)
- S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/5 failed, rate 27%-86% (90%) (cut_in_merge_2hz_rules_r3_007, cut_in_merge_2hz_rules_r3_011, cut_in_merge_2hz_rules_r3_020, cut_in_merge_2hz_rules_r3_028, cut_in_merge_2hz_rules_r3_037)
- S7: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_rules_r3_045, cut_in_merge_2hz_rules_r3_046)
- S8: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_r3_054)
- S9: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_001, cut_in_merge_2hz_rules_r3_016, cut_in_merge_2hz_rules_r3_027, cut_in_merge_2hz_rules_r3_034, cut_in_merge_2hz_rules_r3_044, cut_in_merge_2hz_rules_r3_053)
- S10: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_009, cut_in_merge_2hz_rules_r3_015, cut_in_merge_2hz_rules_r3_024, cut_in_merge_2hz_rules_r3_032, cut_in_merge_2hz_rules_r3_041, cut_in_merge_2hz_rules_r3_050)
- S11: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_002, cut_in_merge_2hz_rules_r3_014, cut_in_merge_2hz_rules_r3_022, cut_in_merge_2hz_rules_r3_030, cut_in_merge_2hz_rules_r3_039, cut_in_merge_2hz_rules_r3_048)
- S12: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_006, cut_in_merge_2hz_rules_r3_013, cut_in_merge_2hz_rules_r3_021, cut_in_merge_2hz_rules_r3_029, cut_in_merge_2hz_rules_r3_038, cut_in_merge_2hz_rules_r3_047)
- S13: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_r3_003, cut_in_merge_2hz_rules_r3_017, cut_in_merge_2hz_rules_r3_026, cut_in_merge_2hz_rules_r3_035, cut_in_merge_2hz_rules_r3_043, cut_in_merge_2hz_rules_r3_052)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
