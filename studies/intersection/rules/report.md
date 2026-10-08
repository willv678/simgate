# At intersections with crossing traffic, which arrival times and speeds of the recorded crossing car make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene, confirmed by repeats.

Study `rules`: 49 kept runs on 6 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 7 rounds.

## Answer

No arrival timing or speed of the crossing car that the study tried made the VaVAM policy collide or leave the road. Every kept run at every setting passed, so no challenging setting was confirmed on any scene and the goal was not met. The search was narrow, though. Most of the budget went to repeating one setting (on time, 1.25x speed) on four scenes, and most other settings ran only once. Those single passes are a hint, not evidence that the policy is safe there. Most of the brief's range was never tried: shifts later than +0.5 s, speeds below 1.0x, and speeds above 1.5x. With no failures, the ranking falls back to near misses. By criticality, scene 13a9767e came closest, at every setting tried there, with on time at 1.25x the highest.

## Findings

- With the crossing car arriving on time at 1.25x speed, every repeat on scenes 02eadd92, 054b5901, 118a3400 and 1a7b81b8 passed. At this setting, a failure rate above 0.5 is ruled out on each of these scenes.
  - S1: 02eadd92 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_004, intersection_rules_010, intersection_rules_017, intersection_rules_024, intersection_rules_031, intersection_rules_038, intersection_rules_045)
  - S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/8 failed, rate 0%-25% (90%) (intersection_rules_001, intersection_rules_007, intersection_rules_012, intersection_rules_018, intersection_rules_026, intersection_rules_033, intersection_rules_040, intersection_rules_047)
  - S10: 118a3400 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_003, intersection_rules_009, intersection_rules_016, intersection_rules_023, intersection_rules_030, intersection_rules_037, intersection_rules_044)
  - S18: 1a7b81b8 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_005, intersection_rules_011, intersection_rules_019, intersection_rules_025, intersection_rules_032, intersection_rules_039, intersection_rules_046)
- Scene 13a9767e gave the closest calls (the highest criticality in the study) at every timing and speed tried, from -0.5 s to +0.5 s and from 1.0x to 1.5x. None of them led to a collision. The repeated on-time settings at 1.0x and 1.25x also passed every run.
  - S11: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_035)
  - S12: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_014)
  - S13: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (intersection_rules_028, intersection_rules_029, intersection_rules_036)
  - S14: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (intersection_rules_002, intersection_rules_008, intersection_rules_015, intersection_rules_022, intersection_rules_043)
  - S15: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_rules_049)
  - S16: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_042)
  - S17: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_021)
- On scene 0d76134f, the crossing car arriving up to 2 s early at 1.0x or 1.25x produced no failure and zero criticality. The ego barely moves in this scene, so these retimings did not create a conflict. Each setting ran only once.
  - S3: 0d76134f at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_041)
  - S4: 0d76134f at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_034)
  - S5: 0d76134f at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_048)
  - S6: 0d76134f at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_027)
  - S7: 0d76134f at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_020)
  - S8: 0d76134f at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_013)
  - S9: 0d76134f at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_006)
- On scenes 02eadd92, 054b5901, 118a3400 and 1a7b81b8, only the on-time 1.25x setting was run, so they show nothing about earlier or later arrivals or other speeds.
  - S1: 02eadd92 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_004, intersection_rules_010, intersection_rules_017, intersection_rules_024, intersection_rules_031, intersection_rules_038, intersection_rules_045)
  - S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/8 failed, rate 0%-25% (90%) (intersection_rules_001, intersection_rules_007, intersection_rules_012, intersection_rules_018, intersection_rules_026, intersection_rules_033, intersection_rules_040, intersection_rules_047)
  - S10: 118a3400 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_003, intersection_rules_009, intersection_rules_016, intersection_rules_023, intersection_rules_030, intersection_rules_037, intersection_rules_044)
  - S18: 1a7b81b8 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_005, intersection_rules_011, intersection_rules_019, intersection_rules_025, intersection_rules_032, intersection_rules_039, intersection_rules_046)

## Open

- Most of the brief's range was never searched: shifts later than +0.5 s on any scene, speeds below 1.0x, and speeds of 2x. Running single probes across that grid on 13a9767e, 054b5901, 02eadd92, 118a3400 and 1a7b81b8 (for example -2, -1, +1 and +2 s at 0.5x and 2x) would show whether any timing breaks the policy. Any setting that fails should then get about 5 repeats.
- For scenes 02eadd92, 054b5901, 118a3400 and 1a7b81b8, the earlier near-misses within 2 m came from CATK-traffic baselines. Under replay, the retime may not actually put the crossing car in the ego's path. Checking the closest-approach logs of the S1, S2, S10 and S18 runs would show whether the conflict was reproduced at all.
- Scene 0d76134f produced no interaction at any setting. It can likely be dropped, or the time shift moved toward later arrivals to match how slowly the ego moves there.
- Turning manoeuvres were not covered: all six scenes have the ego going straight. Intersection scenes where the ego turns would need a crossing car identified by hand.
- No near miss was ranked against a threshold, because the stopping rule only counts failures. Closest-approach distances for 13a9767e would be needed to rank its settings as near misses.

## Every setting

- S1: 02eadd92 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_004, intersection_rules_010, intersection_rules_017, intersection_rules_024, intersection_rules_031, intersection_rules_038, intersection_rules_045)
- S2: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/8 failed, rate 0%-25% (90%) (intersection_rules_001, intersection_rules_007, intersection_rules_012, intersection_rules_018, intersection_rules_026, intersection_rules_033, intersection_rules_040, intersection_rules_047)
- S3: 0d76134f at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_041)
- S4: 0d76134f at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_034)
- S5: 0d76134f at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_048)
- S6: 0d76134f at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_027)
- S7: 0d76134f at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_020)
- S8: 0d76134f at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_013)
- S9: 0d76134f at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_006)
- S10: 118a3400 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_003, intersection_rules_009, intersection_rules_016, intersection_rules_023, intersection_rules_030, intersection_rules_037, intersection_rules_044)
- S11: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_035)
- S12: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_014)
- S13: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (intersection_rules_028, intersection_rules_029, intersection_rules_036)
- S14: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/5 failed, rate 0%-35% (90%) (intersection_rules_002, intersection_rules_008, intersection_rules_015, intersection_rules_022, intersection_rules_043)
- S15: 13a9767e at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_rules_049)
- S16: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_rules_042)
- S17: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (intersection_rules_021)
- S18: 1a7b81b8 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/7 failed, rate 0%-28% (90%) (intersection_rules_005, intersection_rules_011, intersection_rules_019, intersection_rules_025, intersection_rules_032, intersection_rules_039, intersection_rules_046)

## Provenance

Plan: `plan.json` (rationale: Scope: the brief asks for intersection scenes with crossing cars. I chose the six intersection-tagged scenes that have a recorded crossing_vehicle key actor and that passed the earlier 0-delay run. A scene that already fails cannot show that the retiming caused the failure. Five of these scenes came within 2 m of another actor (054b5901 at 0.26 m, 13a9767e at 0.12 m, 118a3400, 02eadd92, 1a7b81b8), so they are likely to break under small shifts. 0d76134f is a spare: its ego moved only 7 m in the earlier run. Having six scenes leaves room for one to never break while still reaching 5 distinct scenes.

How it runs: traffic is replay, as the brief asks. The retime class is automobile, but retime_tracks pins each scene to its crossing car only. That way, lead vehicles in scenes also tagged lead_vehicle or merge_cut_in are not moved, which would confound the result. The two knobs cover the brief's full ranges: -2 to +2 s and 0.5x to 2x speed.

Goal and budget: the goal is top_k, k=5, one per scene, high_min 0.5. With 90% ranges, each confirmed case needs roughly 5 or more mostly failing repeats, so 5 cases take about 25–30 runs. The remaining ~20 runs of the ~50 budget go to searching. Seven rounds of 7 (49 runs) let the proposer search first and then confirm, and the study stops early if 5 are confirmed.

Limits:
- The goal cannot rank near misses. The proposer is told to use closest approach as the tiebreak, but the stopping rule only counts failures.
- 'Crossing traffic' comes from automatically derived key_actors, not checked by hand. All six scenes record the ego going straight (turn 'none'). The intersection scenes where the ego turns (e.g. 16db28cb left; 1be86721 and 1be9be8f right) have no identified crossing car, so turning cases are not covered.
- The 0-delay baselines were run with CATK traffic, not replay, so the baseline passes are only a guide.
- Under replay the crossing car does not react to the ego. A collision may therefore partly reflect a scripted actor that would have yielded in reality.). Report written by claude-opus-5-5 from `results` in 26 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
