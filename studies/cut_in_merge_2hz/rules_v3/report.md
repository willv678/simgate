# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules_v3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not find the 5 challenging cases. No setting was confirmed with a failure rate surely above one half, so the goal was not met. Collisions happened at only two settings: the recorded timing on 19f339ba (S25) and cars 0.5 s earlier on 1c45ce3a (S26). Both ranges still reach well below one half. Neither looks like the policy failing a cut-in. In each, the ego slowed or braked hard with a clear road ahead, and a replayed car that cannot react to it came up from behind or the side into it. The metrics scored this as a front collision. Most of the search kept cars at 1.0x speed and within 0.5 s of the recorded timing, so most of the brief's range (±2 s, 0.5x to 2x) was never tested and the question of which timings and speeds cause failures stays open.

## Findings

- The most failure-prone setting found was the recorded timing (0 s, 1.0x) on 19f339ba. Its failure rate is not confirmed above one half: the range spans from low to just above one half.
  - S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.0: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_v3_006, cut_in_merge_2hz_rules_v3_014, cut_in_merge_2hz_rules_v3_019_a2, cut_in_merge_2hz_rules_v3_028, cut_in_merge_2hz_rules_v3_038, cut_in_merge_2hz_rules_v3_050)
- On 19f339ba, the policy is to blame but did not crash into anything ahead. Both times the ego braked hard on an open highway for no visible reason and fell about 20 m behind its recorded position. A replayed car then ran into its right side, and the metrics scored that as a front collision.
  - S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.0: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_v3_006, cut_in_merge_2hz_rules_v3_014, cut_in_merge_2hz_rules_v3_019_a2, cut_in_merge_2hz_rules_v3_028, cut_in_merge_2hz_rules_v3_038, cut_in_merge_2hz_rules_v3_050)
- Shifting the cut-in car 0.5 s earlier on 1c45ce3a gave one collision, while the recorded timing on that scene gave none. One failure is only a hint. In that run the ego slowed with no one close ahead and a replayed car hit its front-right corner from behind, so it is unclear whether the policy was at fault.
  - S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_v3_031, cut_in_merge_2hz_rules_v3_039, cut_in_merge_2hz_rules_v3_046)
  - S27: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_003, cut_in_merge_2hz_rules_v3_010, cut_in_merge_2hz_rules_v3_021)
- No run failed on the other seven scenes at any setting tried, though each setting got only one to three runs. On 054b5901, even the extreme settings (-2 s at 0.5x and 2x, +1.5 s and +2 s at 0.5x) passed, each on one or two runs.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_034, cut_in_merge_2hz_rules_v3_037, cut_in_merge_2hz_rules_v3_048)
  - S2: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_004, cut_in_merge_2hz_rules_v3_015, cut_in_merge_2hz_rules_v3_025)
  - S3: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_018)
  - S4: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_027)
  - S5: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_008)
  - S6: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_054)
  - S7: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_036, cut_in_merge_2hz_rules_v3_040)
  - S8: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_030)
  - S9: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_005, cut_in_merge_2hz_rules_v3_012, cut_in_merge_2hz_rules_v3_022)
  - S10: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_042, cut_in_merge_2hz_rules_v3_051)
  - S11: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_029)
  - S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_007, cut_in_merge_2hz_rules_v3_013_a2, cut_in_merge_2hz_rules_v3_020)
  - S13: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_041, cut_in_merge_2hz_rules_v3_047)
  - S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_035)
  - S15: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_053)
  - S16: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_001, cut_in_merge_2hz_rules_v3_017, cut_in_merge_2hz_rules_v3_026)
  - S17: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_045)
  - S18: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_033)
  - S19: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_052)
  - S20: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_009, cut_in_merge_2hz_rules_v3_016, cut_in_merge_2hz_rules_v3_024)
  - S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_044)
  - S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_032)
  - S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_002, cut_in_merge_2hz_rules_v3_011, cut_in_merge_2hz_rules_v3_023)
  - S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_043, cut_in_merge_2hz_rules_v3_049)
- The best near-miss leads, ranked by criticality, are: 1c45ce3a at -0.5 s, 023b7fcc at -0.5 s, 09a95ffa at the recorded timing, and 0e899dd3 at 0.75x speed. Near misses guided the search but are not a checked ranking.
  - S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_v3_031, cut_in_merge_2hz_rules_v3_039, cut_in_merge_2hz_rules_v3_046)
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_034, cut_in_merge_2hz_rules_v3_037, cut_in_merge_2hz_rules_v3_048)
  - S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_007, cut_in_merge_2hz_rules_v3_013_a2, cut_in_merge_2hz_rules_v3_020)
  - S19: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_052)
- No failure was flagged as a possible simulator artifact. Still, every collision involved a replayed car that cannot react to the ego, after the ego had fallen far behind its recorded path. This is close to the rear and side hits the plan said to ignore, so these collisions may overstate how dangerous the cut-ins themselves are.
  - S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.0: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_v3_006, cut_in_merge_2hz_rules_v3_014, cut_in_merge_2hz_rules_v3_019_a2, cut_in_merge_2hz_rules_v3_028, cut_in_merge_2hz_rules_v3_038, cut_in_merge_2hz_rules_v3_050)
  - S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_v3_031, cut_in_merge_2hz_rules_v3_039, cut_in_merge_2hz_rules_v3_046)

## Open

- Whether any timing or speed of the other cars reliably makes the policy fail: speed scales of 1.25x to 2x and time shifts beyond ±0.5 s were tried only on 054b5901. A grid of about one run per setting across the full ±2 s and 0.5x–2x range on the scenes with a marked cut-in car (0cf6368d, 12855a41, 1c45ce3a) and on 19f339ba would show where to look.
- Whether 19f339ba at the recorded timing (S25) fails more than half the time: about 4 to 6 more repeats would bring its range clear of one half or settle it below.
- Whether 1c45ce3a at -0.5 s (S26) is a real failure setting: about 4 more repeats, plus nearby settings (-1 s, -0.5 s at 1.25x).
- Whether the policy's unprovoked hard braking on 19f339ba also happens at 10 Hz planning: compare these runs with the matching settings in the 10 Hz study cut_in_merge. This report has no 10 Hz data.
- Whether these collisions count as front or side collisions under the brief: in each one, a replayed car that does not react to the ego hit it from behind or the side. Re-scoring them with a contact-direction check, or re-running with reactive traffic, would show whether the policy really drives into anything.

## Why the runs failed (triage from the video and log)

actor_hit_ego 2, other 1

- cut_in_merge_2hz_rules_v3_014: actor_hit_ego, policy at fault: yes. On an open multi-lane highway with the lane ahead clear and the gap growing (19 m to 60 m and then no lead), the ego braked hard for no visible reason, from 16.9 to 5.6 m/s, and fell about 20 m behind the recorded position. Replayed actor 18, which does not react to the ego, then drove into the ego's right-rear while the ego was still braking. The overlap counted as a front collision, but the ego was not driving into anything.
- cut_in_merge_2hz_rules_v3_028: other, policy at fault: yes. The ego braked hard on an open highway, from 16.9 to 5.4 m/s, with no lead vehicle closer than about 19 m, and drifted slightly toward the left lane. It fell about 20 m behind its recorded position, and by 7.6 s actor 28 (shown ahead earlier) was sitting right on top of the ego's right side, which the metrics scored as a front collision with rear contact as well. This looks like unprovoked hard braking leaving the ego in the way of traffic that doesn't react to it, not driving into a lead car.
- cut_in_merge_2hz_rules_v3_039: actor_hit_ego, policy at fault: unclear. The ego was going straight on a freeway right on the recorded path (0.1 m off) but slowing from 9.7 to 8.0 m/s with no one close ahead, which left it about 24 m behind where the recorded car was. Actor 24, replayed from the log, came up from behind on the right and moved into the ego's front-right corner, which was logged as a front collision. Actor 24 also hit the ego's rear.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_034, cut_in_merge_2hz_rules_v3_037, cut_in_merge_2hz_rules_v3_048)
- S2: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_004, cut_in_merge_2hz_rules_v3_015, cut_in_merge_2hz_rules_v3_025)
- S3: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_018)
- S4: 054b5901 at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_027)
- S5: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_008)
- S6: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_054)
- S7: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_036, cut_in_merge_2hz_rules_v3_040)
- S8: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_030)
- S9: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_005, cut_in_merge_2hz_rules_v3_012, cut_in_merge_2hz_rules_v3_022)
- S10: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_042, cut_in_merge_2hz_rules_v3_051)
- S11: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_029)
- S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_007, cut_in_merge_2hz_rules_v3_013_a2, cut_in_merge_2hz_rules_v3_020)
- S13: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_041, cut_in_merge_2hz_rules_v3_047)
- S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_035)
- S15: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_053)
- S16: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_001, cut_in_merge_2hz_rules_v3_017, cut_in_merge_2hz_rules_v3_026)
- S17: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_045)
- S18: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_033)
- S19: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_052)
- S20: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_009, cut_in_merge_2hz_rules_v3_016, cut_in_merge_2hz_rules_v3_024)
- S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_044)
- S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_rules_v3_032)
- S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_002, cut_in_merge_2hz_rules_v3_011, cut_in_merge_2hz_rules_v3_023)
- S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_rules_v3_043, cut_in_merge_2hz_rules_v3_049)
- S25: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.0: 2/6 failed, rate 12%-65% (90%) (cut_in_merge_2hz_rules_v3_006, cut_in_merge_2hz_rules_v3_014, cut_in_merge_2hz_rules_v3_019_a2, cut_in_merge_2hz_rules_v3_028, cut_in_merge_2hz_rules_v3_038, cut_in_merge_2hz_rules_v3_050)
- S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_rules_v3_031, cut_in_merge_2hz_rules_v3_039, cut_in_merge_2hz_rules_v3_046)
- S27: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_rules_v3_003, cut_in_merge_2hz_rules_v3_010, cut_in_merge_2hz_rules_v3_021)

## Not kept by the gate

- cut_in_merge_2hz_rules_v3_013: not kept: RE-RUN
- cut_in_merge_2hz_rules_v3_019: not kept: RE-RUN

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

56 of 56 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
