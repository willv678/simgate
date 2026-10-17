# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_optuna_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed only 2 of the 5 cases it was looking for. One is 023b7fcc with the cars 1.5 s earlier at 1.25x speed (S1). The other is 09a95ffa with the cars 1 s earlier at 1.25x speed (S10). Every repeat failed at both settings. With so few runs, the failure rate is only just shown to be above one half, so neither setting is shown to fail every time. The two cases fail the same way. The route said RIGHT, but the ego drifted left of the recorded path into the next lane and then did not brake for a slower car ahead, ending in a front collision. In one run on 023b7fcc it hit a car beside it instead (it turned into that car). Every S10 failure happened with the ego more than 3.5 m off its recorded path, so the simulator's rendering may explain them. Triage still found the lead car visible and blamed the policy. No run on the other seven scenes failed, so the remaining three cases were not found within the budget.

## Findings

- On 023b7fcc, moving the cars 1.5 s earlier at 1.25x speed made every repeat fail. No failure here is flagged as a possible simulator artifact, so this is the cleaner of the two confirmed cases.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_002, cut_in_merge_2hz_hybrid_optuna_r3_010, cut_in_merge_2hz_hybrid_optuna_r3_011)
- On 09a95ffa, moving the cars 1 s earlier at 1.25x speed made every repeat fail. Every one of these failures happened with the ego more than 3.5 m off its recorded path, where the camera view was smeared. Triage judged the lead car still visible and blamed the policy, but this case leans on rendering that the simulator may get wrong.
  - S10: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r3_009, cut_in_merge_2hz_hybrid_optuna_r3_012, cut_in_merge_2hz_hybrid_optuna_r3_013)
- Both confirmed cases share one way of failing. The ego drifted left against a RIGHT route command and then held its speed into a slower car ahead in the new lane. Rear hits on the ego came either before or after the front collision and are not what caused the failures. Even at 2 Hz planning, the left drift is still what drives the failures.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_002, cut_in_merge_2hz_hybrid_optuna_r3_010, cut_in_merge_2hz_hybrid_optuna_r3_011)
  - S10: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r3_009, cut_in_merge_2hz_hybrid_optuna_r3_012, cut_in_merge_2hz_hybrid_optuna_r3_013)
- Running the cars earlier and faster does not make every scene fail. The confirmed case's setting on 054b5901 and on 0cf6368d (cars 1 s earlier, 1.25x speed) passed, including repeats on 0cf6368d. So the failures depend on the scene, not just on the timing and speed.
  - S2: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_031)
  - S14: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_052, cut_in_merge_2hz_hybrid_optuna_r3_053, cut_in_merge_2hz_hybrid_optuna_r3_054)
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_002, cut_in_merge_2hz_hybrid_optuna_r3_010, cut_in_merge_2hz_hybrid_optuna_r3_011)
  - S10: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r3_009, cut_in_merge_2hz_hybrid_optuna_r3_012, cut_in_merge_2hz_hybrid_optuna_r3_013)
- Several settings passed every repeat, so they are unlikely to fail at least half the time: 096988dd (0.5 s earlier, 1.5x), 12855a41 (0.5 s earlier, 1.25x), 19f339ba (2 s earlier at 0.75x, and 0.5 s later at 1.5x), and 1c45ce3a (on time at 1.5x, and 2 s later at 0.5x).
  - S8: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_005, cut_in_merge_2hz_hybrid_optuna_r3_016, cut_in_merge_2hz_hybrid_optuna_r3_045)
  - S23: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_024, cut_in_merge_2hz_hybrid_optuna_r3_028, cut_in_merge_2hz_hybrid_optuna_r3_040)
  - S25: 19f339ba at actor_time_shift_s -2, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_046, cut_in_merge_2hz_hybrid_optuna_r3_047, cut_in_merge_2hz_hybrid_optuna_r3_048)
  - S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_007, cut_in_merge_2hz_hybrid_optuna_r3_014, cut_in_merge_2hz_hybrid_optuna_r3_044)
  - S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_006, cut_in_merge_2hz_hybrid_optuna_r3_015, cut_in_merge_2hz_hybrid_optuna_r3_036)
  - S34: 1c45ce3a at actor_time_shift_s 2, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_049, cut_in_merge_2hz_hybrid_optuna_r3_050, cut_in_merge_2hz_hybrid_optuna_r3_051)
- The nearest misses without a failure were on 19f339ba, 1c45ce3a, 12855a41 and 096988dd. Those are the best places to keep searching. The study's stopping rule only counted failures, though, so this ranking of near misses was never checked.
  - S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_007, cut_in_merge_2hz_hybrid_optuna_r3_014, cut_in_merge_2hz_hybrid_optuna_r3_044)
  - S25: 19f339ba at actor_time_shift_s -2, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_046, cut_in_merge_2hz_hybrid_optuna_r3_047, cut_in_merge_2hz_hybrid_optuna_r3_048)
  - S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_006, cut_in_merge_2hz_hybrid_optuna_r3_015, cut_in_merge_2hz_hybrid_optuna_r3_036)
  - S23: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_024, cut_in_merge_2hz_hybrid_optuna_r3_028, cut_in_merge_2hz_hybrid_optuna_r3_040)
  - S22: 12855a41 at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_025)
  - S31: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_041)
  - S8: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_005, cut_in_merge_2hz_hybrid_optuna_r3_016, cut_in_merge_2hz_hybrid_optuna_r3_045)

## Open

- Three of the five cases are still missing. Searching more around the near misses would settle whether these scenes break at all at 2 Hz: 19f339ba (0.5 s later, 1.5x, and 2 s earlier, 0.75x), 1c45ce3a (on time and 1 s earlier at 1.25–1.5x), 12855a41 (0.5–1 s earlier at 1.25–2x), and 096988dd (0.5 s earlier, 1.5x). This would include speeds and timings not tried yet, such as later timings at 2x.
- Neither confirmed case is shown to fail every time. More repeats of S1 and S10 would narrow how often they fail.
- S10 may be a simulator artifact, because every failure happened with the ego far off its recorded path. Repeating it, or checking it with a renderer that holds up off-path, would show whether the policy really misses the lead car there.
- Many settings had only one or two runs (S2–S7, S9, S11–S13, S15–S22, S24, S26, S27, S29–S31, S33). A pass there is a hint, not a sign the setting is safe.
- This report does not show the comparison with the 10 Hz study cut_in_merge. To check whether 2 Hz planning makes things safer, rerun the 10 Hz case settings on these scenes at 2 Hz, and S1 and S10 at 10 Hz.
- The study cannot tell an ego merge from another car cutting in. On 023b7fcc and 09a95ffa every car was retimed, so it is not clear which car's timing causes the failure. Retiming the slower lead car alone (car 56 on 023b7fcc, vehicle 87 on 09a95ffa) would show whether it is the cause.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 5, turned_into_actor 1

- cut_in_merge_2hz_hybrid_optuna_r3_002: no_brake_for_lead, policy at fault: yes. After handoff, the ego drifted left of the recorded path into the lane behind the slower car 56. Although the route command was RIGHT, it kept speeding up to about 6.3 m/s while the gap shrank from 10.9 m to 4.3 m, and its front hit car 56 at 9.2 s. Car 56 was smeared in the camera view but still clearly showed as a vehicle ahead.
- cut_in_merge_2hz_hybrid_optuna_r3_009: no_brake_for_lead, policy at fault: yes. The ego had moved about a lane to the left of the recorded path, even though the command was RIGHT. It then kept going at about 7.5 m/s and hit vehicle 87 ahead in its lane: the gap shrank from 11.5 m to 4.6 m and ended in a front collision at 9.6 s, with no slowing at all. The camera view was heavily smeared because the ego was off the recorded path, but the lead car could still be seen. An earlier rear contact happened before 7.6 s and did not cause this front impact.
- cut_in_merge_2hz_hybrid_optuna_r3_010: no_brake_for_lead, policy at fault: yes. The route said RIGHT, but the ego drove straight or slightly left, off the recorded path, into the lane behind actor 56. It then closed the gap from about 10.6 m to contact while barely slowing (6.7 to 6.0 m/s) and hit 56 with its front at 9.2s. Actor 13 also hit the ego's rear after the ego left its path; the camera view of the lead car was heavily smeared but still visible.
- cut_in_merge_2hz_hybrid_optuna_r3_011: turned_into_actor, policy at fault: yes. Although the route command was RIGHT, the ego veered left out of its lane on a busy multi-lane road. With actor 13 only 1–1.7 m ahead and to its right, the ego made front contact with it around 7.2 s, then kept closing on actor 56 in the new lane. Actor 61 hit the ego's rear later; that is secondary because the front collision came first.
- cut_in_merge_2hz_hybrid_optuna_r3_012: no_brake_for_lead, policy at fault: yes. The ego had moved about 3–4 m into the lane left of the recorded path. It held about 7.6 m/s while the slower car ahead in that lane (actor 87) closed from 10.3 m to 3.4 m, and the ego hit its rear with its front at 9.6 s. That car looks smeared in the camera because the ego was off the recorded path, but it was still visible, so the policy should have braked. An earlier rear contact on the ego came before this crash and did not cause it.
- cut_in_merge_2hz_hybrid_optuna_r3_013: no_brake_for_lead, policy at fault: yes. The route command was RIGHT, but the ego drifted about 4 m left of the recorded path into the next lane and drove in it behind slower vehicle 87. It held about 7.5 m/s and never braked while the gap fell from 11 m to 4 m, then hit 87's rear with its front. Something had already struck the ego's rear before 7.6 s, and the camera showed 87 as a smeared blob, but 87 was clearly visible and closing the whole time.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_002, cut_in_merge_2hz_hybrid_optuna_r3_010, cut_in_merge_2hz_hybrid_optuna_r3_011)
- S2: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_031)
- S3: 054b5901 at actor_time_shift_s -1, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_032)
- S4: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_001)
- S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_038)
- S6: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_037)
- S7: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_034)
- S8: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_005, cut_in_merge_2hz_hybrid_optuna_r3_016, cut_in_merge_2hz_hybrid_optuna_r3_045)
- S9: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_021)
- S10: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (cut_in_merge_2hz_hybrid_optuna_r3_009, cut_in_merge_2hz_hybrid_optuna_r3_012, cut_in_merge_2hz_hybrid_optuna_r3_013)
- S11: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_023)
- S12: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_043)
- S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_004)
- S14: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_052, cut_in_merge_2hz_hybrid_optuna_r3_053, cut_in_merge_2hz_hybrid_optuna_r3_054)
- S15: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_035)
- S16: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_030)
- S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_042)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_008, cut_in_merge_2hz_hybrid_optuna_r3_018)
- S19: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_022)
- S20: 12855a41 at actor_time_shift_s -2, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_033)
- S21: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_039)
- S22: 12855a41 at actor_time_shift_s -1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_025)
- S23: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_024, cut_in_merge_2hz_hybrid_optuna_r3_028, cut_in_merge_2hz_hybrid_optuna_r3_040)
- S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_003, cut_in_merge_2hz_hybrid_optuna_r3_017)
- S25: 19f339ba at actor_time_shift_s -2, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_046, cut_in_merge_2hz_hybrid_optuna_r3_047, cut_in_merge_2hz_hybrid_optuna_r3_048)
- S26: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_020)
- S27: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_029)
- S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_007, cut_in_merge_2hz_hybrid_optuna_r3_014, cut_in_merge_2hz_hybrid_optuna_r3_044)
- S29: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_019)
- S30: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_026)
- S31: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_041)
- S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_006, cut_in_merge_2hz_hybrid_optuna_r3_015, cut_in_merge_2hz_hybrid_optuna_r3_036)
- S33: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_027)
- S34: 1c45ce3a at actor_time_shift_s 2, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_r3_049, cut_in_merge_2hz_hybrid_optuna_r3_050, cut_in_merge_2hz_hybrid_optuna_r3_051)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 38 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
