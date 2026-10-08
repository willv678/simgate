# At intersections with crossing traffic, which arrival times and speeds of the recorded crossing car make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene, confirmed by repeats.

Study `hybrid`: 49 kept runs on 6 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The study found only one of the five settings it was asked for. On scene 02eadd92, delaying the crossing actor (track 127, a bus) by 1 s at 1.25x speed made the policy collide in every repeat, and its 90% range sits above 0.5 (S6). The goal was not met. A single run at +1.5 s and 1.25x on the same scene also failed (S7), but one run is only a hint. On the other five scenes, no setting tried caused a failure, and most settings there got only one or two runs. That leaves wide ranges that cannot rule out moderate failure rates. Every 02eadd92 failure is flagged as a possible simulator artifact because the ego ended up far from its recorded path. However, the review of each failure's video and log blames the policy: the route said RIGHT, but the ego steered left across lanes into the bus while it was clearly visible, so these failures don't look like rendering problems.

## Findings

- The one confirmed challenging setting is on scene 02eadd92: crossing actor delayed by 1 s at 1.25x speed. Every repeat collided.
  - S6: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (intersection_hybrid_034, intersection_hybrid_036, intersection_hybrid_037, intersection_hybrid_038, intersection_hybrid_039)
- On 02eadd92 the failures start once the bus is delayed by 1 s or more at 1.25x. Shifts of -0.5 s to +0.5 s at 1.25x or 1.5x passed in every run. The single failing run at +1.5 s suggests the failing window goes past +1 s, but that is not confirmed.
  - S1: 02eadd92 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_020)
  - S2: 02eadd92 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_004, intersection_hybrid_012)
  - S3: 02eadd92 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_019)
  - S4: 02eadd92 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_028, intersection_hybrid_032)
  - S5: 02eadd92 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_033)
  - S6: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (intersection_hybrid_034, intersection_hybrid_036, intersection_hybrid_037, intersection_hybrid_038, intersection_hybrid_039)
  - S7: 02eadd92 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_hybrid_040)
- Every failure has the same cause, and the policy was at fault each time. The command was RIGHT and the recorded path stayed right, but the ego drifted about 7 m left across lanes and hit bus 127 at about 8 m/s while barely braking. These runs are flagged as possible artifacts only because the ego was far off its recorded path. The bus was visible on camera before impact, so rendering does not explain the crashes.
  - S6: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (intersection_hybrid_034, intersection_hybrid_036, intersection_hybrid_037, intersection_hybrid_038, intersection_hybrid_039)
  - S7: 02eadd92 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_hybrid_040)
- On scene 13a9767e, no setting failed across shifts of -1.5 s to +0.5 s and speeds of 1.25x to 2x. It produced the closest calls of any non-failing scene (highest criticality), so it ranks next on near misses.
  - S20: 13a9767e at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_031)
  - S21: 13a9767e at actor_time_shift_s -1, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_022, intersection_hybrid_029)
  - S22: 13a9767e at actor_time_shift_s -1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_030)
  - S23: 13a9767e at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_045)
  - S24: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_015, intersection_hybrid_024)
  - S25: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_023, intersection_hybrid_041)
  - S26: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (intersection_hybrid_042, intersection_hybrid_043, intersection_hybrid_044)
  - S27: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (intersection_hybrid_002, intersection_hybrid_008, intersection_hybrid_009)
  - S28: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_010)
  - S29: 13a9767e at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_046)
  - S30: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_016)
- On scene 054b5901, no setting failed at early arrivals (-1.5 s to 0 s) or at 1.25x to 2x speed. Each setting got one or two runs, so this is not strong evidence that the scene is safe.
  - S8: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_025)
  - S9: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_017)
  - S10: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_026)
  - S11: 054b5901 at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_035)
  - S12: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_014)
  - S13: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_048)
  - S14: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_001, intersection_hybrid_007)
- Scenes 118a3400 and 1a7b81b8 did not fail at -0.5 s or 0 s with 1.25x or 1.5x speed. Only these small shifts were tried.
  - S16: 118a3400 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_027)
  - S17: 118a3400 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_047)
  - S18: 118a3400 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_003, intersection_hybrid_011)
  - S19: 118a3400 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_018)
  - S31: 1a7b81b8 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_021)
  - S32: 1a7b81b8 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_049)
  - S33: 1a7b81b8 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_005, intersection_hybrid_013)
- The spare scene 0d76134f got one run at 0 s and 1.25x. The ego came nowhere near another actor (criticality 0), so the scene told us nothing.
  - S15: 0d76134f at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_006)

## Open

- Four of the five requested settings are still missing. The most promising place to look is late arrivals (+0.5 s to +2 s), which were tried only on 02eadd92. On 13a9767e, 054b5901, 118a3400 and 1a7b81b8, run shifts of +1 s, +1.5 s and +2 s at 1.25x and 1.5x, then repeat any that fail about 5 times.
- Speeds below 1x (0.5x to 1x) and the extreme shifts (-2 s, +2 s) were never tried on any scene.
- Is the ego's leftward drift on 02eadd92 caused by the retimed bus, or does the ego drift in that scene anyway? Compare the ego's path in the passing runs (S2, S4) with the failing ones. Run S7 (+1.5 s, 1.25x) about 4 more times, and try +1 s at 1.0x and 1.5x, to find the edges of the failing window.
- The 02eadd92 failures are scripted replay: the bus does not react to the ego. A rerun with reactive traffic would show whether the collision survives a bus that can yield.
- Turns where the ego must cross oncoming traffic are not covered: in all six scenes the ego's recorded path goes straight.

## Why the runs failed (triage from the video and log)

turned_into_actor 6

- intersection_hybrid_034: turned_into_actor, policy at fault: yes. Despite a RIGHT command, the ego left the recorded path, which stayed in the right lanes, and steered left across lanes toward bus 127. It ran into the bus's right side while overtaking it at about 8 m/s, without braking or steering away. The ego was about 7 m off the recorded path when it hit the bus.
- intersection_hybrid_036: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded path stays in the right lanes. The ego instead drifted left across the lanes, ending up 6.6 m from the recorded path, toward a bus (actor 127) that was stopped or nearly stopped in a lane further left. It closed in at about 8 m/s, braked only lightly (from 8.6 to 6.9 m/s), and hit the bus's right side with its front corner at 8.9 s.
- intersection_hybrid_037: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego moved left out of the recorded path, ending up 6.7 m from it, toward the lane where bus 127 was coming toward it. The ego kept going at about 8.5 m/s and its front clipped the bus's corner as the bus passed on the left.
- intersection_hybrid_038: turned_into_actor, policy at fault: yes. The route said RIGHT and the recorded path went right, but the ego steered left at about 8.5 m/s into the lane where bus 127 was coming toward it, and hit the bus front-on and side-on. The gap closed faster than the ego was driving, so the bus was moving toward the ego, and the ego ended up 6.7 m off the recorded path.
- intersection_hybrid_039: turned_into_actor, policy at fault: yes. The command was RIGHT and the recorded path stayed in the right lanes, but the ego drifted left across several lanes into the lanes of an oncoming bus (actor 127). It hit the bus head-on at about 7.7 m/s, 6.6 m off the human's path. The gap closed about 16 m/s, so the bus was coming toward the ego, and the ego barely braked. The bus was clearly visible in the camera from 6.7 s on.
- intersection_hybrid_040: turned_into_actor, policy at fault: yes. The route said RIGHT and the recorded path stayed to the right, but the ego steered left at about 8.5 m/s and ended up about 7 m off the recording. It drifted into the lane where bus 127 was coming toward it after a turn and hit the bus at 9.0 s, mostly with its front left. The bus was clearly visible on camera at 7 s and 8 s, so the smearing in the image does not explain the mistake.

## Every setting

- S1: 02eadd92 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_020)
- S2: 02eadd92 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_004, intersection_hybrid_012)
- S3: 02eadd92 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_019)
- S4: 02eadd92 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_028, intersection_hybrid_032)
- S5: 02eadd92 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_033)
- S6: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (intersection_hybrid_034, intersection_hybrid_036, intersection_hybrid_037, intersection_hybrid_038, intersection_hybrid_039)
- S7: 02eadd92 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_hybrid_040)
- S8: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_025)
- S9: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_017)
- S10: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_026)
- S11: 054b5901 at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_035)
- S12: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_014)
- S13: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_048)
- S14: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_001, intersection_hybrid_007)
- S15: 0d76134f at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_006)
- S16: 118a3400 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_027)
- S17: 118a3400 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_047)
- S18: 118a3400 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_003, intersection_hybrid_011)
- S19: 118a3400 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_018)
- S20: 13a9767e at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_031)
- S21: 13a9767e at actor_time_shift_s -1, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_022, intersection_hybrid_029)
- S22: 13a9767e at actor_time_shift_s -1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_030)
- S23: 13a9767e at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_045)
- S24: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_015, intersection_hybrid_024)
- S25: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_023, intersection_hybrid_041)
- S26: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (intersection_hybrid_042, intersection_hybrid_043, intersection_hybrid_044)
- S27: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (intersection_hybrid_002, intersection_hybrid_008, intersection_hybrid_009)
- S28: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_010)
- S29: 13a9767e at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_046)
- S30: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_016)
- S31: 1a7b81b8 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_021)
- S32: 1a7b81b8 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_hybrid_049)
- S33: 1a7b81b8 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (intersection_hybrid_005, intersection_hybrid_013)

## Provenance

Plan: `plan.json` (rationale: Scope: the brief asks for intersection scenes with crossing cars. I chose the six intersection-tagged scenes that have a recorded crossing_vehicle key actor and that passed the earlier 0-delay run. A scene that already fails cannot show that the retiming caused the failure. Five of these scenes came within 2 m of another actor (054b5901 at 0.26 m, 13a9767e at 0.12 m, 118a3400, 02eadd92, 1a7b81b8), so they are likely to break under small shifts. 0d76134f is a spare: its ego moved only 7 m in the earlier run. Having six scenes leaves room for one to never break while still reaching 5 distinct scenes.

How it runs: traffic is replay, as the brief asks. The retime class is automobile, but retime_tracks pins each scene to its crossing car only. That way, lead vehicles in scenes also tagged lead_vehicle or merge_cut_in are not moved, which would confound the result. The two knobs cover the brief's full ranges: -2 to +2 s and 0.5x to 2x speed.

Goal and budget: the goal is top_k, k=5, one per scene, high_min 0.5. With 90% ranges, each confirmed case needs roughly 5 or more mostly failing repeats, so 5 cases take about 25–30 runs. The remaining ~20 runs of the ~50 budget go to searching. Seven rounds of 7 (49 runs) let the proposer search first and then confirm, and the study stops early if 5 are confirmed.

Limits:
- The goal cannot rank near misses. The proposer is told to use closest approach as the tiebreak, but the stopping rule only counts failures.
- 'Crossing traffic' comes from automatically derived key_actors, not checked by hand. All six scenes record the ego going straight (turn 'none'). The intersection scenes where the ego turns (e.g. 16db28cb left; 1be86721 and 1be9be8f right) have no identified crossing car, so turning cases are not covered.
- The 0-delay baselines were run with CATK traffic, not replay, so the baseline passes are only a guide.
- Under replay the crossing car does not react to the ego. A collision may therefore partly reflect a scripted actor that would have yielded in reality.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
