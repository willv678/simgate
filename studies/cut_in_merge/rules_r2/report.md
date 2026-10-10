# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 2 of the 5 cases it was asked to find. Both come from the same setting: recorded cars at 1.25x speed with no time shift, on scenes 023b7fcc (S1) and 09a95ffa (S6). At both, every kept run failed, but with so few repeats the lower end of each range only just clears one half. In these failures no car cut in on the ego. In most of them the policy made an unneeded lane change to the left into a car driving beside it. One S6 failure was a side contact from a replayed car coming up alongside, where it is unclear who was at fault. The search tried almost nothing except 1.25x speed and no or earlier time shifts, and it never ran these scenes at the recorded speed. So the study does not show that the retiming causes these failures, and no other scene was confirmed.

## Findings

- On scene 023b7fcc at 0 s shift and 1.25x speed, every kept run failed. Each time the policy steered left into the next lane, even though it was told to go straight and then right, and hit the car driving beside it (actor 56) with its front. The policy was at fault in every run.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_004, cut_in_merge_rules_r2_010, cut_in_merge_rules_r2_019)
- On scene 09a95ffa at 0 s shift and 1.25x speed, every kept run failed. In two runs the policy planned a lane change to the left and hit actor 33 as it came up alongside. In the third, actor 33 met the ego's left front corner while both drove side by side, and fault is unclear. This confirmation therefore rests partly on a failure the policy may not have caused.
  - S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_007, cut_in_merge_rules_r2_011, cut_in_merge_rules_r2_020)
- The confirmed failures are the policy changing lanes into a car next to it, not a reaction to a car cutting in or to a merge. The study does not show that the 1.25x speed is what triggers them, because these scenes were never run at the recorded speed.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_004, cut_in_merge_rules_r2_010, cut_in_merge_rules_r2_019)
  - S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_007, cut_in_merge_rules_r2_011, cut_in_merge_rules_r2_020)
- The single failure on scene 054b5901 at -1 s was not the policy's fault. A replayed car overlapped the ego while it was still following the recorded path, before the policy took over, so this run is no evidence of a weakness.
  - S2: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_rules_r2_053)
- Scene 054b5901 at 0 s and 1.25x failed only once: the ego left the road at a median island while driving far from the recorded path. The policy was at fault, but the run is flagged as a possible rendering artifact, and the failure rate there may well be below one half.
  - S4: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (cut_in_merge_rules_r2_008, cut_in_merge_rules_r2_015, cut_in_merge_rules_r2_023, cut_in_merge_rules_r2_032, cut_in_merge_rules_r2_038)
- Scene 19f339ba at -1 s and 1.25x had one failure: the ego drifted left and a small car passing on the left clipped it, with the policy at fault. Whether this setting fails more often than not is still unsettled. Nearby settings at -1.5 s, -0.5 s and 0 s each had a single run, with no failure.
  - S14: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (cut_in_merge_rules_r2_027, cut_in_merge_rules_r2_029, cut_in_merge_rules_r2_039, cut_in_merge_rules_r2_048)
  - S13: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_036)
  - S15: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_018)
  - S16: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_006)
- At 0 s and 1.25x, scenes 096988dd, 0cf6368d, 12855a41 and 1c45ce3a never failed. Their ranges put the failure rate well below one half. This includes the two scenes where only the marked cut-in car was retimed.
  - S5: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_005, cut_in_merge_rules_r2_014, cut_in_merge_rules_r2_022, cut_in_merge_rules_r2_033, cut_in_merge_rules_r2_042, cut_in_merge_rules_r2_051)
  - S7: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_001, cut_in_merge_rules_r2_017, cut_in_merge_rules_r2_026, cut_in_merge_rules_r2_034, cut_in_merge_rules_r2_043, cut_in_merge_rules_r2_052)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_002, cut_in_merge_rules_r2_016, cut_in_merge_rules_r2_024, cut_in_merge_rules_r2_030, cut_in_merge_rules_r2_040, cut_in_merge_rules_r2_049)
  - S17: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_003, cut_in_merge_rules_r2_013, cut_in_merge_rules_r2_025, cut_in_merge_rules_r2_031_a2, cut_in_merge_rules_r2_041, cut_in_merge_rules_r2_050)
- Scene 0e899dd3 never failed at any setting tried (0 s, -0.5 s and -1 s at 1.25x, and -0.5 s at 1.0x), though most of those settings had only one or a few runs.
  - S8: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_044)
  - S9: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_054)
  - S10: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_r2_035, cut_in_merge_rules_r2_037, cut_in_merge_rules_r2_047)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_rules_r2_009, cut_in_merge_rules_r2_012, cut_in_merge_rules_r2_021, cut_in_merge_rules_r2_028)

## Open

- Three of the five cases are still missing. The search covered only part of the knob ranges: positive time shifts, speeds of 0.5x and 2x, and shifts beyond -1.5 s were never tried. Runs at those settings on the scenes that never failed (096988dd, 0cf6368d, 12855a41, 1c45ce3a, 0e899dd3) could turn up new cases.
- Is the speed change behind the S1 and S6 failures? Repeats on 023b7fcc and 09a95ffa at 0 s and 1.0x speed (replayed traffic) would show whether the policy also swerves left into the neighbouring car without any retiming.
- S6's confirmation partly rests on a failure with unclear fault. More repeats at S6 would show whether the rate stays above one half when that run is left out.
- S14 (19f339ba, -1 s, 1.25x) and S4 (054b5901, 0 s, 1.25x) each had one failure the policy caused. More repeats at each would show whether either is a reliable failure.
- Whether these scenes involve the ego merging or another car cutting in cannot be told from their tags. None of the failures seen so far was a car cutting into the ego's lane.

## Why the runs failed (triage from the video and log)

turned_into_actor 6, actor_hit_ego 2, left_road 1

- cut_in_merge_rules_r2_004: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was going straight at about 5 m/s with a clear lane ahead, but its plan started veering left toward actor 37's lane. By 6.7 s it had cut across the lane line and its front hit actor 56, a car in the adjacent left lane. The recorded human car stayed in its lane (and the route command was turning RIGHT), and the camera looked clean before impact, so the bad lane change was the policy's own mistake.
- cut_in_merge_rules_r2_007: actor_hit_ego, policy at fault: unclear. The ego held about 8 m/s near its recorded path, within 0.8 m of where the human drove. Actor 33 came up quickly from behind in the lane to the left and drew alongside, and its right side met the ego's left front corner, which sat close to the lane line. Contact was side-to-side between two vehicles moving in parallel. The ego did not steer into actor 33 and could do little to avoid it. Actor 33 is a replayed vehicle that does not react to the ego, and the ego was slightly off the recording, so who is at fault is unclear.
- cut_in_merge_rules_r2_010: turned_into_actor, policy at fault: yes. After the policy took over in moderate highway traffic, it planned and steered a leftward drift into the next lane even though the command was STRAIGHT and later RIGHT. While speeding up to about 5.9 m/s it cut into actor 56, which was travelling in that left lane right beside it, and hit it with its front.
- cut_in_merge_rules_r2_011: turned_into_actor, policy at fault: yes. On a multi-lane freeway at about 8 m/s, the policy planned a lane change to the left and moved the ego about 0.9 m off the recorded path toward the left lane. Vehicle 33 was coming up alongside in that lane, and the ego's front corner hit it at 6.2 s; the camera smear on the left appears only at the moment of contact.
- cut_in_merge_rules_r2_019: turned_into_actor, policy at fault: yes. After handoff, the ego was on a multi-lane highway with the command STRAIGHT, later RIGHT. Its plan swung left toward the next lane while speeding up from 4.2 to 6.0 m/s, and it cut across into actor 56, which was travelling alongside it in the left lane, hitting it with its front at 6.7 s. The lead car was more than 20 m ahead and the camera view before impact was clean, so the unneeded lane change into an occupied lane caused the collision.
- cut_in_merge_rules_r2_020: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 8 m/s with the command STRAIGHT, the policy took over at 4.6 s and planned a lane change to the left. It drifted toward the left lane, and actor 33, which was coming up alongside in that lane, was beside it. The ego's front-left corner hit actor 33 at 6.2 s.
- cut_in_merge_rules_r2_032: left_road, policy at fault: yes. With a RIGHT command, the ego stayed in the far-left lane, about 7–8 m left of the recorded path, which curves right. It slowed from 8.5 to 5.4 m/s, and its plan then bent left toward the median island, so it went off the drivable area at the island's edge. There was no collision; the smearing on the left of the camera image appears to come from the ego being far from where the real car drove, not to be what caused the mistake.
- cut_in_merge_rules_r2_039: turned_into_actor, policy at fault: yes. The ego was going about 4 m/s on a multi-lane highway and slowly drifted left, about 1.7 m off the recorded human path; its planned path also bent left. A small actor (id 19) passing on the left in the next lane clipped the ego's left side, and the simulator logged it as a lateral collision with the ego at fault.
- cut_in_merge_rules_r2_053: actor_hit_ego, policy at fault: no. While the ego was still replaying the logged trajectory before handoff (deviation 0 m, about 14 m/s), actor 16 came up from behind, overlapped the ego (rear collision flagged at 2.7–3.7 s, camera smeared inside the car) and ended up just ahead of it. At handoff (4.7 s), the ego's front bumper is still overlapping actor 16, so a front collision was registered at the very instant the policy took control, with no time for the policy to react.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_004, cut_in_merge_rules_r2_010, cut_in_merge_rules_r2_019)
- S2: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_rules_r2_053)
- S3: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_rules_r2_045, cut_in_merge_rules_r2_046)
- S4: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (cut_in_merge_rules_r2_008, cut_in_merge_rules_r2_015, cut_in_merge_rules_r2_023, cut_in_merge_rules_r2_032, cut_in_merge_rules_r2_038)
- S5: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_005, cut_in_merge_rules_r2_014, cut_in_merge_rules_r2_022, cut_in_merge_rules_r2_033, cut_in_merge_rules_r2_042, cut_in_merge_rules_r2_051)
- S6: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_r2_007, cut_in_merge_rules_r2_011, cut_in_merge_rules_r2_020)
- S7: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_001, cut_in_merge_rules_r2_017, cut_in_merge_rules_r2_026, cut_in_merge_rules_r2_034, cut_in_merge_rules_r2_043, cut_in_merge_rules_r2_052)
- S8: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_044)
- S9: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_054)
- S10: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_r2_035, cut_in_merge_rules_r2_037, cut_in_merge_rules_r2_047)
- S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_rules_r2_009, cut_in_merge_rules_r2_012, cut_in_merge_rules_r2_021, cut_in_merge_rules_r2_028)
- S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_002, cut_in_merge_rules_r2_016, cut_in_merge_rules_r2_024, cut_in_merge_rules_r2_030, cut_in_merge_rules_r2_040, cut_in_merge_rules_r2_049)
- S13: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_036)
- S14: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (cut_in_merge_rules_r2_027, cut_in_merge_rules_r2_029, cut_in_merge_rules_r2_039, cut_in_merge_rules_r2_048)
- S15: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_018)
- S16: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_rules_r2_006)
- S17: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_rules_r2_003, cut_in_merge_rules_r2_013, cut_in_merge_rules_r2_025, cut_in_merge_rules_r2_031_a2, cut_in_merge_rules_r2_041, cut_in_merge_rules_r2_050)

## Not kept by the gate

- cut_in_merge_rules_r2_031: not kept: RE-RUN

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
