# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `rules`: 27 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 3 rounds.

## Answer

The code's check marks the goal as met: five settings on five different scenes failed in every repeat (S1, S2, S4, S6, S8). Each range sits just above one half. The triage, though, shows that only two of the five are the policy colliding. At S1 (023b7fcc) and S4 (09a95ffa), the policy steered left into the next lane and hit a car driving alongside. At S2, S6 and S8 the failures were not the policy's: in one scene a car overlapped the ego at the start, and in the other two replayed cars hit the ego from behind. The plan said to ignore rear-end hits on the ego, so read the result as two confirmed policy failures, not five. The study also never varied the timing or speed of the other cars. Every scene ran only at the recorded timing (0 s shift) with the other cars at 1.25x speed, so it cannot say which timings or speeds cause collisions, or whether the 1.25x speed matters at all.

## Findings

- In scene 023b7fcc, with the other cars at 1.25x speed and no time shift, every run ended with the policy steering left into the next lane while speeding up, against a STRAIGHT command, and hitting vehicle 56 alongside it. This is a real failure of the policy.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_004, cut_in_merge_rules_011, cut_in_merge_rules_019)
- In scene 09a95ffa, at the same setting, every run ended in a front-left contact with actor 33, which was coming up in the lane to the left. In two runs the policy's plan swung left and drifted into it. In the third run the ego made no clear move toward the car and fault is unclear. This is mostly the policy's failure.
  - S4: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_007, cut_in_merge_rules_013, cut_in_merge_rules_021)
- The failures in scene 054b5901 are not the policy's. In every run the front collision was flagged in the first frame, because actor 150 was placed overlapping the ego before the policy had driven at all. This looks like an error in setting up the scenario, even though no run was flagged as a possible artifact.
  - S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_008, cut_in_merge_rules_014, cut_in_merge_rules_022)
- The failures in scenes 0e899dd3 and 19f339ba were replayed cars running into the ego from behind and then overlapping its box, which set off the front-collision flag. The ego stayed in its lane. In 0e899dd3 it slowed well below the human's speed, which may have let the following car catch up, so fault there is unclear. These are rear-end hits that the plan said to ignore.
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_009, cut_in_merge_rules_015, cut_in_merge_rules_023)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_006, cut_in_merge_rules_012, cut_in_merge_rules_020)
- Three scenes never failed at this setting: 096988dd, 0cf6368d and 12855a41. Scene 1c45ce3a failed once, and that was a replayed car hitting the ego's right side after an earlier rear collision, so it was not the policy's fault.
  - S3: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_005, cut_in_merge_rules_017, cut_in_merge_rules_026)
  - S5: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_001, cut_in_merge_rules_018, cut_in_merge_rules_027)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_002, cut_in_merge_rules_016, cut_in_merge_rules_025)
  - S9: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_rules_003, cut_in_merge_rules_010, cut_in_merge_rules_024)
- Every setting the study ran used a 0 s time shift and 1.25x speed, so the results say nothing about how the timing or speed of the other cars changes the outcome.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_004, cut_in_merge_rules_011, cut_in_merge_rules_019)
  - S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_008, cut_in_merge_rules_014, cut_in_merge_rules_022)
  - S3: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_005, cut_in_merge_rules_017, cut_in_merge_rules_026)
  - S4: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_007, cut_in_merge_rules_013, cut_in_merge_rules_021)
  - S5: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_001, cut_in_merge_rules_018, cut_in_merge_rules_027)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_009, cut_in_merge_rules_015, cut_in_merge_rules_023)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_002, cut_in_merge_rules_016, cut_in_merge_rules_025)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_006, cut_in_merge_rules_012, cut_in_merge_rules_020)
  - S9: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_rules_003, cut_in_merge_rules_010, cut_in_merge_rules_024)

## Open

- Whether the policy's lane-change collisions in 023b7fcc and 09a95ffa depend on the retiming at all. Repeat both scenes at 1.0x speed with a 0 s shift, and at a few time shifts between -2 s and +2 s.
- Which timings and speeds make the policy fail. The study stopped after 3 rounds without searching the timing and speed ranges. Spend the rest of the budget (about 27 runs) on a grid of time shifts and speed scales over the scenes that did not show a policy failure.
- Three more scenes with failures caused by the policy itself. 054b5901 needs its setup overlap fixed (actor 150 at t=0), and 0e899dd3 and 19f339ba need the rear-end-and-overlap hits excluded. After that, search them and the scenes that never failed (096988dd, 0cf6368d, 12855a41, 1c45ce3a) at other settings.
- The collision check counts a car overlapping the ego from behind as a front collision, and the artifact flag missed the overlap at t=0. Both need fixing before the goal's count of confirmed cases can be trusted.
- Near misses were not ranked. Scenes 1c45ce3a and 12855a41 had high criticality without a failure caused by the policy and are the next places to look.

## Why the runs failed (triage from the video and log)

actor_hit_ego 8, turned_into_actor 5, other 3

- cut_in_merge_rules_003: actor_hit_ego, policy at fault: no. The ego was going straight in its highway lane, within 0.4 m of the recorded path, but slowing (10.1 to 8.4 m/s) and about 23 m behind where the human car was at that moment. Actor 24, a replayed vehicle that does not react to the ego, came up from behind on the right and moved into the ego's space, hitting its right side. A rear collision had already happened earlier in the run.
- cut_in_merge_rules_004: turned_into_actor, policy at fault: yes. The route said STRAIGHT and then RIGHT, but the ego planned and steered left into the next lane while speeding up from 4.2 to 5.8 m/s. Its front hit actor 56, which was driving in that lane next to it and slightly ahead. The camera only smeared at the moment of impact.
- cut_in_merge_rules_006: actor_hit_ego, policy at fault: no. The ego was driving straight down a multi-lane highway, staying on the recorded path and slowing gently from 18.4 to 15.8 m/s, with the car ahead far off and getting farther. Actor 28 came up behind it in the same lane and hit its rear at about 3.9 s. By 4.9 s actor 28 overlaps the ego's box, and that overlap is what set off the front-collision flag.
- cut_in_merge_rules_007: actor_hit_ego, policy at fault: unclear. On a multi-lane highway the ego held about 8 m/s, staying within 0.9 m of the recorded human path, with the lead car more than 24 m ahead. Actor 33 came up from behind in the lane to the left and closed in alongside the ego's front-left corner, where the contact was flagged as a front collision. The ego made no clear lateral move toward it, and the smeared car in the camera view at impact is from being so close.
- cut_in_merge_rules_008: other, policy at fault: no. The front collision was flagged at t=0.0 s, in the very first frame, before the policy had driven at all. On the map, actor 150's box already overlaps the right-front of the ego, but the camera shows no vehicle directly ahead. This looks like a problem with the scenario setup (an actor placed overlapping the ego, or an initial-state glitch), not a driving error.
- cut_in_merge_rules_009: actor_hit_ego, policy at fault: no. On a busy freeway with the STRAIGHT command, the ego stayed in its lane but slowed from 4.9 to 2.9 m/s. That left it about 7 m behind where the human driver was at the same moment. Actor 10 is a replayed car following its recorded path and does not react to the ego. It first hit the ego from behind (collision_rear), then moved into and over the ego's box from the rear-right, which the metric counted as a front collision. The real lead car was still about 26 m ahead and the planner metric shows collision_at_fault = 0.
- cut_in_merge_rules_011: turned_into_actor, policy at fault: yes. On a straight multi-lane highway (command STRAIGHT), the ego left its route line and steered left into the next lane while speeding up from 4.2 to 5.9 m/s, hitting vehicle 56 driving alongside in that lane. The gap fell from 21.5 m to 3.2 m only because the lane change made 56 the vehicle ahead, and the camera view was clean before impact.
- cut_in_merge_rules_012: actor_hit_ego, policy at fault: no. The ego was going straight in its highway lane and easing off from 18.4 to 15.8 m/s, with the lead vehicle well ahead (gap growing from 26 to 42 m). Replayed vehicle 28, following its recorded path, came up from behind, hit the ego's rear at about 3.9 s, then drove through the ego, which set the front-collision flag at 4.9 s; the ego never left its lane or the recorded path.
- cut_in_merge_rules_013: turned_into_actor, policy at fault: yes. At about 8 m/s on a multi-lane freeway with a STRAIGHT command, the ego's plan (orange) swung left toward the next lane. Actor 33 was coming up from behind in that lane, and the ego drifted about 0.9 m left of the human's path and hit it with its front-left corner. The camera smear at 6.2s comes from the impact itself, so it doesn't explain the mistake.
- cut_in_merge_rules_014: other, policy at fault: no. The front collision is flagged at t=0.0 s, the first frame, because actor 150 already overlaps the ego's right front on the map, while the camera shows clear road ahead. It looks like the actor was placed overlapping the ego when the scene was set up, not something the policy did. The Agg collision metrics are 0.00.
- cut_in_merge_rules_015: actor_hit_ego, policy at fault: unclear. The ego crept along in heavy highway traffic, slowing from 4.9 to 3.1 m/s even though the car ahead was 13–15 m away, so it ended up about 7 m behind where the human drove. Actor 10, which comes from behind on the right in the replay and does not react to the ego, drove up into the ego's spot and overlapped it at the right front. A rear collision had also already been flagged earlier in the run.
- cut_in_merge_rules_019: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's plan swung left toward the next lane while it sped up from 4.2 to 5.9 m/s. Vehicle 56 was driving alongside in that lane, and the ego cut into it. The recorded human path stayed in the ego's own lane.
- cut_in_merge_rules_020: actor_hit_ego, policy at fault: no. On a straight multi-lane highway, the ego stayed in its lane on the recorded path while easing off from 18.4 to 15.8 m/s, with the lead vehicle more than 25 m ahead and pulling away. Actor 28, a replayed vehicle behind it, kept going and ran into the ego from behind: a rear collision is logged at 3.9 s, and by 4.9 s its box overlaps the ego's, which also sets off the front-collision flag. The ego's slowing probably made the replayed car catch up, but the ego didn't hit anything itself and the metrics don't put the collision on it.
- cut_in_merge_rules_021: turned_into_actor, policy at fault: yes. At about 8 m/s on a multi-lane highway, the ego's planned path (orange) bent left toward the adjacent lane. The ego drifted about 0.9 m left of where the recorded car drove and clipped vehicle 33 with its front as 33 passed on the left. The lead car stayed about 25 m ahead the whole time, and the smeared camera image appears only at the moment of contact.
- cut_in_merge_rules_022: other, policy at fault: no. The front collision is logged at t=0.0 s, the very first frame, before the policy could do anything. Actor 150's box already overlaps the right front of the ego on the map, and the camera shows no vehicle there, so this looks like a scenario setup or actor-placement error, not a driving mistake. The run's whole-run offroad value is 1, but this frame shows no offroad (its per-frame value is 0), so that must have happened later and none of the frames show it.
- cut_in_merge_rules_023: actor_hit_ego, policy at fault: unclear. The ego was going straight in congested highway traffic with about 25 m of clear lane ahead, but slowed steadily from 5.0 to 2.5 m/s and fell about 7.5 m behind where the recorded car was. Actor 10 is replayed from the log and does not react, and it drove up from behind into the ego (an earlier rear contact, then the box overlaps the ego at 8.7 s, which sets the front flag). The ego did not drive into anything ahead.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_004, cut_in_merge_rules_011, cut_in_merge_rules_019)
- S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_008, cut_in_merge_rules_014, cut_in_merge_rules_022)
- S3: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_005, cut_in_merge_rules_017, cut_in_merge_rules_026)
- S4: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_007, cut_in_merge_rules_013, cut_in_merge_rules_021)
- S5: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_001, cut_in_merge_rules_018, cut_in_merge_rules_027)
- S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_009, cut_in_merge_rules_015, cut_in_merge_rules_023)
- S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_rules_002, cut_in_merge_rules_016, cut_in_merge_rules_025)
- S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_rules_006, cut_in_merge_rules_012, cut_in_merge_rules_020)
- S9: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_rules_003, cut_in_merge_rules_010, cut_in_merge_rules_024)

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

27 of 27 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
