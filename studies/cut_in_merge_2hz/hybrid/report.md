# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Code confirmed four settings on four different scenes (S1, S3, S7, S9), not the five asked for, and the video triage shows only one of them is clearly a policy error. At S1 (scene 023b7fcc, no time shift, cars at 1.25x speed), the policy drifted left out of its lane and hit a car driving alongside, even though it was told to go straight and the recorded human went right. So the left drift still causes collisions at 2 Hz planning. At S3 and S7, which speed the cars up to 1.5x and 2x, every failure was a replayed car from behind driving through the ego at the moment the policy took over. These are rear-end overlaps that were counted as front collisions, not policy failures, and the plan said to ignore rear-end hits. At S9 a replayed car overtook the ego and cut across into it; the triage could not say whether the policy was at fault. Each confirmed setting rests on only a few repeats, so their failure ranges are wide even though they clear one half.

## Findings

- At scene 023b7fcc with no time shift and cars at 1.25x speed, every run failed because the policy itself drifted left into the next lane and hit a car alongside, against a STRAIGHT command. This is the only confirmed setting where the policy is clearly at fault.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_004, cut_in_merge_2hz_hybrid_010, cut_in_merge_2hz_hybrid_011)
- At scene 054b5901 with cars at 1.5x speed, every run failed. In each one a replayed car from directly behind drove into the ego's box at the handoff, while the ego was still exactly on the recorded path. These are rear-end overlaps scored as front collisions, not policy failures. At 1.25x speed the same scene did not fail.
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_036, cut_in_merge_2hz_hybrid_037, cut_in_merge_2hz_hybrid_038, cut_in_merge_2hz_hybrid_039)
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_008)
- At scene 096988dd, only 2x speed failed, and every run there failed the same way: a replayed car from behind ran through the ego before the policy took control. Lower speeds and time shifts of plus or minus 0.5 s at this scene did not fail, though some came close.
  - S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_029, cut_in_merge_2hz_hybrid_040, cut_in_merge_2hz_hybrid_041, cut_in_merge_2hz_hybrid_042)
  - S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_030)
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_005, cut_in_merge_2hz_hybrid_018)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_027)
  - S8: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_031)
- At scene 09a95ffa with cars at 1.25x speed, every run failed. In each, replayed actor 33 overtook on the left and cut across the ego's front corner while the ego held its lane. The triage could not say whether the policy was at fault.
  - S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_007, cut_in_merge_2hz_hybrid_012, cut_in_merge_2hz_hybrid_013)
- Scenes 0e899dd3, 12855a41, 0cf6368d and 1c45ce3a never failed at any setting tried. Repeated runs at S18, S19 and S25 put their failure rates below one half.
  - S16: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_054)
  - S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_024)
  - S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_050, cut_in_merge_2hz_hybrid_051, cut_in_merge_2hz_hybrid_052, cut_in_merge_2hz_hybrid_053)
  - S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_hybrid_045, cut_in_merge_2hz_hybrid_046, cut_in_merge_2hz_hybrid_047, cut_in_merge_2hz_hybrid_048, cut_in_merge_2hz_hybrid_049)
  - S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_009, cut_in_merge_2hz_hybrid_035)
  - S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_023)
  - S22: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_034)
  - S23: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_020)
  - S24: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_002, cut_in_merge_2hz_hybrid_014)
  - S25: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_015, cut_in_merge_2hz_hybrid_022, cut_in_merge_2hz_hybrid_028)
  - S26: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_019)
  - S27: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_021)
  - S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_026)
  - S11: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_044)
  - S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_001)
  - S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_025)
  - S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_032)
  - S15: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_033)
  - S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_043)
  - S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_003, cut_in_merge_2hz_hybrid_016)
  - S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_017)
- Scene 19f339ba was tried at only one setting and one run, so it is essentially unexplored.
  - S28: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_006)

## Open

- Whether S3 and S7 involve any policy failure at all: their failures come from replayed cars behind the ego running through it before handoff. Rerunning them with the follower removed, or retiming only the lane-changing car, would show whether anything is left once those rear overlaps are gone.
- Whether the policy is at fault at S9: the sideswipe by overtaking actor 33 is marked unclear. Repeats with that actor's timing shifted slightly, or with reactive traffic, would show whether the ego could have avoided it.
- How reliable S1 is: only a few repeats support it, so more runs would narrow its range. Comparing it with the matching setting in the 10 Hz cut_in_merge study would show whether 2 Hz planning reduces the left drift in this scene.
- Whether a genuine policy failure exists near the closest non-failing settings: S4 (096988dd, -0.5 s, 1.5x), S25 (12855a41, 1.5x) and S18 (0e899dd3, 0.75x) came closest without failing. Probing next to them with larger time shifts, up to ±2 s, was never tried.
- Scene 19f339ba (S28) needs a proper search, and the full ±2 s time-shift range went unexplored at every scene.

## Why the runs failed (triage from the video and log)

actor_hit_ego 11, turned_into_actor 3

- cut_in_merge_2hz_hybrid_004: turned_into_actor, policy at fault: yes. On a multi-lane freeway, with the command STRAIGHT and then RIGHT, the policy's plan (orange) veered left toward actor 15, while the recorded human path (green) went straight and then right. The ego drifted into the lane on its left and its front hit actor 56, which was driving alongside there, at 7.2 s.
- cut_in_merge_2hz_hybrid_007: actor_hit_ego, policy at fault: unclear. The ego was going straight in its highway lane at a steady ~8 m/s. Actor 33 came up from behind in the lane to the left, passed the ego and cut in across the lane line just ahead of it, and the ego's front clipped 33's rear-right corner at 6.6s. The camera smear at impact is 33 right beside the ego, not a cause.
- cut_in_merge_2hz_hybrid_010: turned_into_actor, policy at fault: yes. On a multi-lane highway, after the policy took over, the ego sped up from 4.4 to 6.5 m/s and drifted left out of its lane, following a planned path toward actor 15's lane, while the recorded route went straight and then right. Its front hit actor 56, which was driving alongside in the lane to its left.
- cut_in_merge_2hz_hybrid_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy planned and carried out a left lane change while speeding up from 4.4 to 6.5 m/s. It cut into the adjacent left lane right where vehicle 56 was alongside, just ahead and to the left. The ego's front hit 56 at 7.2 s. The camera smear at impact came from being that close to 56 and did not cause the mistake.
- cut_in_merge_2hz_hybrid_012: actor_hit_ego, policy at fault: unclear. The ego held its lane at about 8 m/s, heading slightly right with the route command. Actor 33 came up from behind on the left and passed close alongside, then cut toward the ego's lane and clipped its front-left corner at 6.6 s. The recorded human driver had moved left into that lane instead, so the replayed actor wasn't reacting to where the ego actually was.
- cut_in_merge_2hz_hybrid_013: actor_hit_ego, policy at fault: unclear. The ego was cruising straight on a multi-lane highway at about 8 m/s with a large gap ahead (over 25 m). Actor 33, a replayed car in the lane to the left and behind it, came up and overtook it on the left. At 6.6 s it was alongside and overlapping the ego's front-left corner. The ego was only 0.9 m off the recorded path, drifting slightly left and straddling the lane line, which the human driver also crossed. The contact is a sideswipe from a replayed car overtaking it, not a failure to brake for a car ahead, and the run is also marked rear_ended.
- cut_in_merge_2hz_hybrid_029: actor_hit_ego, policy at fault: no. Actor 9 came up from behind in the ego's lane and hit its rear at about 3.7s, while the ego was still replaying the recorded drive. By 4.7s, when the policy took over, actor 9 had driven up onto the ego's box and was registered as a front collision. The ego was exactly on the recorded path (0.0 m off) and had no time to react, so this looks like a log-replay actor overlapping the ego, not a mistake by the policy.
- cut_in_merge_2hz_hybrid_036: actor_hit_ego, policy at fault: no. At 3.7s, actor 16 was just behind the ego in the same lane. By 4.7s it had driven forward into the ego's box, so the overlap was scored as a front collision. This happened at the handoff moment, while the ego was still exactly on the recorded human path (0.0 m off) and slowing slightly to 13.7 m/s, so the policy had no chance to react.
- cut_in_merge_2hz_hybrid_037: actor_hit_ego, policy at fault: no. The ego was replaying the recorded drive, going straight at about 14 m/s with nothing ahead. Actor 16, a faster vehicle coming up from directly behind in the same lane, drove into and through the ego's box; at 4.7 s it overlaps the ego's front half. That registered as a front collision at the exact moment of handoff (4.7 s), before the policy had any chance to act, and the camera smear in that frame comes from the actor sitting inside the ego.
- cut_in_merge_2hz_hybrid_038: actor_hit_ego, policy at fault: no. At 3.7s, actor 16 was directly behind the ego in the same lane. By 4.7s it had moved up and overlapped the ego's front, which was scored as a front collision. The ego was still exactly on the recorded human path (0.0 m off) at about 14 m/s, and the policy only took over at 4.7s, so this is a replayed actor driving through the ego, not a policy error.
- cut_in_merge_2hz_hybrid_039: actor_hit_ego, policy at fault: no. The ego was still replaying the recorded trajectory (0.0 m off it, about 14 m/s, going straight) when actor 16 came up from directly behind in the same lane and drove through the ego's box. By 4.7 s it overlapped the ego's front half, so the collision was counted as a front collision. This happened at the handoff moment itself (4.7 s), so the policy never had control and could not have avoided it. The camera smear in the last frame is from the overlap at impact.
- cut_in_merge_2hz_hybrid_040: actor_hit_ego, policy at fault: no. The ego was on the replayed human trajectory, 0.0 m off, at about 5 m/s on a straight highway lane with no car close ahead. Actor 9 came up from behind, hit the ego's rear by 3.7 s, and by 4.7 s its box covered the ego's, which the metrics also counted as a front collision. That 4.7 s mark is the instant the policy took over, so it had no chance to act.
- cut_in_merge_2hz_hybrid_041: actor_hit_ego, policy at fault: no. Actor 9 came up from behind in the ego's lane, rear-ended the ego by 3.7 s and kept going until its box sat on top of the ego. That overlap is what registered as a front collision at 4.7 s, the moment the policy took over. Before that the ego was replaying the recorded drive (0 m off the recording) at a steady 5.6 m/s, with no vehicle ahead closer than about 40 m.
- cut_in_merge_2hz_hybrid_042: actor_hit_ego, policy at fault: no. The ego was still replaying the recorded drive, straight in its lane at about 5 m/s (0.0 m off the recording). Actor 9 came up from behind, hit the ego's rear at 3.7 s, and kept driving into it until at 4.7 s it overlapped the whole ego box, which the metrics then count as a front collision at the same moment the policy took over.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_004, cut_in_merge_2hz_hybrid_010, cut_in_merge_2hz_hybrid_011)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_008)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_036, cut_in_merge_2hz_hybrid_037, cut_in_merge_2hz_hybrid_038, cut_in_merge_2hz_hybrid_039)
- S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_030)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_005, cut_in_merge_2hz_hybrid_018)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_027)
- S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_029, cut_in_merge_2hz_hybrid_040, cut_in_merge_2hz_hybrid_041, cut_in_merge_2hz_hybrid_042)
- S8: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_031)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_007, cut_in_merge_2hz_hybrid_012, cut_in_merge_2hz_hybrid_013)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_026)
- S11: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_044)
- S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_001)
- S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_025)
- S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_032)
- S15: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_033)
- S16: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_054)
- S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_024)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_050, cut_in_merge_2hz_hybrid_051, cut_in_merge_2hz_hybrid_052, cut_in_merge_2hz_hybrid_053)
- S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_hybrid_045, cut_in_merge_2hz_hybrid_046, cut_in_merge_2hz_hybrid_047, cut_in_merge_2hz_hybrid_048, cut_in_merge_2hz_hybrid_049)
- S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_009, cut_in_merge_2hz_hybrid_035)
- S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_023)
- S22: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_034)
- S23: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_020)
- S24: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_002, cut_in_merge_2hz_hybrid_014)
- S25: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_015, cut_in_merge_2hz_hybrid_022, cut_in_merge_2hz_hybrid_028)
- S26: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_019)
- S27: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_021)
- S28: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_006)
- S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_043)
- S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_003, cut_in_merge_2hz_hybrid_016)
- S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_017)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 25 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
