# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: four challenging settings were confirmed, each on a different scene, against the five asked for. They are 0e899dd3 at 2x speed (S14), 096988dd at 2x (S7), 023b7fcc at 1.25x (S1) and 09a95ffa at 1.25x (S8), all with the recorded timing (0 s shift). Each failure range sits above one half, but the lower bounds only just clear it. S7 does not show a policy weakness. In every failure there, a replayed car sped up from behind and drove through the ego before the policy took control, which is the kind of rear hit the brief says to ignore. That leaves three cases that are the policy's fault. In those, the policy mostly drifted or changed lanes to the left on its own and hit a car in the next lane, rather than failing to handle a car cutting in. No timing shift caused a failure in any setting we tried, so speeding the other cars up is the only part of the retiming that broke the policy.

## Findings

- In 023b7fcc at 1.25x speed and 0 s shift, every run failed. Each time the policy started a left lane change that the human never made (the route said straight, then right), sped up, and hit the car alongside it in the left lane. The policy was at fault.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r2_004, cut_in_merge_hybrid_r2_010, cut_in_merge_hybrid_r2_011)
- In 09a95ffa at 1.25x speed and 0 s shift, every run failed. The policy drifted or changed lanes to the left into a car coming up in the left lane, with a clear gap ahead. In one run it is unclear whether the ego drifted or the replayed car squeezed it.
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r2_007, cut_in_merge_hybrid_r2_012, cut_in_merge_hybrid_r2_013)
- In 0e899dd3 at 2x speed and 0 s shift, every run failed. In most runs the ego slowed and drifted left into a slow car in the next lane. In one run that car cut in ahead and the ego braked too gently, which is the only true cut-in failure in the study. The two slower speeds tried in this scene had no failures.
  - S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r2_022, cut_in_merge_hybrid_r2_031, cut_in_merge_hybrid_r2_032, cut_in_merge_hybrid_r2_033)
  - S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_009)
  - S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_016, cut_in_merge_hybrid_r2_021_a2)
- In 096988dd, the 2x speed setting counts as confirmed, but none of its failures were the policy's. A replayed car sped up from behind, hit the ego's rear and drove through it before the 4.7 s handoff, so the overlap was scored as a front collision. The slower speeds had no failures. This case shows a limit of retiming replayed traffic, not a policy weakness.
  - S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r2_024, cut_in_merge_hybrid_r2_028, cut_in_merge_hybrid_r2_029, cut_in_merge_hybrid_r2_030)
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_005)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_017, cut_in_merge_hybrid_r2_023)
- 19f339ba at 1.5x is the fifth-scene candidate. It failed repeatedly, every time from the policy drifting left into a passing small vehicle, but its failure range spans one half, so it was not confirmed.
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 4/11 failed, rate 18%-61% (90%) (cut_in_merge_hybrid_r2_039, cut_in_merge_hybrid_r2_040, cut_in_merge_hybrid_r2_046, cut_in_merge_hybrid_r2_047, cut_in_merge_hybrid_r2_048, cut_in_merge_hybrid_r2_049, cut_in_merge_hybrid_r2_050, cut_in_merge_hybrid_r2_051, cut_in_merge_hybrid_r2_052, cut_in_merge_hybrid_r2_053, cut_in_merge_hybrid_r2_054)
  - S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_006)
- In 054b5901, the triage describes failures at 1.5x that were again a replayed car driving through the ego from behind at handoff. The table still records no failures for that setting, so these runs were scored differently from S7. No speed tried in this scene produced a failure that was the policy's.
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r2_018, cut_in_merge_hybrid_r2_019, cut_in_merge_hybrid_r2_020)
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_008)
  - S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_037, cut_in_merge_hybrid_r2_038)
- Shifting the cut-in car earlier or later by up to 1 s, at 1.25x to 2x speed, caused no failures in 12855a41, 1c45ce3a or 0cf6368d (the three scenes where only the marked cut-in car was retimed). Each setting there ran once or twice, so these are hints that the settings are safe, not rates.
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_026)
  - S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_002, cut_in_merge_hybrid_r2_025)
  - S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_014)
  - S18: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_036)
  - S19: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_043)
  - S20: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_044)
  - S23: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_041)
  - S24: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_003, cut_in_merge_hybrid_r2_027)
  - S25: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_015)
  - S26: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_034)
  - S27: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_042)
  - S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_001)
  - S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_035)
  - S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_045)

## Open

- S7 and S3 were scored differently: failures where a replayed car drove through the ego from behind count as failures in S7 but not in S3. If rear hits are excluded as the brief asks, S7 drops out and only three cases remain confirmed. That scoring rule needs to be settled.
- Whether 19f339ba at 1.5x fails more than half the time is unsettled. More repeats there, or trying 2x in that scene, would decide it.
- S1 and S8 were never run at 1.0x with replay traffic, so we cannot tell whether the 1.25x speed-up causes those left drifts or whether the policy drifts there anyway. Repeats at 1.0x and 0 s in 023b7fcc and 09a95ffa would settle it.
- Timing shifts beyond ±1 s were never tried, and shifts were tried only in 12855a41 and 1c45ce3a. Shifts of ±1.5 to 2 s in the three scenes with a marked cut-in car would test whether timing matters at all.
- Most failures are the policy changing lanes on its own, not reactions to a car cutting in. This study does not show which car timings defeat the policy's response to a real cut-in.

## Why the runs failed (triage from the video and log)

turned_into_actor 12, actor_hit_ego 8, no_brake_for_lead 1

- cut_in_merge_hybrid_r2_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT/RIGHT command, the policy planned a lane change to the left that the human never made, and sped up from 4.2 to 6.0 m/s. It cut into the adjacent left lane and its front hit actor 56, which was travelling alongside and slightly ahead in that lane.
- cut_in_merge_hybrid_r2_007: actor_hit_ego, policy at fault: unclear. The ego was cruising straight on the freeway at about 8 m/s with a clear gap of over 24 m ahead. Actor 33 came up from behind in the lane to the left and, as it passed, its right side touched the ego's front-left corner. The ego was only 0.9 m off the recorded human path, so it is unclear whether the ego drifted slightly left into the passing car or the replayed car squeezed it; the smear in the camera happens only at the moment of impact.
- cut_in_merge_hybrid_r2_010: turned_into_actor, policy at fault: yes. After handoff the policy planned and steered a lane change to the left on a straight multi-lane highway, while the route said STRAIGHT and later RIGHT. It cut into the next lane while vehicle 56 was right beside it there, and the ego's front-left corner hit 56 at about 6 m/s.
- cut_in_merge_hybrid_r2_011: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the policy planned a lane change to the left when it should have stayed in its lane. It sped up from 4.2 to 6.0 m/s and steered into the lane where vehicle 56 was driving alongside it, hitting that car with its front-left corner.
- cut_in_merge_hybrid_r2_012: turned_into_actor, policy at fault: yes. On a multi-lane freeway with the STRAIGHT command, the policy planned a drift to the left (orange path) instead of following the recorded straight path (green line). It moved about 0.9 m left, and its front corner hit actor 33, which was coming up in the adjacent left lane. The lead vehicle stayed about 25 m ahead the whole time, so this was not a following failure.
- cut_in_merge_hybrid_r2_013: turned_into_actor, policy at fault: yes. After handoff, with the command at STRAIGHT and then RIGHT, the policy planned and began a lane change to the left at about 8 m/s. It moved into the adjacent left lane just as vehicle 33 was coming up from behind on the left, and the two collided side by side at 6.2 s. There was no slow lead vehicle; the gap ahead stayed around 25 m.
- cut_in_merge_hybrid_r2_018: actor_hit_ego, policy at fault: no. The ego was replaying the logged human path (0.0 m off the recording) at about 14 m/s. Actor 36 came up from directly behind in the same lane and drove through the ego's box, ending up overlapping its front. Because the replayed actor and the ego were in the same space, this was scored as a front collision at 4.7 s, the same moment as handoff, so the policy never had a chance to act.
- cut_in_merge_hybrid_r2_019: actor_hit_ego, policy at fault: no. The ego was still replaying the recorded drive straight down its lane at about 14 m/s, with no offset from the log, when actor 16 came up from directly behind in the same lane at 3.7 s. By 4.7 s, the moment the policy took over, actor 16 overlapped the ego's front and was scored as a front collision. The policy never had control before contact, so this looks like the replayed actor driving through the ego's box, not a policy error.
- cut_in_merge_hybrid_r2_020: actor_hit_ego, policy at fault: no. The ego was going straight at about 14 m/s, still replaying the recorded drive. Actor 16 was right behind it at 3.7 s, and by 4.7 s it had driven up through the ego and overlapped its front (1.6 m gap), which the metrics counted as a front collision. This happened at the exact moment of handoff (4.7 s), so the policy never had control before the contact.
- cut_in_merge_hybrid_r2_022: turned_into_actor, policy at fault: yes. After handoff, the ego slowed from 6.5 to 3.1 m/s. It drifted about 1.4 m left of the recorded path, into the lane of actor 23, a slow vehicle just ahead-left, and hit it with its front at 7.8 s (the gap ahead had shrunk to 4.4 m). Actor 23 was heavily smeared in the camera the whole time, but it was still recognisable as a car. The ego was also rear-ended at some point.
- cut_in_merge_hybrid_r2_024: actor_hit_ego, policy at fault: no. Before the policy took over, actor 9 came up from behind in the ego's lane and hit its rear (rear collision at 3.7 s, while the ego was still replaying the log at about 5 m/s). By the 4.7 s handoff, actor 9 was driving through the ego's box, so the overlap got flagged as a front, at-fault collision at the first moment the policy was in control. The camera smear in that frame comes from the overlap.
- cut_in_merge_hybrid_r2_028: actor_hit_ego, policy at fault: no. Actor 9 came up from behind in the ego's lane and was already hitting the ego's rear at 3.7s (collision_rear=1), before the policy took over at 4.7s. It kept going through the ego, so by 4.7s it covered the ego's front and a front collision was logged at the handoff instant. Nothing was ahead in the lane (the lead was about 44 m away), so the ego was hit by a replayed actor and had no time to react.
- cut_in_merge_hybrid_r2_029: actor_hit_ego, policy at fault: no. The ego was driving straight in its lane on the recorded path while actor 9 came up fast from behind. Actor 9 hit the ego's rear by 3.7s, before the policy took over, then drove through the ego, so by 4.7s it fully overlapped the ego and a front collision was registered.
- cut_in_merge_hybrid_r2_030: actor_hit_ego, policy at fault: no. The ego was driving straight in its lane, replaying the recorded trajectory (0.0 m off) and speeding up gently, with the nearest car ahead 25–44 m away. Actor 9 came up from behind: it was already touching the ego's rear at 3.7 s, a second before handoff, and by 4.7 s it had driven through the ego and overlapped its front. That overlap is why a front collision was flagged at the moment of handoff, and the 0.5 m "gap ahead" is actor 9, not a lead vehicle.
- cut_in_merge_hybrid_r2_031: turned_into_actor, policy at fault: yes. On a congested highway, the ego drifted left out of its lane, away from the recorded path, even though the route command was STRAIGHT and then RIGHT. Its front hit actor 23, a slow vehicle in the adjacent left lane, at about 3 m/s. The rear contact recorded in the run came after this.
- cut_in_merge_hybrid_r2_032: turned_into_actor, policy at fault: yes. After handoff, the ego slowed and drifted left across the lane line even though the command was RIGHT. Its front hit the rear of actor 23, which was driving normally in the adjacent left lane ahead (gap about 4.4 m, ego at 3 m/s).
- cut_in_merge_hybrid_r2_033: no_brake_for_lead, policy at fault: unclear. On the multi-lane highway, actor 23 cut in from the left into the ego's lane just ahead. The ego was told to go RIGHT and its plan pointed right, but it stayed in its lane (the human had already moved one lane right), braked only gently (3.7→2.9 m/s while the gap fell from 7.7 to 4.4 m), and its front hit 23. It was also rear-ended at some point.
- cut_in_merge_hybrid_r2_040: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego drove unusually slowly (about 4–5 m/s) while its planned path veered left of the route, drifting about 1.6 m off the recorded trajectory toward the left lane line. Vehicle 29 was passing on the left, and the ego sideswiped it (lateral collision) at 11.8 s.
- cut_in_merge_hybrid_r2_046: turned_into_actor, policy at fault: yes. On a straight highway with a STRAIGHT command, the ego was going only about 4 m/s and its plan kept bending left of the recorded path, so it drifted across the lane line into the lane on its left. A small vehicle (actor 29, which looks like a motorcycle) came up in that lane from behind and was hit by the ego's front-left corner.
- cut_in_merge_hybrid_r2_048: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was going slowly (about 4–5 m/s) and its planned path wandered to the left, so it ended up about 1.5 m off the recorded human path. A small actor (29) passing in the adjacent left lane then side-swiped the ego's front-left corner, which was logged as a lateral at-fault collision with no braking issue for a lead vehicle.
- cut_in_merge_hybrid_r2_053: turned_into_actor, policy at fault: yes. The ego was moving slowly on a multi-lane highway, about 4–5 m/s. Its planned path bent left, and it drifted across the lane line toward the left lane. While it was straddling the line, its front-left corner hit actor 29, a small vehicle passing in the adjacent left lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r2_004, cut_in_merge_hybrid_r2_010, cut_in_merge_hybrid_r2_011)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_008)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r2_018, cut_in_merge_hybrid_r2_019, cut_in_merge_hybrid_r2_020)
- S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_037, cut_in_merge_hybrid_r2_038)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_005)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_017, cut_in_merge_hybrid_r2_023)
- S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r2_024, cut_in_merge_hybrid_r2_028, cut_in_merge_hybrid_r2_029, cut_in_merge_hybrid_r2_030)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r2_007, cut_in_merge_hybrid_r2_012, cut_in_merge_hybrid_r2_013)
- S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_001)
- S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_035)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_045)
- S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_009)
- S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_016, cut_in_merge_hybrid_r2_021_a2)
- S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r2_022, cut_in_merge_hybrid_r2_031, cut_in_merge_hybrid_r2_032, cut_in_merge_hybrid_r2_033)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_026)
- S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_002, cut_in_merge_hybrid_r2_025)
- S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_014)
- S18: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_036)
- S19: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_043)
- S20: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_044)
- S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_006)
- S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 4/11 failed, rate 18%-61% (90%) (cut_in_merge_hybrid_r2_039, cut_in_merge_hybrid_r2_040, cut_in_merge_hybrid_r2_046, cut_in_merge_hybrid_r2_047, cut_in_merge_hybrid_r2_048, cut_in_merge_hybrid_r2_049, cut_in_merge_hybrid_r2_050, cut_in_merge_hybrid_r2_051, cut_in_merge_hybrid_r2_052, cut_in_merge_hybrid_r2_053, cut_in_merge_hybrid_r2_054)
- S23: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_041)
- S24: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r2_003, cut_in_merge_hybrid_r2_027)
- S25: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_015)
- S26: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_034)
- S27: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r2_042)

## Not kept by the gate

- cut_in_merge_hybrid_r2_021: not kept: RE-RUN

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
