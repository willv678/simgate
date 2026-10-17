# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_optuna`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only 2 of the 5 cases were confirmed, each on its own scene. On 023b7fcc, cars running 1 s late at 1.5x speed (S1) made every run fail. On 096988dd, cars running 1 s early at 0.75x speed (S5) also made every run fail. Almost every failure has the same cause: the policy drifts left out of its lane into a car in the next lane, often while driving well below traffic speed, and even when the route command says RIGHT or STRAIGHT. So the retiming mostly decides whether a car is alongside when the drift happens, rather than creating a hard cut-in. The best third candidate is 19f339ba at -0.5 s and 1.5x (S18). It failed in more than half its runs, but its range still reaches below one half, and several of its side hits were cars coming from behind where the policy's fault is unclear. No failure counts are flagged as possible simulator artifacts.

## Findings

- Confirmed case 1: on 023b7fcc, with cars 1 s late at 1.5x speed, every run failed. In three of them the policy steered left out of its lane and hit actor 56 in the left lane. In the fourth, actor 56 cut in sharply in front of the ego, which never braked; whose fault that was is unclear.
  - S1: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_002, cut_in_merge_2hz_hybrid_optuna_010, cut_in_merge_2hz_hybrid_optuna_011, cut_in_merge_2hz_hybrid_optuna_012)
- Confirmed case 2: on 096988dd, with cars 1 s early at 0.75x speed, every run failed. Each time the ego slowed and drifted left against a RIGHT command, and its side hit actor 41 in the left lane. Other settings on the same scene did not fail, and the one at -1.5 s and 1.5x got repeats, so the failure depends on the timing.
  - S5: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_034, cut_in_merge_2hz_hybrid_optuna_040, cut_in_merge_2hz_hybrid_optuna_041, cut_in_merge_2hz_hybrid_optuna_042)
  - S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_003, cut_in_merge_2hz_hybrid_optuna_016, cut_in_merge_2hz_hybrid_optuna_021)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_022)
- On 19f339ba at -0.5 s and 1.5x, the policy failed in more than half of many repeats, but it is not confirmed above one half. The failures are side hits after the ego crawled at about 4 m/s and drifted about 2 m left onto the lane line. Cars coming up from behind in the left lane then hit it. Some of these hits are marked as unclear fault, not the policy's.
  - S18: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 7/12 failed, rate 36%-78% (90%) (cut_in_merge_2hz_hybrid_optuna_026, cut_in_merge_2hz_hybrid_optuna_028, cut_in_merge_2hz_hybrid_optuna_029, cut_in_merge_2hz_hybrid_optuna_030, cut_in_merge_2hz_hybrid_optuna_043, cut_in_merge_2hz_hybrid_optuna_044, cut_in_merge_2hz_hybrid_optuna_045, cut_in_merge_2hz_hybrid_optuna_046, cut_in_merge_2hz_hybrid_optuna_047, cut_in_merge_2hz_hybrid_optuna_048, cut_in_merge_2hz_hybrid_optuna_049, cut_in_merge_2hz_hybrid_optuna_050)
- On 1c45ce3a, the only failure (at +1 s and 1.25x) was a replayed car coming up from the right rear while the ego stayed on its recorded path. Fault is unclear, and the other runs at that setting passed.
  - S19: 1c45ce3a at actor_time_shift_s 1, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (cut_in_merge_2hz_hybrid_optuna_036, cut_in_merge_2hz_hybrid_optuna_037, cut_in_merge_2hz_hybrid_optuna_038, cut_in_merge_2hz_hybrid_optuna_039)
  - S20: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_024)
  - S21: 1c45ce3a at actor_time_shift_s 2, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_006)
- Settings that came close but never failed when repeated look safe below one half: 0e899dd3 at +1 s/1.5x and +0.5 s/2x, 12855a41 at +1 s/2x, and 09a95ffa at -2 s/1.5x.
  - S14: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_051, cut_in_merge_2hz_hybrid_optuna_052, cut_in_merge_2hz_hybrid_optuna_053, cut_in_merge_2hz_hybrid_optuna_054)
  - S13: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_023, cut_in_merge_2hz_hybrid_optuna_031, cut_in_merge_2hz_hybrid_optuna_032)
  - S15: 12855a41 at actor_time_shift_s 1, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_009, cut_in_merge_2hz_hybrid_optuna_017, cut_in_merge_2hz_hybrid_optuna_019, cut_in_merge_2hz_hybrid_optuna_020)
  - S7: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_008, cut_in_merge_2hz_hybrid_optuna_013, cut_in_merge_2hz_hybrid_optuna_014)
- No setting failed on 054b5901 or 0cf6368d, but each setting there got only one run, which is a hint, not a rate.
  - S2: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_005)
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_025)
  - S9: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_035)
  - S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_027)
  - S11: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_004)
- Most failures in this study come from the policy drifting left into the adjacent lane, not from braking too late for a cut-in car. That holds even at 2 Hz planning, where the left drift is said to be halved.
  - S1: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_002, cut_in_merge_2hz_hybrid_optuna_010, cut_in_merge_2hz_hybrid_optuna_011, cut_in_merge_2hz_hybrid_optuna_012)
  - S5: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_034, cut_in_merge_2hz_hybrid_optuna_040, cut_in_merge_2hz_hybrid_optuna_041, cut_in_merge_2hz_hybrid_optuna_042)
  - S18: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 7/12 failed, rate 36%-78% (90%) (cut_in_merge_2hz_hybrid_optuna_026, cut_in_merge_2hz_hybrid_optuna_028, cut_in_merge_2hz_hybrid_optuna_029, cut_in_merge_2hz_hybrid_optuna_030, cut_in_merge_2hz_hybrid_optuna_043, cut_in_merge_2hz_hybrid_optuna_044, cut_in_merge_2hz_hybrid_optuna_045, cut_in_merge_2hz_hybrid_optuna_046, cut_in_merge_2hz_hybrid_optuna_047, cut_in_merge_2hz_hybrid_optuna_048, cut_in_merge_2hz_hybrid_optuna_049, cut_in_merge_2hz_hybrid_optuna_050)

## Open

- The study found only 2 of the 5 cases. Finding the other three needs more search on the scenes that never failed (054b5901, 0cf6368d, 09a95ffa, 0e899dd3, 12855a41), most of which had only single runs per setting, plus on knob values that were never tried.
- Whether 19f339ba at -0.5 s/1.5x (S18) fails more than half the time: more repeats would settle it. Its failures also need a clearer fault call, because several are cars coming from behind into an ego that had drifted and slowed down.
- Whether 1c45ce3a has a reliable failure anywhere: the one failure at S19 was not clearly the policy's fault.
- How these results compare with the 10 Hz cut_in_merge study, and whether 2 Hz planning changes which scenes and timings break: that study's results are not in this input.
- Whether the failures depend on the retimed cut-in car or on other cars: on 023b7fcc and 096988dd every car was retimed, so the car that triggers the failure cannot be isolated.

## Why the runs failed (triage from the video and log)

turned_into_actor 12, actor_hit_ego 4

- cut_in_merge_2hz_hybrid_optuna_002: actor_hit_ego, policy at fault: unclear. The ego was going straight and speeding up from 4.5 to 6.7 m/s. Actor 56, a replayed vehicle from the original recording that was in the lane to the left, passed the ego and moved into the ego's lane right in front of it. The gap to the vehicle ahead dropped from 21.8 m to 3.6 m within 0.5 s, and the ego's front left corner clipped 56's rear. The ego kept speeding up and never braked, but the cut-in was very sudden and the ego was only 1.6 m from where the human drove, so it is unclear how much of this is the policy's fault.
- cut_in_merge_2hz_hybrid_optuna_010: turned_into_actor, policy at fault: yes. After handoff on a straight multi-lane highway, the policy steered left out of its lane, about 1.6 m off the recorded path, while speeding up from 4.5 to 6.7 m/s. Its front hit actor 56, which was travelling in the adjacent left lane. A follower also touched the ego's rear, but only after this at-fault front collision.
- cut_in_merge_2hz_hybrid_optuna_011: turned_into_actor, policy at fault: yes. Moving at about 6–7 m/s with plenty of room ahead (21 m gap), the ego drifted left toward the lane next to it and its front-left corner hit actor 56, which was driving alongside in that lane. The policy didn't yield to the car next to it during the lateral move; a rear contact came only after the front collision.
- cut_in_merge_2hz_hybrid_optuna_012: turned_into_actor, policy at fault: yes. Once the policy took over, the ego sped up from 4.5 to 6.8 m/s and steered left out of its lane, away from the recorded path, which stayed straight and later bore right. Its front hit vehicle 56, which was alongside and slightly ahead in the next lane on the left. A car behind also touched the ego's rear, but only after this front collision started.
- cut_in_merge_2hz_hybrid_optuna_026: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed to about 3–4 m/s. By the end it was about 69 m behind where the human car was at that time, and it drifted about 2 m left of the recorded path, partly into the lane to its left. Vehicle 25, coming up from behind in that lane, then struck the ego's left side (a side collision). Nothing was close ahead, so the policy did not need to brake.
- cut_in_merge_2hz_hybrid_optuna_028: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego crawled at about 4 m/s, far slower than the recorded car (by the end it was 69 m behind where the real car was). It also drifted about 2.4 m left of the recorded path until it straddled the lane line on its left, even though the command had switched to RIGHT. Actor 29, coming up from behind in the left lane, then sideswiped the ego's left side (lateral collision at 11.6 s).
- cut_in_merge_2hz_hybrid_optuna_034: turned_into_actor, policy at fault: yes. On a wet multi-lane highway, the ego slowed to about 3.3 m/s and drifted left across the lane line toward the adjacent left lane, even though the route command was RIGHT and the recorded drive went right. Its side hit actor 41, which was coming up alongside in that left lane (lateral collision at 8.2 s).
- cut_in_merge_2hz_hybrid_optuna_036: actor_hit_ego, policy at fault: unclear. The ego stayed in its lane on the recorded path (0.1 m off) but slowed steadily from 10.2 to 8.3 m/s with no lead nearby, so it fell about 22 m behind where the human car was at that time. Actor 24 is a log-replayed car in the right lane, and it came up from the ego's right rear and overlapped the ego's right side and front corner. That contact was scored as a front collision, and a rear contact was also recorded.
- cut_in_merge_2hz_hybrid_optuna_040: turned_into_actor, policy at fault: yes. On a multi-lane freeway, the policy cut speed and steered left toward the lane on its left (the orange plan bends left), even though the recorded path went straight and the command changed to RIGHT. Its left side hit actor 41, which was traveling alongside it in that lane, a lateral collision 1.7 m off the recorded path.
- cut_in_merge_2hz_hybrid_optuna_041: turned_into_actor, policy at fault: yes. After handoff, the ego slowed to about 3.5 m/s and drifted left into the adjacent left lane, even though the recorded path stayed in its lane and the route command was STRAIGHT and then RIGHT. Actor 41 was coming up from behind in that lane, and the ego's left side hit it at 8.2 s.
- cut_in_merge_2hz_hybrid_optuna_042: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a RIGHT command, the ego slowed and drifted left toward the adjacent left lane instead of following the recorded path. Vehicle 41 was coming up in that lane, and the ego's left side hit it (lateral collision at 8.2 s).
- cut_in_merge_2hz_hybrid_optuna_043: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was going only about 4 m/s and drifted left onto the lane line, about 1.8 m left of the recorded path. Actor 29, coming up from behind in the lane to the left, side-swiped the ego's left side, which was sticking into its lane.
- cut_in_merge_2hz_hybrid_optuna_044: actor_hit_ego, policy at fault: unclear. On a multi-lane highway, the ego crept along at about 4 m/s, far below traffic speed, and ended up 68 m behind its recorded position and 2.3 m left of the recorded path, which ran one lane to the right. Actor 19, a replayed vehicle coming up from behind, appeared at the ego's left rear and the two made side contact (collision_lateral), with no frontal contact.
- cut_in_merge_2hz_hybrid_optuna_045: actor_hit_ego, policy at fault: unclear. On a multi-lane highway, the ego crawled at about 3.4 m/s and fell about 70 m behind the recorded human. It also drifted about 2 m left of the recorded path, toward the left lane line. Actor 29 (a replayed car, not tracked ahead at 11.1 s) then appeared overlapping the ego's front-left corner at 11.6 s, likely overtaking from behind or beside into the space the ego's drift and slow speed had put it in.
- cut_in_merge_2hz_hybrid_optuna_047: turned_into_actor, policy at fault: yes. Command was STRAIGHT on a multi-lane highway, but the ego drove slowly (about 4 m/s) and steered left, angling about 2 m off its recorded path toward the next lane. Actor 78, a vehicle coming up from behind and to the right, met the ego's left rear side in a lateral collision at 11.6 s.
- cut_in_merge_2hz_hybrid_optuna_050: turned_into_actor, policy at fault: yes. The ego was going very slowly (about 4 m/s) on a multi-lane highway. Instead of following the recorded path in its lane to the right, it drifted left onto the dashed lane line and ended up about 2.2 m off the recording. Actor 29 was coming up in the left lane, and the ego's left side hit it in a lateral collision at 11.6 s.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_002, cut_in_merge_2hz_hybrid_optuna_010, cut_in_merge_2hz_hybrid_optuna_011, cut_in_merge_2hz_hybrid_optuna_012)
- S2: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_005)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_025)
- S4: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_003, cut_in_merge_2hz_hybrid_optuna_016, cut_in_merge_2hz_hybrid_optuna_021)
- S5: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.75: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_optuna_034, cut_in_merge_2hz_hybrid_optuna_040, cut_in_merge_2hz_hybrid_optuna_041, cut_in_merge_2hz_hybrid_optuna_042)
- S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_022)
- S7: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_008, cut_in_merge_2hz_hybrid_optuna_013, cut_in_merge_2hz_hybrid_optuna_014)
- S8: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_015)
- S9: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_035)
- S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_027)
- S11: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_004)
- S12: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_001)
- S13: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_optuna_023, cut_in_merge_2hz_hybrid_optuna_031, cut_in_merge_2hz_hybrid_optuna_032)
- S14: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_051, cut_in_merge_2hz_hybrid_optuna_052, cut_in_merge_2hz_hybrid_optuna_053, cut_in_merge_2hz_hybrid_optuna_054)
- S15: 12855a41 at actor_time_shift_s 1, actor_speed_scale 2: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_hybrid_optuna_009, cut_in_merge_2hz_hybrid_optuna_017, cut_in_merge_2hz_hybrid_optuna_019, cut_in_merge_2hz_hybrid_optuna_020)
- S16: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_033)
- S17: 19f339ba at actor_time_shift_s -2, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_optuna_007, cut_in_merge_2hz_hybrid_optuna_018)
- S18: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 7/12 failed, rate 36%-78% (90%) (cut_in_merge_2hz_hybrid_optuna_026, cut_in_merge_2hz_hybrid_optuna_028, cut_in_merge_2hz_hybrid_optuna_029, cut_in_merge_2hz_hybrid_optuna_030, cut_in_merge_2hz_hybrid_optuna_043, cut_in_merge_2hz_hybrid_optuna_044, cut_in_merge_2hz_hybrid_optuna_045, cut_in_merge_2hz_hybrid_optuna_046, cut_in_merge_2hz_hybrid_optuna_047, cut_in_merge_2hz_hybrid_optuna_048, cut_in_merge_2hz_hybrid_optuna_049, cut_in_merge_2hz_hybrid_optuna_050)
- S19: 1c45ce3a at actor_time_shift_s 1, actor_speed_scale 1.25: 1/4 failed, rate 6%-64% (90%) (cut_in_merge_2hz_hybrid_optuna_036, cut_in_merge_2hz_hybrid_optuna_037, cut_in_merge_2hz_hybrid_optuna_038, cut_in_merge_2hz_hybrid_optuna_039)
- S20: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_024)
- S21: 1c45ce3a at actor_time_shift_s 2, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_optuna_006)

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

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
