# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `random_confirm_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

At 2 Hz planning the study confirmed only one of the five challenging settings it was looking for, so the goal was not met. The confirmed setting is on scene 09a95ffa, with the cars shifted 1.5 s earlier at recorded speed (1.0x). Every repeat there failed, but its range only just clears one half. One of those failures was a car cutting in from the ego's rear quarter, which was not the policy's fault. The other two were the policy drifting left into a car passing in the next lane. No other scene failed at any setting tried. At most settings there was only one run, so a pass there is a hint, not evidence that the setting is safe. The study can't say whether the other eight scenes have no failing timing or the search just didn't find one.

## Findings

- The one confirmed challenging setting is scene 09a95ffa with the cars 1.5 s earlier at 1.0x speed. Every repeat failed, and the failure rate is surely above one half.
  - S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_r3_018, cut_in_merge_2hz_random_confirm_r3_019, cut_in_merge_2hz_random_confirm_r3_028)
- The policy caused only some of the failures at that setting. In two runs the planned path bent left on a STRAIGHT command and the ego hit the car passing alongside, so the left drift is still there at 2 Hz. In the third run that car cut in from behind on the left and hit the ego, which was not the policy's fault. Without that run the policy-caused failures alone would probably not clear the bar.
  - S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_r3_018, cut_in_merge_2hz_random_confirm_r3_019, cut_in_merge_2hz_random_confirm_r3_028)
- On the same scene, cars 1.5 s earlier at 2.0x speed failed in its only run: the ego stayed a lane left of its route and did not brake for a slower car ahead. The run was flagged as a possible simulator artifact, but triage found the car clearly visible, so rendering does not explain it. A single run is a hint, not a rate.
  - S13: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_2hz_random_confirm_r3_034)
- On scene 09a95ffa, slowing the cars to 0.75x made no run fail, whether shifted 1.5 s or 2 s earlier. This hints that the failure there depends on the cars' speed as well as their timing.
  - S10: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_006, cut_in_merge_2hz_random_confirm_r3_011)
  - S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_052)
  - S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_r3_018, cut_in_merge_2hz_random_confirm_r3_019, cut_in_merge_2hz_random_confirm_r3_028)
- Several settings were repeated enough to look safe, with failure rates surely below one half: 19f339ba at +0.5 s and 1.5x, 1c45ce3a at -2 s and 1.0x, 0e899dd3 at 0 s and 0.5x, and 12855a41 at -2 s and 0.75x and at +2 s and 2.0x.
  - S29: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_random_confirm_r3_005, cut_in_merge_2hz_random_confirm_r3_010, cut_in_merge_2hz_random_confirm_r3_020, cut_in_merge_2hz_random_confirm_r3_029, cut_in_merge_2hz_random_confirm_r3_038, cut_in_merge_2hz_random_confirm_r3_047)
  - S30: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_r3_016, cut_in_merge_2hz_random_confirm_r3_021, cut_in_merge_2hz_random_confirm_r3_030, cut_in_merge_2hz_random_confirm_r3_039)
  - S22: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_026, cut_in_merge_2hz_random_confirm_r3_031, cut_in_merge_2hz_random_confirm_r3_040)
  - S23: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_008, cut_in_merge_2hz_random_confirm_r3_013, cut_in_merge_2hz_random_confirm_r3_022)
  - S28: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_032, cut_in_merge_2hz_random_confirm_r3_037, cut_in_merge_2hz_random_confirm_r3_048)
- No run failed on scenes 023b7fcc, 054b5901, 096988dd, 0cf6368d, 0e899dd3, 12855a41, 19f339ba or 1c45ce3a. Most of their settings had a single run, which cannot rule out a failure rate above one half.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_033)
  - S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_042, cut_in_merge_2hz_random_confirm_r3_049)
  - S3: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_050)
  - S4: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_001)
  - S5: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_009)
  - S6: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_017)
  - S7: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_051)
  - S8: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_053)
  - S9: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_002, cut_in_merge_2hz_random_confirm_r3_012)
  - S14: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_025)
  - S15: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_014)
  - S16: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_027)
  - S17: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_045)
  - S18: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_007)
  - S19: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_023)
  - S20: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_041)
  - S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_043, cut_in_merge_2hz_random_confirm_r3_046)
  - S24: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_015)
  - S25: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_054)
  - S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_024)
  - S27: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_036)
  - S31: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_044)
  - S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_035)
  - S33: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_003)
  - S34: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_004)

## Open

- Four of the five cases are still missing. The closest calls on other scenes are worth repeating and probing nearby: 0e899dd3 at -1 s and 1.25x, 023b7fcc at +0.5 s and 0.5x, 12855a41 at 0 s and 0.5x, and 1c45ce3a at -1 s and 1.5x (S21, S2, S25, S31). They need repeats and neighbouring settings, beyond this budget.
- The S12 confirmation includes one failure that was not the policy's fault. More repeats at 09a95ffa, -1.5 s and 1.0x would show whether the policy's own left-drift failures alone stay above one half.
- Whether the 2.0x failure on 09a95ffa (S13) repeats or was a one-off: it needs about three more runs.
- Comparing with the 10 Hz study cut_in_merge needs that study's results side by side. This study alone cannot show whether 2 Hz planning reduces failures, though left drift still caused collisions here.
- The tags cannot tell ego merges apart from other cars cutting in. Six scenes retime every car at once, so the study cannot isolate which car's timing matters.

## Why the runs failed (triage from the video and log)

turned_into_actor 2, actor_hit_ego 1, no_brake_for_lead 1

- cut_in_merge_2hz_random_confirm_r3_018: actor_hit_ego, policy at fault: no. The ego was cruising straight at about 8 m/s in its lane on a multi-lane highway. Actor 33 came up fast from behind on the left and cut right into the ego's lane, hitting the ego's front-left corner; the gap to the actor ahead fell from 25 m to 2.6 m because actor 33 was suddenly beside and ahead of the ego. The ego was only 1.3 m from the recorded human path and had little chance to avoid a vehicle merging in from its rear quarter.
- cut_in_merge_2hz_random_confirm_r3_019: turned_into_actor, policy at fault: yes. On a straight multi-lane freeway at about 8 m/s, the ego's planned path (orange) bent left toward the next lane while actor 33 was passing in that lane on its left. The ego moved about 1.3 m left of the recorded path and its front-left corner hit 33 alongside it; there was no lead-vehicle closing beforehand (the gap held steady at 25–30 m).
- cut_in_merge_2hz_random_confirm_r3_028: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a STRAIGHT command, the policy's planned path (orange) bent left toward the next lane while the recorded route stayed in the ego's lane. The ego drifted left at about 8 m/s into actor 33, which was driving alongside in that lane, and hit it with its front-left (front collision at 6.6 s).
- cut_in_merge_2hz_random_confirm_r3_034: no_brake_for_lead, policy at fault: yes. The route command was RIGHT, but after handoff the ego stayed about one lane left of the recorded path and followed slower vehicle 87 in that lane. The gap to 87 shrank from 13 m to 4 m while the ego only eased from 6.7 to 5.4 m/s, and it hit 87's rear with its front at 10.1 s. 87 was smeared in the camera view but clearly shown, so rendering does not explain the failure to brake.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_033)
- S2: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_042, cut_in_merge_2hz_random_confirm_r3_049)
- S3: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_050)
- S4: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_001)
- S5: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_009)
- S6: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_017)
- S7: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_051)
- S8: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_053)
- S9: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_002, cut_in_merge_2hz_random_confirm_r3_012)
- S10: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_006, cut_in_merge_2hz_random_confirm_r3_011)
- S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_052)
- S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_r3_018, cut_in_merge_2hz_random_confirm_r3_019, cut_in_merge_2hz_random_confirm_r3_028)
- S13: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_2hz_random_confirm_r3_034)
- S14: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_025)
- S15: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_014)
- S16: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_027)
- S17: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_045)
- S18: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_007)
- S19: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_023)
- S20: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_041)
- S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_r3_043, cut_in_merge_2hz_random_confirm_r3_046)
- S22: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_026, cut_in_merge_2hz_random_confirm_r3_031, cut_in_merge_2hz_random_confirm_r3_040)
- S23: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_008, cut_in_merge_2hz_random_confirm_r3_013, cut_in_merge_2hz_random_confirm_r3_022)
- S24: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_015)
- S25: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_054)
- S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_024)
- S27: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_036)
- S28: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_random_confirm_r3_032, cut_in_merge_2hz_random_confirm_r3_037, cut_in_merge_2hz_random_confirm_r3_048)
- S29: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_random_confirm_r3_005, cut_in_merge_2hz_random_confirm_r3_010, cut_in_merge_2hz_random_confirm_r3_020, cut_in_merge_2hz_random_confirm_r3_029, cut_in_merge_2hz_random_confirm_r3_038, cut_in_merge_2hz_random_confirm_r3_047)
- S30: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_r3_016, cut_in_merge_2hz_random_confirm_r3_021, cut_in_merge_2hz_random_confirm_r3_030, cut_in_merge_2hz_random_confirm_r3_039)
- S31: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_044)
- S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_035)
- S33: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_003)
- S34: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_r3_004)

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
