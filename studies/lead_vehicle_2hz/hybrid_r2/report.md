# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_r2`: 49 kept runs on 7 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The study confirmed 2 of the 5 cases it was asked for, so the goal was not met. The two confirmed settings are: 09a95ffa with the lead car 0.5 s later at 0.75x speed (S14), and 12855a41 with the lead car at 0.5x speed (S18). Neither shows the policy rear-ending the lead car. At S14, every run's failure followed the same pattern: the ego braked hard behind the slowed lead car, then drifted left against a RIGHT command and hit a car in the left lane. At S18, the front contacts were flagged 0.5 s after handoff while the ego was still exactly on the recorded path. That looks like a log-replay or bounding-box artifact (the automatic artifact check did not flag it), so S18's confirmation is doubtful. Every other setting failed at most once, or is one to three runs, which is a hint rather than a rate. In this study, no rear-end of the lead car by the policy was shown at 2 Hz.

## Findings

- At 09a95ffa with the lead car 0.5 s later at 0.75x speed, every run failed and the failure rate is confirmed above 0.5. Every failure was the ego turning left into car 33 in the adjacent lane after braking hard for the lead car, not a rear-end. The policy was at fault each time.
  - S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_2hz_hybrid_r2_042, lead_vehicle_2hz_hybrid_r2_046, lead_vehicle_2hz_hybrid_r2_047, lead_vehicle_2hz_hybrid_r2_048)
- At 09a95ffa, the same 0.5 s delay at the recorded speed, and the unshifted lead car at 0.75x, 1x or 1.25x speed, produced no failures. The failure needs both the later and the slower lead car, though these settings had only one or two runs each.
  - S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_016)
  - S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_013, lead_vehicle_2hz_hybrid_r2_028)
  - S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_006)
  - S15: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_035, lead_vehicle_2hz_hybrid_r2_041)
- At 12855a41 with the lead car at 0.5x speed, every run failed and the code counts it as confirmed. But the triage puts the contacts 0.5 s after handoff with the ego still on the recorded path and a gap of about 4 m, which points to replay or bounding-box artifacts and not a policy error. The policy was judged not at fault in two runs and unclear in the third.
  - S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_2hz_hybrid_r2_026, lead_vehicle_2hz_hybrid_r2_029, lead_vehicle_2hz_hybrid_r2_030)
- At 12855a41 with the lead car at 0.75x speed, most runs failed, but this is not confirmed. One failure was the ego drifting left into the adjacent lane and being sideswiped (policy at fault). The other was a replayed car cutting across the ego's front (fault unclear). The recorded and faster lead speeds did not fail.
  - S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75: 2/3 failed, rate 25%-92% (90%) (lead_vehicle_2hz_hybrid_r2_015, lead_vehicle_2hz_hybrid_r2_022, lead_vehicle_2hz_hybrid_r2_023)
  - S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_012, lead_vehicle_2hz_hybrid_r2_018)
  - S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_003)
- Every failure where the policy was at fault was a leftward lateral move into a car in the adjacent lane, mostly against a RIGHT or STRAIGHT command. At 2 Hz the left drift, not braking for the lead car, is what causes the failures.
  - S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75: 1/5 failed, rate 5%-56% (90%) (lead_vehicle_2hz_hybrid_r2_017, lead_vehicle_2hz_hybrid_r2_024, lead_vehicle_2hz_hybrid_r2_025, lead_vehicle_2hz_hybrid_r2_036, lead_vehicle_2hz_hybrid_r2_037)
  - S6: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (lead_vehicle_2hz_hybrid_r2_040, lead_vehicle_2hz_hybrid_r2_043, lead_vehicle_2hz_hybrid_r2_044, lead_vehicle_2hz_hybrid_r2_045)
  - S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_2hz_hybrid_r2_042, lead_vehicle_2hz_hybrid_r2_046, lead_vehicle_2hz_hybrid_r2_047, lead_vehicle_2hz_hybrid_r2_048)
  - S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75: 2/3 failed, rate 25%-92% (90%) (lead_vehicle_2hz_hybrid_r2_015, lead_vehicle_2hz_hybrid_r2_022, lead_vehicle_2hz_hybrid_r2_023)
- On 023b7fcc and 096988dd, single failures appeared: an unprompted left lane change at the unshifted, 0.75x setting, and a left steer into car 41 with the lead car 1 s earlier at 1.25x speed. Neither is confirmed, and nearby settings did not fail.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_038, lead_vehicle_2hz_hybrid_r2_049)
  - S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_hybrid_r2_027, lead_vehicle_2hz_hybrid_r2_031, lead_vehicle_2hz_hybrid_r2_032)
  - S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75: 1/5 failed, rate 5%-56% (90%) (lead_vehicle_2hz_hybrid_r2_017, lead_vehicle_2hz_hybrid_r2_024, lead_vehicle_2hz_hybrid_r2_025, lead_vehicle_2hz_hybrid_r2_036, lead_vehicle_2hz_hybrid_r2_037)
  - S4: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_014)
  - S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_005)
  - S6: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (lead_vehicle_2hz_hybrid_r2_040, lead_vehicle_2hz_hybrid_r2_043, lead_vehicle_2hz_hybrid_r2_044, lead_vehicle_2hz_hybrid_r2_045)
  - S7: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_033, lead_vehicle_2hz_hybrid_r2_039)
  - S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_010)
  - S9: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_hybrid_r2_004, lead_vehicle_2hz_hybrid_r2_008, lead_vehicle_2hz_hybrid_r2_019)
  - S10: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_020)
- No failure appeared on 19f339ba at any setting tried, and none on 0dbb91dd or 0cf6368d, each of which had only a single screening run.
  - S16: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_007)
  - S17: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_001)
  - S22: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_034)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_011)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_002_a2, lead_vehicle_2hz_hybrid_r2_009)
  - S25: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_021)

## Open

- Is S18 (12855a41, 0.5x) a real failure? Check the bounding boxes and the pre-handoff contact in runs r2_026, r2_029 and r2_030, or rerun with an earlier handoff so the policy has time to act. Until then it should not count as one of the five.
- S19 (12855a41, 0.75x) needs about two to three more runs to confirm or reject it. Its failures are of mixed kinds.
- S6 (096988dd, lead car 1 s earlier, 1.25x speed) and S3 (023b7fcc, unshifted, 0.75x) each failed once. Repeats, and neighbours such as 096988dd at -1.5 s or 023b7fcc at 0.5 s later and 0.75x, would show whether either is a third case.
- Scene 0e899dd3 was never run, and 0dbb91dd and 0cf6368d got only one run each at 1.25x. Slower-lead settings (0.5–0.75x, 0 to +1 s) on these scenes are the remaining chances to find more distinct-scene cases.
- Whether the policy rear-ends the lead car at all at 2 Hz is still open. Settings with a harder stop (0.5x with later shifts) on the scenes that came closest before (19f339ba, 096988dd, 023b7fcc) were barely explored.
- Comparison with the 10 Hz lead_vehicle study is not possible from these results alone. Put the two studies' failure causes side by side to test whether halving the left drift changed which cases fail.

## Why the runs failed (triage from the video and log)

turned_into_actor 7, other 2, actor_hit_ego 1, no_brake_for_lead 1

- lead_vehicle_2hz_hybrid_r2_015: actor_hit_ego, policy at fault: unclear. The ego crawled along in dense highway traffic at about 3.5 m/s. It sat about 2 m left of the recorded human path, straddling toward the left lane, despite the RIGHT command. Actor 51, replayed from the log, came up from behind-left, passed the ego and moved right across its front-left corner, triggering a front collision at 11.7 s. The ego was driving straight and neither braked nor moved right to make room.
- lead_vehicle_2hz_hybrid_r2_017: turned_into_actor, policy at fault: yes. The ego was following car 12 at about 7 m. It then changed lanes to the left, even though the route command was RIGHT and the recorded path stayed to the right. Partway into the next lane it made side contact with car 56, which was coming up in that lane just behind the ego (lateral collision at 7.7 s).
- lead_vehicle_2hz_hybrid_r2_023: turned_into_actor, policy at fault: yes. The route said RIGHT and the human had moved right toward actor 9's lane. Instead, the ego slowly (about 3–4 m/s) drifted left until it straddled the lane line into the left lane, ending about 2.1 m off the recorded path. Actor 51 came up in that left lane and sideswiped the ego at 10.7 s, a lateral collision caused by the ego being in its lane.
- lead_vehicle_2hz_hybrid_r2_026: other, policy at fault: no. In slow highway traffic, the ego followed lead car 5 in its lane at about 3 m/s while the reported gap shrank from 8 m to 4.1 m. A front collision with car 5 was flagged at 5.2 s, only 0.5 s after the policy took over, while the ego was still on the recorded human path (0.0 m off) and the gap was about 4 m. That points to a log-replay or bounding-box artifact rather than a real rear-end by the policy.
- lead_vehicle_2hz_hybrid_r2_029: no_brake_for_lead, policy at fault: unclear. In stop-and-go highway traffic, the ego was following lead car 5 in its lane on a straight. The gap was closing at about 1.3 m/s before the 4.7 s handoff, and a front collision with car 5 was flagged at 5.2 s, only 0.5 s after the policy took over. The ego was still exactly on the recorded path (0.0 m off) and had slowed only from 3.3 to 2.9 m/s, so the closing situation came from the replayed log and the gap data (still 4.1 m) do not clearly show contact.
- lead_vehicle_2hz_hybrid_r2_030: other, policy at fault: no. In slow highway traffic, the ego was following lead car 5 at about 3 m/s with a closing gap. The front contact was flagged at 5.2 s, only 0.5 s after the policy took over, while the ego was still exactly on the recorded human path (0.0 m off) and slowing down, so this looks like a box-overlap artifact from the replayed log, not a policy error. The map already shows contact marks at the ego's front at 4.2 s, before handoff, and the ego was also rear-ended at some point.
- lead_vehicle_2hz_hybrid_r2_040: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5 m/s with a STRAIGHT command, the policy began steering left toward the next lane (orange path), away from the recorded trajectory (green). Car 41 was already in that lane just ahead-left of the ego, and the ego's front corner hit it at 7.2 s (front collision, 1.3 m off the recorded path).
- lead_vehicle_2hz_hybrid_r2_042: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego braked hard behind lead car 1 (from 7.9 to 2.9 m/s). It then started drifting left toward the next lane, even though the route command was RIGHT and then STRAIGHT. Its front-left corner moved into actor 33, which was coming up alongside on the left, and the collision counted as a front, at-fault contact.
- lead_vehicle_2hz_hybrid_r2_046: turned_into_actor, policy at fault: yes. After hard braking behind the slower lead (actor 1, about a 5 m gap at 7.9 m/s), the ego drifted left onto the lane line even though the command was RIGHT. Its front-left corner then hit actor 33, which was coming up from behind in the left lane.
- lead_vehicle_2hz_hybrid_r2_047: turned_into_actor, policy at fault: yes. After braking hard behind lead car 1, the ego slowly drifted left across the lane line, even though the route command was RIGHT. Its front clipped car 33, which was travelling alongside in the left lane, at 7.6 s. The lead car was 25 m ahead by then, so this was a lateral encroachment by the ego, not a failure to brake.
- lead_vehicle_2hz_hybrid_r2_048: turned_into_actor, policy at fault: yes. After handoff, the ego braked hard (from 7.9 to 3 m/s) for actor 1, which was close ahead. It then drifted left toward the adjacent lane, following a leftward plan even though the route said RIGHT and then STRAIGHT. At 7.6 s its front-left corner hit actor 33, which was coming up alongside in the left lane. By then the ego was about 12 m behind the recorded drive, and the replayed actor 33 was reaching the spot the ego had moved into.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_038, lead_vehicle_2hz_hybrid_r2_049)
- S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_hybrid_r2_027, lead_vehicle_2hz_hybrid_r2_031, lead_vehicle_2hz_hybrid_r2_032)
- S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75: 1/5 failed, rate 5%-56% (90%) (lead_vehicle_2hz_hybrid_r2_017, lead_vehicle_2hz_hybrid_r2_024, lead_vehicle_2hz_hybrid_r2_025, lead_vehicle_2hz_hybrid_r2_036, lead_vehicle_2hz_hybrid_r2_037)
- S4: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_014)
- S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_005)
- S6: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (lead_vehicle_2hz_hybrid_r2_040, lead_vehicle_2hz_hybrid_r2_043, lead_vehicle_2hz_hybrid_r2_044, lead_vehicle_2hz_hybrid_r2_045)
- S7: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_033, lead_vehicle_2hz_hybrid_r2_039)
- S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_010)
- S9: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_hybrid_r2_004, lead_vehicle_2hz_hybrid_r2_008, lead_vehicle_2hz_hybrid_r2_019)
- S10: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_020)
- S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_016)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_013, lead_vehicle_2hz_hybrid_r2_028)
- S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_006)
- S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_2hz_hybrid_r2_042, lead_vehicle_2hz_hybrid_r2_046, lead_vehicle_2hz_hybrid_r2_047, lead_vehicle_2hz_hybrid_r2_048)
- S15: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_035, lead_vehicle_2hz_hybrid_r2_041)
- S16: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_007)
- S17: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_001)
- S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_2hz_hybrid_r2_026, lead_vehicle_2hz_hybrid_r2_029, lead_vehicle_2hz_hybrid_r2_030)
- S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75: 2/3 failed, rate 25%-92% (90%) (lead_vehicle_2hz_hybrid_r2_015, lead_vehicle_2hz_hybrid_r2_022, lead_vehicle_2hz_hybrid_r2_023)
- S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_012, lead_vehicle_2hz_hybrid_r2_018)
- S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_003)
- S22: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_034)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_011)
- S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_r2_002_a2, lead_vehicle_2hz_hybrid_r2_009)
- S25: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_r2_021)

## Not kept by the gate

- lead_vehicle_2hz_hybrid_r2_002: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Copied from studies/lead_vehicle/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
