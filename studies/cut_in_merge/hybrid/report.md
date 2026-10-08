# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid`: 27 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 3 rounds.

## Answer

The study's check counts five settings as confirmed, all at the recorded timing (0 s shift) with the other cars at 1.25x speed (S1, S2, S6, S9, S13). Each range sits above one half, but each rests on only a few repeats. The videos show that only two of these are real policy failures. In 023b7fcc (S1) and 09a95ffa (S6), every repeat failed the same way: the ego was told to go STRAIGHT, steered left into the next lane anyway, and hit a car driving alongside. The other three don't count as policy collisions. In 054b5901 (S2), the ego starts the run already overlapping another car. In 19f339ba (S13), a replayed car hits the ego from behind, which the plan said to ignore. In 0e899dd3 (S9), a replayed car hits the ego from behind or the side after the ego slows for no clear reason. So the study supports two challenging cases, not five, and it does not show that the timing or speed change caused even those two, because no run used the recorded timing and speed as a baseline.

## Findings

- In 023b7fcc at 0 s and 1.25x, every repeat failed the same way and the policy was at fault. With a STRAIGHT command, the ego sped up, steered left into the next lane and hit vehicle 56 alongside it, while the recorded human path stayed in its lane.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_004, cut_in_merge_hybrid_010, cut_in_merge_hybrid_011)
- In 09a95ffa at 0 s and 1.25x, every repeat failed and the policy was at fault. The ego drifted left with a STRAIGHT/RIGHT command and its front-left corner hit vehicle 33 in the left lane. The car ahead stayed about 25 m away, so this was not a failure to brake.
  - S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_007, cut_in_merge_hybrid_015, cut_in_merge_hybrid_014_a2)
- The failures counted in 054b5901 at 0 s and 1.25x are not driving failures. Every one was flagged in the first frame, before the policy acted, with a recorded actor's box already overlapping the ego and no car visible on camera. This looks like a setup or reconstruction artifact. The artifact flag missed it, so the setting counts as confirmed anyway.
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_008, cut_in_merge_hybrid_018, cut_in_merge_hybrid_019, cut_in_merge_hybrid_020, cut_in_merge_hybrid_021)
- In 19f339ba at 0 s and 1.25x, every failure was actor 28 hitting the ego from behind while the ego held the recorded path with open road ahead. The contact was then logged as a front collision. These are rear-end hits the plan says to ignore, and the policy was not at fault.
  - S13: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_006, cut_in_merge_hybrid_012, cut_in_merge_hybrid_013)
- In 0e899dd3 at 0 s and 1.25x, the failures came from replayed actor 10 driving into the ego from behind or the right. That happened after the ego slowed for no clear reason with the car ahead about 25 m away. The policy shares the blame at most (fault judged no or unclear), so this is not a clear policy collision.
  - S9: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_009, cut_in_merge_hybrid_016, cut_in_merge_hybrid_017)
- In 096988dd, speeding the cars up to 1.5x brought a single failure: the ego slowed for no clear reason and a replayed follower clipped its side, with the fault unclear. At 1.25x, with and without a -0.5 s shift, it did not fail. One run is a hint, not a rate.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_hybrid_024)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_005)
  - S3: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_025)
- Scenes 0cf6368d, 12855a41 and 1c45ce3a, the three where only the marked cut-in car was retimed, did not fail at 1.25x or 1.5x, or at -0.5 s in 12855a41. Each of these settings has a single run, so this does not show they are safe.
  - S7: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_001)
  - S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_026)
  - S10: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_023)
  - S11: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_002)
  - S12: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_022)
  - S14: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_003_a2)
  - S15: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_027)

## Open

- Whether retiming causes the failures at all: no setting at 0 s and 1.0x was run with replayed traffic. Running 023b7fcc and 09a95ffa at 0 s / 1.0x a few times each would show whether the left swerve happens without any speed-up.
- The timing knob was barely explored: only 0 s and -0.5 s were tried, and nothing beyond ±0.5 s or with a later shift. Speed was tried only at 1.25x and 1.5x, never slower than recorded.
- Three more real policy cases are still needed. Candidates: repeat 096988dd at 0 s / 1.5x (S5), and search 0cf6368d, 12855a41 and 1c45ce3a at larger shifts (±1 to ±2 s) and 2x speed, where the single runs came close.
- 054b5901 needs its initial overlap checked: was actor 150/156 placed on top of the ego by the 1.25x retiming or by the reconstruction itself? Until then the scene gives no evidence about the policy.
- The study cannot tell ego merges from cut-ins. Both policy failures were the ego changing lanes on its own, not another car cutting in.

## Why the runs failed (triage from the video and log)

actor_hit_ego 7, turned_into_actor 6, other 5

- cut_in_merge_hybrid_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT (RIGHT in the last frame), the ego sped up from 4.2 to 5.9 m/s while its planned path swung left toward the next lane. It cut left into vehicle 56, which was driving alongside it in that lane, and hit it with its front-left corner.
- cut_in_merge_hybrid_006: actor_hit_ego, policy at fault: no. The ego was going straight down the highway on the recorded human path, with the car ahead more than 25 m away and pulling further ahead. Vehicle 28 came up from behind in the same lane, hit the ego's rear at about 3.9s and drove into and through it by 4.9s, which the run recorded as a front collision; collision_at_fault is 0.
- cut_in_merge_hybrid_007: turned_into_actor, policy at fault: yes. On a multi-lane highway at a steady ~8 m/s, the ego drifted left toward the adjacent lane even though the route command was STRAIGHT and then RIGHT. Its nose hit vehicle 33, which was travelling alongside in that left lane. The lead vehicle was about 25 m ahead the whole time, so braking was not the issue. The camera smear in the last frame happens at impact and did not cause the mistake.
- cut_in_merge_hybrid_008: other, policy at fault: no. The front collision was flagged at t=0.0s, the first frame of the run, before the policy had acted. On the map, actor 150 already overlaps the front-right of the ego's box. The camera shows no vehicle directly ahead. This points to a setup or initialization artifact (the actor starts overlapping the ego), not a driving mistake.
- cut_in_merge_hybrid_009: actor_hit_ego, policy at fault: unclear. The ego was going straight in a highway lane. It slowed from 5.0 to 2.6 m/s even though the nearest car ahead was 25–28 m away, so it fell more than 7 m behind where the human driver had been. Actor 10, a replayed car following from behind in the same lane (it was just behind the ego at 7.7s), caught up and ran into the ego; the box overlap at 8.7s is logged as a front/lateral collision, and rear contact had already been logged earlier in the run.
- cut_in_merge_hybrid_010: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a STRAIGHT command, the ego's plan (orange) swerved left toward the next lane, where vehicle 56 was driving right beside it. The ego cut into that lane anyway and sideswiped vehicle 56 at about 6 m/s, while the recorded human path (green) stayed in the original lane.
- cut_in_merge_hybrid_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the ego planned a lane change to the left (orange path) and sped up from 4.2 to 5.8 m/s. It moved into the left lane while vehicle 56 was right beside it and slightly ahead, and its front corner hit vehicle 56 at 6.7 s.
- cut_in_merge_hybrid_012: actor_hit_ego, policy at fault: no. The ego was going straight down its highway lane on the recorded path, easing off from 18.4 to 15.8 m/s with a clear and growing gap ahead (26→42 m). Actor 28 came up from behind and rear-ended it at about 3.9 s, then drove through the ego's box; that overlap triggered the front/lateral collision flag at 4.9 s, and the sim scored it not at fault.
- cut_in_merge_hybrid_013: actor_hit_ego, policy at fault: no. The ego was going straight in its lane on the highway at about 17 m/s, staying on the recorded human path (0.0–0.14 m off), with no actor near it ahead. At 3.9 s actor 28 drove into the ego from behind, which registered as a rear collision. By 4.9 s actor 28 had moved up through the ego's box and overlapped its front, which is why the run shows a front collision even though the ego was not closing on anything.
- cut_in_merge_hybrid_015: turned_into_actor, policy at fault: yes. On a multi-lane freeway at about 8 m/s, the ego's planned path bent left toward the next lane, even though the route command was STRAIGHT. The ego drifted left and its front-left corner struck vehicle 33, which was coming up alongside in that left lane. The recorded trajectory stayed in the ego's own lane. The smeared camera view only appears at the moment of impact.
- cut_in_merge_hybrid_016: actor_hit_ego, policy at fault: no. The ego was going straight in heavy freeway traffic and slowed from 5.0 to 2.6 m/s, even though the nearest car ahead in its lane was about 25 m away. That left it about 7.5 m behind where the recorded car was at that moment. Actor 10, a replayed vehicle that came up from behind and to the right at 7.7 s, kept its recorded path, ran into the ego's space and overlapped it at 8.7 s, which the sim logged as a front collision.
- cut_in_merge_hybrid_017: actor_hit_ego, policy at fault: no. On a straight, congested highway, the ego slowed from 4.9 to 2.9 m/s even though the nearest car ahead was about 26 m away. That left it about 7 m behind where the recorded car was. Actor 10 is replayed from the recording and does not react to the ego; it came up from behind and slightly to the right, ran into the ego's box and overlapped it. So the impact was flagged as a front collision even though nothing was ahead of the ego in its lane (a rear collision had also been flagged earlier in the run).
- cut_in_merge_hybrid_018: other, policy at fault: no. The front collision was flagged at t=0.0s, the very first frame, so the policy never got to act. Actor 150 already overlaps the ego's front-right in the top-down map, but no vehicle shows up there in the front camera. This looks like a bad starting setup (an actor placed on top of the ego) or a spurious collision check: the run-wide collision values are 0.00 even though the per-frame value is 1.00.
- cut_in_merge_hybrid_014_a2: turned_into_actor, policy at fault: yes. On a straight multi-lane highway at about 8 m/s, the ego's plan bent left toward the neighbouring lane, away from the recorded path, which goes straight. The ego angled across the lane line and its front-left corner hit actor 33, which was passing alongside in the left lane.
- cut_in_merge_hybrid_019: other, policy at fault: no. The front collision was flagged at t=0.0 s, the run's first frame, before the policy had driven at all. On the map, actor 156's box already overlaps the right front of the ego's box, but the camera shows no vehicle directly ahead. This looks like an overlap left over from initialization or the recorded actor's box, not a driving mistake. The run-level Agg metrics also show 0 collisions.
- cut_in_merge_hybrid_020: other, policy at fault: no. The front collision was flagged at t=0.0s, the first frame, before the policy had controlled anything. On the map, actor 150 already overlaps the front-right of the ego box. The camera shows no vehicle in that spot, so this looks like the scenario started with the ego and actor 150 overlapping, not a driving mistake. Agg collision is 0.00 while Per-Ts collision_front is 1.00, which also suggests a setup glitch rather than a real crash.
- cut_in_merge_hybrid_021: other, policy at fault: no. The collision is flagged at t=0.0s, the first frame of the run, before the policy has controlled anything. On the map, actor 150 already overlaps the ego's right front at spawn. The camera shows no vehicle directly ahead in the lane, and the gap to the actor ahead is null. This looks like an overlap left over from how the scene was set up or reconstructed, not something the ego did; the whole-run (Agg) collision values even read 0.00 while the single-frame value reads 1.00.
- cut_in_merge_hybrid_024: actor_hit_ego, policy at fault: unclear. On the highway, the ego slowed from 5.7 to 4.1 m/s even though the lead was 26 m or more ahead, and it was starting a rightward drift toward the route (command RIGHT). Replayed actor 9 had been close behind it at 6.8 s. By 7.8 s, actor 9 came up along the ego's right side and overlapped it, causing a lateral contact (an earlier rear contact is also logged, and the metrics mark neither as the ego's fault). The ego's needless slowdown and its 1.8 m offset from the recorded path likely let the non-reactive follower catch up and clip it, so the blame is shared and the policy's fault is unclear.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_004, cut_in_merge_hybrid_010, cut_in_merge_hybrid_011)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_008, cut_in_merge_hybrid_018, cut_in_merge_hybrid_019, cut_in_merge_hybrid_020, cut_in_merge_hybrid_021)
- S3: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_025)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_005)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_hybrid_024)
- S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_007, cut_in_merge_hybrid_015, cut_in_merge_hybrid_014_a2)
- S7: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_001)
- S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_026)
- S9: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_009, cut_in_merge_hybrid_016, cut_in_merge_hybrid_017)
- S10: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_023)
- S11: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_002)
- S12: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_022)
- S13: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_006, cut_in_merge_hybrid_012, cut_in_merge_hybrid_013)
- S14: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_003_a2)
- S15: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_027)

## Not kept by the gate

- cut_in_merge_hybrid_003: not kept: RE-RUN
- cut_in_merge_hybrid_014: not kept: RE-RUN

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

29 of 29 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
