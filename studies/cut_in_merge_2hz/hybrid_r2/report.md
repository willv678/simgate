# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Three settings cleared the bar, each on a different scene: 096988dd with the cars at 0 s and 2x speed (S5), and 023b7fcc and 09a95ffa with the cars at 0 s and 1.25x speed (S1, S6). Only S1 is clearly the policy's fault: the ego sped up and steered left into a car in the next lane. At S6 a replayed car overtaking from behind clipped the ego while it held its lane, so the policy's fault is unclear. At S5 most failures come from a bad track for actor 9, which appears overlapping the ego at handoff, not from a driving mistake. So only one of the three is a clean policy failure. A fourth scene, 19f339ba, fails often at 1.25x but has not cleared the bar. There the policy drifts left even though its route command says RIGHT (S18, S19), so its left drift still causes collisions at 2 Hz. The study only tried shifts of ±0.5 s and speeds of 1.25x to 2x, never a recorded-timing run on the same replay setup, so it does not show whether the retiming causes these failures.

## Findings

- At 023b7fcc with the cars at 0 s and 1.25x speed, every run failed and the policy was at fault each time. Going straight on a multi-lane highway, the ego sped up, left the recorded path to the left and hit vehicle 56, which was driving alongside in the left lane.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r2_004, cut_in_merge_2hz_hybrid_r2_010, cut_in_merge_2hz_hybrid_r2_011)
- At 09a95ffa with the cars at 0 s and 1.25x speed, every run failed, but in each one replayed vehicle 33 came up from behind in the left lane and clipped the ego's front-left corner. The ego was holding its lane at a steady speed, so the policy's fault is unclear. This counts as confirmed but is weak evidence of a policy weakness.
  - S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r2_007, cut_in_merge_2hz_hybrid_r2_012, cut_in_merge_2hz_hybrid_r2_013)
- At 096988dd with the cars at 2x speed, every run failed. In most of them, though, actor 9 already sits on or overlaps the ego at handoff while the ego is on the human's path. Triage reads this as a bad actor track, not the policy's fault, and blames the policy for only one run (no braking for the lead). At 1.25x and 1.5x the scene did not fail.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_r2_035, cut_in_merge_2hz_hybrid_r2_037, cut_in_merge_2hz_hybrid_r2_038, cut_in_merge_2hz_hybrid_r2_039)
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_005, cut_in_merge_2hz_hybrid_r2_018)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_024)
- 19f339ba fails repeatedly with the cars at 1.25x speed, at both -0.5 s and 0 s, but neither setting cleared the confirmation bar. These failures are the policy's: with a RIGHT command, the ego drifts about 1.5 m left onto the lane line and hits a car or motorcycle overtaking on its left. So the left drift still causes collisions at 2 Hz planning.
  - S18: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 4/7 failed, rate 29%-81% (90%) (cut_in_merge_2hz_hybrid_r2_044, cut_in_merge_2hz_hybrid_r2_046, cut_in_merge_2hz_hybrid_r2_047, cut_in_merge_2hz_hybrid_r2_048, cut_in_merge_2hz_hybrid_r2_049, cut_in_merge_2hz_hybrid_r2_050, cut_in_merge_2hz_hybrid_r2_051)
  - S19: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 3/9 failed, rate 14%-60% (90%) (cut_in_merge_2hz_hybrid_r2_006, cut_in_merge_2hz_hybrid_r2_014, cut_in_merge_2hz_hybrid_r2_015, cut_in_merge_2hz_hybrid_r2_019, cut_in_merge_2hz_hybrid_r2_020, cut_in_merge_2hz_hybrid_r2_021, cut_in_merge_2hz_hybrid_r2_028, cut_in_merge_2hz_hybrid_r2_029, cut_in_merge_2hz_hybrid_r2_030)
- 12855a41 did not fail at any setting tried (shifts of -0.5 s to +0.5 s, speeds of 1.25x to 2x). For 1.5x, and for 1.5x with a +0.5 s shift, the ranges already put the failure rate below one half.
  - S13: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_023)
  - S14: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_002, cut_in_merge_2hz_hybrid_r2_016)
  - S15: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_r2_022, cut_in_merge_2hz_hybrid_r2_052, cut_in_merge_2hz_hybrid_r2_053, cut_in_merge_2hz_hybrid_r2_054)
  - S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_032, cut_in_merge_2hz_hybrid_r2_033)
  - S17: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r2_034, cut_in_merge_2hz_hybrid_r2_042, cut_in_merge_2hz_hybrid_r2_043)
- 0e899dd3 did not fail at any setting tried. With the cars 0.5 s later at 1.25x speed, the failure rate is surely below one half.
  - S9: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_026)
  - S10: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_009, cut_in_merge_2hz_hybrid_r2_017)
  - S11: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_025)
  - S12: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r2_036, cut_in_merge_2hz_hybrid_r2_041, cut_in_merge_2hz_hybrid_r2_040_a2)
- 054b5901, 0cf6368d and 1c45ce3a each got only one run per setting, all without failure. That is too few runs to call these scenes safe.
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_008)
  - S7: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_001)
  - S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_027)
  - S22: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_003)

## Open

- Whether the retiming causes the failures at all: no setting ran the recorded timing (0 s, 1.0x) with replayed traffic. Repeats at 0 s / 1.0x on 023b7fcc, 09a95ffa, 096988dd and 19f339ba would show whether these scenes already fail without retiming.
- Most of the time and speed range was never searched: shifts beyond ±0.5 s (up to ±2 s) and speeds below 1.0x (down to 0.5x) were not run on any scene.
- Whether 19f339ba is a fourth confirmed case: more repeats at -0.5 s, 1.25x would settle whether its failure rate is above one half.
- Whether S5 is a real case: actor 9's track at 096988dd should be checked. If the track is bad, that setting should be dropped, and the scene probed at other speeds or with actor 9 removed.
- Whether S6 reflects a policy weakness or only a replayed car that cannot react sideswiping the ego. That needs a look at the ego's lateral drift in those runs, or a run with reactive traffic.
- 054b5901, 0cf6368d and 1c45ce3a are barely explored. Several runs each at 1.5x to 2x and at shifted timings would show whether any of them breaks.
- The comparison with the 10 Hz study cut_in_merge needs that study's results next to these. This report cannot say whether 2 Hz planning changes which scenes fail.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, actor_hit_ego 4, other 3, no_brake_for_lead 1

- cut_in_merge_2hz_hybrid_r2_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's plan (orange) veered left toward vehicle 15's lane, against the recorded path (green). The ego sped up from 4.4 to 6.6 m/s and cut left into vehicle 56, which was just ahead in the adjacent left lane, so its front hit 56 at 7.2 s. The rear contact came after this front collision.
- cut_in_merge_2hz_hybrid_r2_006: turned_into_actor, policy at fault: yes. The route said RIGHT, but the ego crept along a multi-lane highway at about 4.5 m/s. Its planned path bent left, and from 10.1s it straddled the lane line on its left. At 12.1s actor 29, a small vehicle overtaking in the lane to the left, made side contact with the ego's left side; the ego was 1.5 m off the recorded human path.
- cut_in_merge_2hz_hybrid_r2_007: actor_hit_ego, policy at fault: unclear. The ego was going straight at a steady 8 m/s, with a clear 25 m or more to the car ahead. Vehicle 33 came up from behind in the left lane and ended up overlapping the ego's front-left corner at 6.6 s, which registered as a front collision; the run also has rear contact, and the ego was only 0.9 m off the recorded human path. This looks like a replayed actor sideswiping the ego as it passed, not the ego steering into it, but the frames can't rule out a small leftward drift by the ego.
- cut_in_merge_2hz_hybrid_r2_010: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy steered left away from the recorded path toward the next lane and sped up from 4.4 to 6.5 m/s. Its front hit vehicle 56, which was driving beside it in that lane. The 2.6 m gap at 7.2 s is the distance to vehicle 56, and the camera smear on the left appears only at impact.
- cut_in_merge_2hz_hybrid_r2_011: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego sped up from about 4.4 to 6.5 m/s and drifted left toward the lane the recorded human moved into. Its front corner ran into actor 56, which was alongside in the left lane, at 7.2 s. The ego did not wait for a gap or yield to 56. The rear contact flag comes from a separate contact behind the ego; the front collision is the failure being counted.
- cut_in_merge_2hz_hybrid_r2_012: actor_hit_ego, policy at fault: unclear. The ego kept going straight in its lane at about 8 m/s while the recorded human drifted left. Actor 33 came up from behind in the left lane, got level with the ego, and touched its front-left corner at 6.6 s. The run also records a rear contact, which fits an overtaking actor clipping the ego.
- cut_in_merge_2hz_hybrid_r2_013: actor_hit_ego, policy at fault: unclear. The ego kept going straight in its lane at a steady 8 m/s, while the human in the recording moved into the lane to the left. Actor 33 came up fast from behind in that left lane and, by 6.6s, cut across the ego's front-left corner, which counts as a front collision. The vehicle ahead in the ego's own lane stayed about 26 m away, and the ego never steered toward 33.
- cut_in_merge_2hz_hybrid_r2_015: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego crawled along at about 4 m/s, roughly 68 m behind where the human drove, and straddled the line between its lane and the lane to its left. Actor 29, replayed from the recording, came up from behind in that left lane and struck the ego's left side (lateral collision) because the ego was half in its lane.
- cut_in_merge_2hz_hybrid_r2_019: actor_hit_ego, policy at fault: unclear. On a multi-lane highway the ego crawled along at about 4 m/s, roughly 70 m behind where the recorded car was at that point, and drifted about 1.5 m left of the recorded path. A small replayed actor (29), not visible a second earlier, came up from behind on the left and hit the ego's left side. The actor follows the recording and cannot react, but the ego's slow speed and drift to the left put it in that actor's path.
- cut_in_merge_2hz_hybrid_r2_035: other, policy at fault: no. Actor 9's track is inconsistent with the recorded drive. At handoff (4.7 s) it already sits about 0.5 m ahead of the ego, and at 5.2 s it overlaps the ego, while the ego is still on the human's path (0.02 m off). It then pulls ahead to about 8 m and closes back in to overlap the ego again at 7.2 s, even though the ego slowed from 5.5 to 4.0 m/s and stayed within 0.2 m of the human trajectory. The camera shows actor 9 only as a smeared blob. This looks like a bad actor track or reconstruction, with an inconsistent rear contact as well, not a real driving mistake: the human drove through the same space without a collision.
- cut_in_merge_2hz_hybrid_r2_037: no_brake_for_lead, policy at fault: yes. Lead actor 9 was already almost touching the ego in its lane at handoff (gap 43.6 m → 0.5 m between 4.2 and 4.7 s, likely a cut-in) and the two overlapped around 5.2 s. The gap then opened to about 8 m, but the ego only slowed from 5.7 to 4.0 m/s, closed on the slower actor 9 again and hit it with its front at 7.2 s. Actor 9 was a smeared but visible blob in the camera at 6.2 s.
- cut_in_merge_2hz_hybrid_r2_038: other, policy at fault: unclear. The ego stayed on the recorded human path, 0.1 m off at the failure. Actor 9 sat on that same path and was already overlapping the ego at handoff (gap 0.5 m at 4.7 s, front-collision flag set by 5.2 s). Its motion was implausible: it pulled 8 m ahead and then nearly stopped, so the ego closed in from 8.1 m to 3.7 m while slowing only from 5.7 to 4.2 m/s, and hit it at 7.2 s. Because the human drove through this spot, actor 9 looks like a spurious or misplaced track that the camera shows only as a smear, so this is a scenario artifact more than a clean failure to brake for a lead.
- cut_in_merge_2hz_hybrid_r2_039: other, policy at fault: no. Actor 9 seems to be a bad track, not a real vehicle. At handoff (4.7 s) it suddenly sits 0.5 m ahead of the ego in the ego's own lane, though nothing was within 43 m half a second earlier. It already overlaps the ego at 5.2 s, pulls ahead to about 8 m, then almost stops and is touched again at 7.2 s. The ego stays on the recorded human path the whole time (0.0 m off at failure), the camera shows only a smeared ghost car, and a rear contact is also logged.
- cut_in_merge_2hz_hybrid_r2_044: turned_into_actor, policy at fault: yes. The ego was going about 5 m/s in slow highway traffic with a RIGHT command, but its plan drifted left, putting it about 1.5 m left of the recorded path and onto the lane line. A small actor (29, probably a motorcycle) was passing on the left, and the ego hit it side-on (lateral collision) at 11.6 s.
- cut_in_merge_2hz_hybrid_r2_046: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5.5 m/s, with the route command changing to RIGHT, the ego drifted left across the lane line instead of following the recorded path to the right. Its left side hit actor 25, which was in the adjacent left lane alongside it, and the run logged a lateral collision about 1.6 m off the recorded trajectory.
- cut_in_merge_2hz_hybrid_r2_049: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5 m/s, the ego drifted left toward the lane line even though the route command was RIGHT, ending up 1.6 m left of the human's path. A small actor (29, likely a motorcycle) came up on the ego's left, and the ego's front-left corner clipped it.
- cut_in_merge_2hz_hybrid_r2_051: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5 m/s, with the route command RIGHT, the ego drifted left across its lane toward the left lane line, ending 1.6 m left of the recorded human path. Actor 29 was overtaking in the adjacent left lane, and the ego's front-left corner clipped it as it passed at 12.1 s.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r2_004, cut_in_merge_2hz_hybrid_r2_010, cut_in_merge_2hz_hybrid_r2_011)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_008)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_005, cut_in_merge_2hz_hybrid_r2_018)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_024)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_r2_035, cut_in_merge_2hz_hybrid_r2_037, cut_in_merge_2hz_hybrid_r2_038, cut_in_merge_2hz_hybrid_r2_039)
- S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r2_007, cut_in_merge_2hz_hybrid_r2_012, cut_in_merge_2hz_hybrid_r2_013)
- S7: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_001)
- S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_027)
- S9: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_026)
- S10: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_009, cut_in_merge_2hz_hybrid_r2_017)
- S11: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_025)
- S12: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r2_036, cut_in_merge_2hz_hybrid_r2_041, cut_in_merge_2hz_hybrid_r2_040_a2)
- S13: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_023)
- S14: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_002, cut_in_merge_2hz_hybrid_r2_016)
- S15: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_r2_022, cut_in_merge_2hz_hybrid_r2_052, cut_in_merge_2hz_hybrid_r2_053, cut_in_merge_2hz_hybrid_r2_054)
- S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r2_032, cut_in_merge_2hz_hybrid_r2_033)
- S17: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r2_034, cut_in_merge_2hz_hybrid_r2_042, cut_in_merge_2hz_hybrid_r2_043)
- S18: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 4/7 failed, rate 29%-81% (90%) (cut_in_merge_2hz_hybrid_r2_044, cut_in_merge_2hz_hybrid_r2_046, cut_in_merge_2hz_hybrid_r2_047, cut_in_merge_2hz_hybrid_r2_048, cut_in_merge_2hz_hybrid_r2_049, cut_in_merge_2hz_hybrid_r2_050, cut_in_merge_2hz_hybrid_r2_051)
- S19: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 3/9 failed, rate 14%-60% (90%) (cut_in_merge_2hz_hybrid_r2_006, cut_in_merge_2hz_hybrid_r2_014, cut_in_merge_2hz_hybrid_r2_015, cut_in_merge_2hz_hybrid_r2_019, cut_in_merge_2hz_hybrid_r2_020, cut_in_merge_2hz_hybrid_r2_021, cut_in_merge_2hz_hybrid_r2_028, cut_in_merge_2hz_hybrid_r2_029, cut_in_merge_2hz_hybrid_r2_030)
- S20: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_031)
- S21: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_045)
- S22: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r2_003)

## Not kept by the gate

- cut_in_merge_2hz_hybrid_r2_040: not kept: RESTART_CLEANUP

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

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
