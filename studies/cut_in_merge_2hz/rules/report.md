# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules`: 53 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: the study confirmed 2 of the 5 cases it was asked to find. Both are at the same setting, with recorded timing (0 s shift) and cars at 1.25x speed. On 023b7fcc (S1) every run failed because the policy drifted left into a car in the next lane, so the policy was at fault. On 09a95ffa (S5) every run also failed, but each time a car came up from behind-left and cut into the ego's front-left corner while the ego held near its recorded path. Triage judged the policy not at fault or unclear in those S5 runs, so S5 shows a cut-in the policy did not avoid more than an error by the policy. Both cases rest on only a few repeats, so their failure-rate ranges are wide, though they stay above one half. Nearly every setting kept the 1.25x speed and 0 s shift, so the study cannot say which timings or speeds cause the failures. Neither failing scene was run at 1.0x, so it is not even shown that the retiming caused them.

## Findings

- On 023b7fcc at 0 s shift and 1.25x speed, every run failed with a front-left collision. The policy steered left off the recorded path (going STRAIGHT) into actor 56 in the adjacent lane, and triage put the policy at fault every time. Planning at 2 Hz did not stop this left drift.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_004, cut_in_merge_2hz_rules_010, cut_in_merge_2hz_rules_019)
- On 09a95ffa at 0 s shift and 1.25x speed, every run failed when actor 33 came from behind-left and cut into the ego's front-left corner. The ego stayed within about 0.9 m of the recorded path and did not react to the cut-in. Triage judged the policy not at fault or unclear in each run, so this confirmed case may say more about the replayed cut-in than about the policy.
  - S5: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_007, cut_in_merge_2hz_rules_011, cut_in_merge_2hz_rules_020)
- On 19f339ba only one setting produced a failure: a 1.0 s earlier shift at 1.25x speed, with one failed run among a few. The ego was drifting left at low speed when a small, fast actor (possibly a motorcycle) appeared at its front-left, and fault is unclear. Nearby settings on this scene (-2.0 s, -1.5 s, -0.5 s and 0 s shifts at 1.25x, and -1.0 s at 1.0x) did not fail, so this is a hint, not a confirmed case.
  - S15: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_027, cut_in_merge_2hz_rules_029, cut_in_merge_2hz_rules_046)
  - S12: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_044)
  - S13: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_036, cut_in_merge_2hz_rules_037)
  - S14: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_053)
  - S16: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_018)
  - S17: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_006)
- Five scenes look safe at 0 s shift and 1.25x speed: 096988dd, 0cf6368d, 0e899dd3, 12855a41 and 1c45ce3a. None of their repeated runs failed, and their ranges stay below one half. This includes 12855a41 and 096988dd, which came close at baseline. 054b5901 at -0.5 s shift and 1.25x was also repeated without a failure.
  - S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_005, cut_in_merge_2hz_rules_014, cut_in_merge_2hz_rules_023, cut_in_merge_2hz_rules_033, cut_in_merge_2hz_rules_042, cut_in_merge_2hz_rules_051)
  - S6: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_001, cut_in_merge_2hz_rules_016, cut_in_merge_2hz_rules_026, cut_in_merge_2hz_rules_034, cut_in_merge_2hz_rules_043, cut_in_merge_2hz_rules_052)
  - S7: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_009, cut_in_merge_2hz_rules_013, cut_in_merge_2hz_rules_022, cut_in_merge_2hz_rules_031, cut_in_merge_2hz_rules_040, cut_in_merge_2hz_rules_049)
  - S10: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_002, cut_in_merge_2hz_rules_012, cut_in_merge_2hz_rules_021, cut_in_merge_2hz_rules_028, cut_in_merge_2hz_rules_038, cut_in_merge_2hz_rules_047)
  - S18: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_003, cut_in_merge_2hz_rules_015, cut_in_merge_2hz_rules_025, cut_in_merge_2hz_rules_030, cut_in_merge_2hz_rules_048)
  - S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_017, cut_in_merge_2hz_rules_024, cut_in_merge_2hz_rules_032, cut_in_merge_2hz_rules_041, cut_in_merge_2hz_rules_050)
- Single runs on 12855a41 at -0.5 s and +0.5 s shift (1.25x) and at 1.0x speed, and on 054b5901 at 0 s shift (1.25x), passed. One run each cannot rule these settings out.
  - S8: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_035)
  - S9: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_054)
  - S11: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_045)
  - S3: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_008)

## Open

- Whether retiming causes the two confirmed failures at all: S1 (023b7fcc) and S5 (09a95ffa) were never run at 1.0x speed and 0 s shift. A few repeats there would show whether these scenes fail as recorded under replay traffic.
- Which timings and speeds matter: the search stayed almost entirely at 1.25x speed and 0 s shift. The 0.5x and 2x speeds and shifts of ±1 to ±2 s were barely tried or not tried at all. A sweep over these on 023b7fcc, 09a95ffa and 19f339ba would answer the question as asked.
- Whether 19f339ba at -1.0 s and 1.25x (S15) is a real case: about four more repeats would confirm or drop it, and a review of the motorcycle actor would settle fault.
- Whether S5 counts as a policy failure: a review of the 09a95ffa videos would show whether a reasonable driver could have braked or yielded before actor 33's cut-in.
- Three more confirmed scenes are still needed to reach five. The scenes that look safe at 1.25x/0 s (096988dd, 0cf6368d, 0e899dd3, 12855a41, 1c45ce3a, 054b5901) were never tried at the extreme speeds or shifts.
- 1c45ce3a lost runs to the gate (re-run, then halted). Those runs are not evidence, and the harness issue behind them is unresolved.
- How this compares with the 10 Hz cut_in_merge study is not settled here: a side-by-side of the same scenes and settings is needed, especially 023b7fcc, where left drift still caused failures at 2 Hz.

## Why the runs failed (triage from the video and log)

turned_into_actor 4, actor_hit_ego 3

- cut_in_merge_2hz_rules_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy steered left away from the recorded path, toward the adjacent lane behind actor 15. Actor 56 was traveling alongside in that left lane, and the ego's front left corner hit it at 7.2s.
- cut_in_merge_2hz_rules_007: actor_hit_ego, policy at fault: unclear. The ego was cruising straight at about 8 m/s with a clear lane ahead (gap of about 26 m). Actor 33 came up quickly from behind-left in the adjacent lane and closed in on the ego's left side, and at 6.6 s their boxes overlap at the ego's front-left corner. The ego was within 0.9 m of the recorded human path, so the replayed actor seems to have squeezed into the ego rather than the ego steering into it; the smeared car in the camera only appears at the moment of contact.
- cut_in_merge_2hz_rules_010: turned_into_actor, policy at fault: yes. After handoff, the ego sped up from about 4.4 to 6.4 m/s and drifted left toward the adjacent left lane, roughly following the recorded human's lane change. While doing so, its front-left hit the rear-right of actor 56, which was just ahead in that lane, at 7.2 s; the rear contact flagged in the run came after this front collision.
- cut_in_merge_2hz_rules_011: actor_hit_ego, policy at fault: unclear. On the multi-lane highway the ego held its lane at about 8 m/s. Actor 33 came up from behind-left in the adjacent lane, passed the ego and cut right into its lane. By 6.6 s it overlapped the ego's front-left corner, which registered as a front collision. The ego was only 0.9 m off the recorded path and the lead car in its own lane was about 26 m ahead, so this looks like a replayed actor merging into the ego rather than the ego steering into it. Still, the small offset and the fact that the ego didn't react to the cut-in leave some doubt about fault.
- cut_in_merge_2hz_rules_019: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT and then RIGHT, the policy planned a drift to the left (orange path) away from the recorded path. It sped up from 4.4 to 6.5 m/s and steered into the left lane, and its front hit actor 56, which was travelling alongside and slightly ahead in that lane. The rear contact is also flagged, but it came after this front collision.
- cut_in_merge_2hz_rules_020: actor_hit_ego, policy at fault: no. The ego was cruising straight in its lane on a multi-lane freeway at a steady 8 m/s, with a clear gap of over 25 m to the car ahead. Actor 33 came up from behind in the lane to the left, passed the ego, and cut across the lane line into the ego's front-left corner, so the impact counted as a front collision.
- cut_in_merge_2hz_rules_046: turned_into_actor, policy at fault: unclear. The ego was going straight on a multi-lane highway at only about 4–5 m/s, and its planned path kept bending left toward the next lane. At 12.1 s a small actor (29, maybe a motorcycle) suddenly shows up right at the ego's front-left. It was not on the map a second earlier, so it probably came up fast from behind, and the ego's leftward drift brought them into a front collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_004, cut_in_merge_2hz_rules_010, cut_in_merge_2hz_rules_019)
- S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_017, cut_in_merge_2hz_rules_024, cut_in_merge_2hz_rules_032, cut_in_merge_2hz_rules_041, cut_in_merge_2hz_rules_050)
- S3: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_008)
- S4: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_005, cut_in_merge_2hz_rules_014, cut_in_merge_2hz_rules_023, cut_in_merge_2hz_rules_033, cut_in_merge_2hz_rules_042, cut_in_merge_2hz_rules_051)
- S5: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_rules_007, cut_in_merge_2hz_rules_011, cut_in_merge_2hz_rules_020)
- S6: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_001, cut_in_merge_2hz_rules_016, cut_in_merge_2hz_rules_026, cut_in_merge_2hz_rules_034, cut_in_merge_2hz_rules_043, cut_in_merge_2hz_rules_052)
- S7: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_009, cut_in_merge_2hz_rules_013, cut_in_merge_2hz_rules_022, cut_in_merge_2hz_rules_031, cut_in_merge_2hz_rules_040, cut_in_merge_2hz_rules_049)
- S8: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_035)
- S9: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_054)
- S10: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_rules_002, cut_in_merge_2hz_rules_012, cut_in_merge_2hz_rules_021, cut_in_merge_2hz_rules_028, cut_in_merge_2hz_rules_038, cut_in_merge_2hz_rules_047)
- S11: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_045)
- S12: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_044)
- S13: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_036, cut_in_merge_2hz_rules_037)
- S14: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_053)
- S15: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_027, cut_in_merge_2hz_rules_029, cut_in_merge_2hz_rules_046)
- S16: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_018)
- S17: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_006)
- S18: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_rules_003, cut_in_merge_2hz_rules_015, cut_in_merge_2hz_rules_025, cut_in_merge_2hz_rules_030, cut_in_merge_2hz_rules_048)

## Not kept by the gate

- cut_in_merge_2hz_rules_039: not kept: RE-RUN
- cut_in_merge_2hz_rules_039_a2: not kept: RE-RUN
- cut_in_merge_2hz_rules_039_a3: not kept: HALT

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

56 of 56 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
