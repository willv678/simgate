# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_optuna_r2`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only 2 of the 5 settings were confirmed, and only one of those clearly shows a weakness in the policy. Scene 023b7fcc with the cars 1 s later and 1.5x faster (S2) failed every time it was repeated. In each failure the ego's front hit car 56 in the left lane: in some runs the policy steered left out of its lane on its own, and in the others car 56 cut right in front of it. Scene 19f339ba with the cars 2 s later and 1.5x faster (S23) also failed every time, but the video review blames none of those failures on the policy. The lead car's replayed track jumps onto the ego, or a car behind drives into it at its recorded speed. S23 should be read as a fault in the traffic replay, not a challenging case. None of the other seven scenes failed at any setting tried, and the few settings repeated there kept the failure rate below one half.

## Findings

- On scene 023b7fcc, with the cars 1 s later and 1.5x faster, every repeat collided and the failure rate is surely above one half. The video review shows the policy at fault in some runs: on a STRAIGHT command it changed lanes left on its own and hit car 56. In the other runs car 56 cut right across the lane line into the ego, and fault is unclear. 2 Hz planning did not stop this left drift on this scene.
  - S2: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_023, cut_in_merge_2hz_hybrid_optuna_r2_028, cut_in_merge_2hz_hybrid_optuna_r2_029, cut_in_merge_2hz_hybrid_optuna_r2_030)
- On scene 19f339ba, with the cars 2 s later and 1.5x faster, every repeat registered a front collision. The video review clears or questions the policy in every run. Lead car 18 jumps from about 36 m ahead onto the ego within half a second, which is physically impossible and looks like a replay or ID-swap glitch, or car 28 comes from behind and hits the ego. The ego had braked well below the recorded speed, so it was behind where the human car had been. The rule counts this as confirmed, but it does not show a weakness in the policy.
  - S23: 19f339ba at actor_time_shift_s 2, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_009, cut_in_merge_2hz_hybrid_optuna_r2_010, cut_in_merge_2hz_hybrid_optuna_r2_011, cut_in_merge_2hz_hybrid_optuna_r2_012)
- On scene 023b7fcc, a nearby setting (1.5 s later, 1.25x speed) failed in its single run: on a RIGHT command the policy edged right into a slower car and barely braked. That one run is a hint, not a rate, and it is flagged as a possible simulator artifact.
  - S3: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r2_024)
- On scene 023b7fcc, the cars 2 s earlier at recorded speed did not cause a failure, so in this scene the danger lies with the cars later and faster.
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_008, cut_in_merge_2hz_hybrid_optuna_r2_018)
- Settings that came close but were repeated without any failure are surely below a one-half failure rate. These are scene 0e899dd3 (1 s earlier, 2x speed), scene 12855a41 (1.5 s earlier, 2x speed), scene 054b5901 (0.5 s later at 1.5x, and 1 s later at 2x), scene 096988dd (2 s later, 1.5x) and scene 1c45ce3a (0.5 s later, 2x).
  - S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_006, cut_in_merge_2hz_hybrid_optuna_r2_017, cut_in_merge_2hz_hybrid_optuna_r2_033, cut_in_merge_2hz_hybrid_optuna_r2_052)
  - S20: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_005, cut_in_merge_2hz_hybrid_optuna_r2_013, cut_in_merge_2hz_hybrid_optuna_r2_014, cut_in_merge_2hz_hybrid_optuna_r2_051)
  - S5: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_002, cut_in_merge_2hz_hybrid_optuna_r2_015, cut_in_merge_2hz_hybrid_optuna_r2_016)
  - S6: 054b5901 at actor_time_shift_s 1, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_046, cut_in_merge_2hz_hybrid_optuna_r2_047, cut_in_merge_2hz_hybrid_optuna_r2_048)
  - S9: 096988dd at actor_time_shift_s 2, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_036, cut_in_merge_2hz_hybrid_optuna_r2_041, cut_in_merge_2hz_hybrid_optuna_r2_054)
  - S26: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_027, cut_in_merge_2hz_hybrid_optuna_r2_031, cut_in_merge_2hz_hybrid_optuna_r2_032)
- Scenes 09a95ffa and 0cf6368d had no failures in a few runs each, with no setting repeated enough to rule one out.
  - S10: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_004)
  - S11: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_043)
  - S12: 09a95ffa at actor_time_shift_s 2, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_021, cut_in_merge_2hz_hybrid_optuna_r2_042)
  - S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_007, cut_in_merge_2hz_hybrid_optuna_r2_034)
  - S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_025)
  - S15: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_037)

## Open

- Three more cases are missing. On seven of the nine scenes no setting caused a failure, so the study cannot say whether those scenes break at 2 Hz within the knob ranges or the search just missed the right settings.
- S23 depends on whether car 18's track in scene 19f339ba is corrupt. That should be checked in the replay log, or with a run where car 18 is removed or not retimed, before S23 is counted as a challenging case.
- S3 (023b7fcc, 1.5 s later, 1.25x) rests on one run flagged as a possible artifact. It would need about three more repeats, though the rules allow only one case per scene and 023b7fcc already has S2.
- The near miss at S1 (023b7fcc, 2 s earlier) and the single-run settings with close approaches, S21, S22, S24 and S25 on 12855a41 and 1c45ce3a, were not followed up. A few probes next to them could still turn up failures.
- The comparison with the 10 Hz study cut_in_merge needs that study's results side by side. These results show only that left drift into the adjacent lane still causes collisions at 2 Hz on 023b7fcc.
- The scene tags don't say whether the ego is merging or another car is cutting in, and on six scenes every car was retimed. So these results cannot pin a failure on the car that changes lanes.

## Why the runs failed (triage from the video and log)

actor_hit_ego 4, turned_into_actor 3, other 2

- cut_in_merge_2hz_hybrid_optuna_r2_009: other, policy at fault: no. The ego was going straight in its lane and braking from 17 to 9 m/s, so the lead car (actor 18) pulled away, from 12.7 m to 36 m ahead. Then, between 6.6 s and 7.1 s, actor 18 jumped from about 36 m ahead to overlapping the ego (gap 1.4 m), which looks like a glitch or ID swap in the replayed actor track, not real motion, and this registered as a front collision.
- cut_in_merge_2hz_hybrid_optuna_r2_010: actor_hit_ego, policy at fault: unclear. The ego stayed in its highway lane but slowed from about 17 to 9.4 m/s with no close lead, ending up about 12 m behind where the human car was at that moment. At 7.1 s, actor 18 (tracked earlier as the lead about 36 m ahead) shows up overlapping the ego's front-right as a car merging in from the right lane. That looks like a replayed actor, or a track-ID jump, moving into space the human car had already left; the ego never steered into it.
- cut_in_merge_2hz_hybrid_optuna_r2_011: other, policy at fault: unclear. After handoff, the ego braked steadily on a straight highway (17.1 to 8.8 m/s) while lead actor 18 pulled away to 36 m. Then within half a second actor 18 jumped onto the ego's position, overlapping its front-right (gap 36.2 to 1.5 m). That is physically impossible, so it looks like a replay or tracking teleport of the logged actor, probably made worse by the ego sitting about 13 m behind where the recorded car was.
- cut_in_merge_2hz_hybrid_optuna_r2_012: actor_hit_ego, policy at fault: unclear. After handoff, the ego braked hard on an open highway lane (17 to 8 m/s, with nothing within about 59 m ahead at 6.6 s). It also drifted about 0.8 m left of the recorded path. At 7.1 s a vehicle coming up from behind (id 28) ran into the ego's right-front side and rear while still driving at its recorded speed. The impact was counted as an at-fault front collision, but the ego was hit by an actor that did not react to it.
- cut_in_merge_2hz_hybrid_optuna_r2_023: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy steered left out of its lane, away from the recorded path, while speeding up from 4.5 to 6.8 m/s. Its front hit vehicle 56, which was driving in the adjacent left lane just ahead and beside it. A trailing actor also touched the ego's rear, but only after the front collision began.
- cut_in_merge_2hz_hybrid_optuna_r2_024: turned_into_actor, policy at fault: yes. Following the RIGHT command in dense, slow highway traffic, the ego edged right into the lane of actor 15, a slower car just ahead and to its right. The gap fell from 28 m to 10.6 m once 15 counted as the car ahead, then shrank to 4.7 m, but the ego only slowed from 6.7 to 6.0 m/s and hit 15 with its front.
- cut_in_merge_2hz_hybrid_optuna_r2_028: actor_hit_ego, policy at fault: unclear. The ego kept to its lane and sped up gently from 4.5 to 6.8 m/s while the recorded human drifted left. Replayed actor 56, in the lane to the left and slightly ahead, moved right across the lane line into the ego's path, and the ego's front-left clipped it (the gap to the actor ahead fell from 21.8 m to 3.6 m). The ego was also struck from behind at some point in the run.
- cut_in_merge_2hz_hybrid_optuna_r2_029: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT/RIGHT command, the policy planned and started an unprompted lane change to the left while speeding up from 4.2 to 6.7 m/s. Its front then hit actor 56, which was travelling in the adjacent left lane just ahead; the recorded human drive stayed in its lane.
- cut_in_merge_2hz_hybrid_optuna_r2_030: actor_hit_ego, policy at fault: unclear. The ego stayed in its lane on a multi-lane road and sped up from 4.2 to 6.8 m/s, while the recorded human path drifted left. Actor 56 came up from behind on the left, passed the ego and cut right into the ego's lane just ahead of it, and the ego's front corner clipped 56 at 7.2 s (the gap to the actor ahead fell from 21.8 m to 3.6 m). Separately, something also hit the ego's rear.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_008, cut_in_merge_2hz_hybrid_optuna_r2_018)
- S2: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_023, cut_in_merge_2hz_hybrid_optuna_r2_028, cut_in_merge_2hz_hybrid_optuna_r2_029, cut_in_merge_2hz_hybrid_optuna_r2_030)
- S3: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r2_024)
- S4: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_044)
- S5: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_002, cut_in_merge_2hz_hybrid_optuna_r2_015, cut_in_merge_2hz_hybrid_optuna_r2_016)
- S6: 054b5901 at actor_time_shift_s 1, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_046, cut_in_merge_2hz_hybrid_optuna_r2_047, cut_in_merge_2hz_hybrid_optuna_r2_048)
- S7: 054b5901 at actor_time_shift_s 2, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_035)
- S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_003, cut_in_merge_2hz_hybrid_optuna_r2_026)
- S9: 096988dd at actor_time_shift_s 2, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_036, cut_in_merge_2hz_hybrid_optuna_r2_041, cut_in_merge_2hz_hybrid_optuna_r2_054)
- S10: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_004)
- S11: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_043)
- S12: 09a95ffa at actor_time_shift_s 2, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_021, cut_in_merge_2hz_hybrid_optuna_r2_042)
- S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_007, cut_in_merge_2hz_hybrid_optuna_r2_034)
- S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_025)
- S15: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_037)
- S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_006, cut_in_merge_2hz_hybrid_optuna_r2_017, cut_in_merge_2hz_hybrid_optuna_r2_033, cut_in_merge_2hz_hybrid_optuna_r2_052)
- S17: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_049, cut_in_merge_2hz_hybrid_optuna_r2_050)
- S18: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_045)
- S19: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_019)
- S20: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_005, cut_in_merge_2hz_hybrid_optuna_r2_013, cut_in_merge_2hz_hybrid_optuna_r2_014, cut_in_merge_2hz_hybrid_optuna_r2_051)
- S21: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_022)
- S22: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_038)
- S23: 19f339ba at actor_time_shift_s 2, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_009, cut_in_merge_2hz_hybrid_optuna_r2_010, cut_in_merge_2hz_hybrid_optuna_r2_011, cut_in_merge_2hz_hybrid_optuna_r2_012)
- S24: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_040)
- S25: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_001)
- S26: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_027, cut_in_merge_2hz_hybrid_optuna_r2_031, cut_in_merge_2hz_hybrid_optuna_r2_032)
- S27: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_020)
- S28: 1c45ce3a at actor_time_shift_s 2, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r2_039, cut_in_merge_2hz_hybrid_optuna_r2_053)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
