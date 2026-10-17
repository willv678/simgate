# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `optuna_confirm_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: only one challenging setting was confirmed, on scene 023b7fcc. There, recorded cars shifted 1.5 s earlier at 1.25x speed made the policy fail on every repeat (S4). All failures in the study came from that scene and from the -1.5 s shift, at speed scales 0.5x, 1.0x and 1.25x (S2, S3, S4). Only S4 has enough repeats to put its failure rate surely above one half. S2 and S3 rest on one or two runs each, so they are hints, not rates. None of the other eight scenes failed in any run. Three of them were repeated enough to look safe at their most critical setting (S18, S19, S29). Triage put every failure on the policy and flagged no simulator artifacts. In most of them the ego drifted left off its route, even though the route command was RIGHT, and hit or scraped the cars beside or ahead of it (actors 13 and 56).

## Findings

- On scene 023b7fcc, retiming the cars 1.5 s earlier at 1.25x speed is a confirmed challenging case: every repeat failed, and the failure rate is surely above one half.
  - S4: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_002, cut_in_merge_2hz_optuna_confirm_r3_010, cut_in_merge_2hz_optuna_confirm_r3_019, cut_in_merge_2hz_optuna_confirm_r3_025, cut_in_merge_2hz_optuna_confirm_r3_050)
- On 023b7fcc, the -1.5 s shift also made the ego fail at 1.0x and 0.5x speed. With only one or two runs per setting, these are hints that the shift matters more than the speed.
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_052)
  - S3: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_024, cut_in_merge_2hz_optuna_confirm_r3_041)
- On 023b7fcc, single runs at other shifts all passed: -2.0 s, -1.0 s, -0.5 s, 0 s, and +0.5 s to +2.0 s. Several were near misses with high criticality, so the failing window around -1.5 s looks narrow but is not established.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_036)
  - S5: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_032)
  - S6: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_043)
  - S7: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_054)
  - S8: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_015)
  - S9: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_006)
  - S10: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_051)
  - S11: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_009)
  - S12: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_033)
- At 1.0x and 1.25x speed on 023b7fcc, the failures were the policy's own: the ego steered left out of its lane against a RIGHT route command. It either hit actor 56 alongside it or closed on 56 from behind without braking, often after scraping actor 13. No failure was flagged as a possible simulator artifact.
  - S3: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_024, cut_in_merge_2hz_optuna_confirm_r3_041)
  - S4: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_002, cut_in_merge_2hz_optuna_confirm_r3_010, cut_in_merge_2hz_optuna_confirm_r3_019, cut_in_merge_2hz_optuna_confirm_r3_025, cut_in_merge_2hz_optuna_confirm_r3_050)
- The single failure at 0.5x speed was a different mechanism. The ego stayed in its lane, on the human's path, and rear-ended lead car 12 in slow, dense traffic because it barely braked.
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_052)
- Scenes 096988dd, 09a95ffa and 19f339ba never failed, even when their most critical setting was repeated. The ranges place those settings' failure rates below one half.
  - S18: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_optuna_confirm_r3_005, cut_in_merge_2hz_optuna_confirm_r3_011, cut_in_merge_2hz_optuna_confirm_r3_020, cut_in_merge_2hz_optuna_confirm_r3_028, cut_in_merge_2hz_optuna_confirm_r3_037, cut_in_merge_2hz_optuna_confirm_r3_047)
  - S19: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r3_014, cut_in_merge_2hz_optuna_confirm_r3_021, cut_in_merge_2hz_optuna_confirm_r3_029, cut_in_merge_2hz_optuna_confirm_r3_038, cut_in_merge_2hz_optuna_confirm_r3_046)
  - S29: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r3_016, cut_in_merge_2hz_optuna_confirm_r3_022, cut_in_merge_2hz_optuna_confirm_r3_030, cut_in_merge_2hz_optuna_confirm_r3_039, cut_in_merge_2hz_optuna_confirm_r3_048)
- Scenes 12855a41, 0cf6368d, 1c45ce3a, 0e899dd3 and 054b5901 produced no failures. Most of these settings ran only once or twice, so they are not shown to be safe. At 12855a41, +1.5 s at 0.75x was repeated, and its range keeps it below one half.
  - S13: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_018)
  - S14: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_017)
  - S15: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_008)
  - S16: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_001)
  - S20: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_026)
  - S21: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_004, cut_in_merge_2hz_optuna_confirm_r3_013)
  - S22: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_034)
  - S23: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_045, cut_in_merge_2hz_optuna_confirm_r3_049)
  - S24: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_023)
  - S25: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_053)
  - S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_042)
  - S27: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_optuna_confirm_r3_003, cut_in_merge_2hz_optuna_confirm_r3_012, cut_in_merge_2hz_optuna_confirm_r3_031)
  - S28: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_027)
  - S30: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_035, cut_in_merge_2hz_optuna_confirm_r3_040)
  - S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_007)

## Open

- Four of the five requested cases were not found. No scene other than 023b7fcc broke at 2 Hz within the budget. A wider search on the near misses would settle whether any other scene can be broken: 12855a41 at -1.5 s, 1.25x (S25); 0e899dd3 at -2.0 s, 1.0x (S23); 1c45ce3a at -0.5 s, 1.25x (S30).
- Whether the 023b7fcc failures depend on speed, or only on the -1.5 s shift, needs repeats at S2 and S3, plus runs at -1.75 s and -1.25 s.
- Comparing with the 10 Hz study cut_in_merge needs that study's results next to these. Whether 2 Hz planning made the policy harder to break cannot be judged from this study alone. The left drift that caused the failures still appears at 2 Hz.
- On 023b7fcc every car is retimed, so the study cannot say which car's timing causes the failure. Retiming actors 56 and 13 alone at -1.5 s would isolate it.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 4, turned_into_actor 4

- cut_in_merge_2hz_optuna_confirm_r3_002: no_brake_for_lead, policy at fault: yes. The route said RIGHT, but the ego's plan drifted left into the next lane, away from the recorded path. There it closed on actor 56 ahead, going from a 10.6 m gap to contact at 6.3–6.8 m/s with almost no braking, and hit it front-first at 9.2 s. The camera smeared nearby cars throughout, but 56 was clearly ahead and getting closer, and the ego had earlier front contacts with actor 13 plus a rear contact.
- cut_in_merge_2hz_optuna_confirm_r3_010: no_brake_for_lead, policy at fault: yes. The route command was RIGHT, but the ego angled left off its route into the lane behind slower actor 56 (it had already scraped actor 13 on its right around 7.2 s). It then held about 6.3 m/s while the gap closed from 10.7 m to contact, and its front hit 56's rear at 9.2 s.
- cut_in_merge_2hz_optuna_confirm_r3_019: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the policy drifted left off the recorded path toward the next lane. Around 7.2s it scraped actor 13, which was right beside it (front contact, gap 0.4 m), and around 8.2s actor 61 tapped its rear. It kept merging left at a steady ~6.9 m/s without braking and at 9.2s hit the back of actor 56, the slower car in the lane it was moving into, as the gap shrank from 9.7 m to 3.3 m to contact.
- cut_in_merge_2hz_optuna_confirm_r3_024: turned_into_actor, policy at fault: yes. Once the policy took over on the multi-lane highway, its plan (orange) curved left toward the next lane, and the ego drifted out of its lane into actor 56, which was driving alongside it in the left lane. The front contact came at 7.2s. The lead car was about 20 m ahead and the camera view looked fine, so the policy made an unsafe lane change without yielding to the car next to it.
- cut_in_merge_2hz_optuna_confirm_r3_025: no_brake_for_lead, policy at fault: yes. The ego was on a multi-lane road with a RIGHT command and had already scraped actor 13 on its right while edging toward that lane, then got rear-tapped. It then stayed in its current lane behind slower actor 56 and kept going at about 6.5 m/s while the gap shrank from 10.6 m to 3.6 m, hitting 56 at 9.2 s without braking enough.
- cut_in_merge_2hz_optuna_confirm_r3_041: turned_into_actor, policy at fault: yes. The ego was going straight on a multi-lane highway and speeding up from 4.4 to 6.4 m/s. As it did, it drifted left toward the next lane, and its front hit vehicle 56, which was driving alongside just ahead on its left, at 7.2s. The lead vehicle stayed about 20 m ahead the whole time, and the ego's rear contact was not the first contact.
- cut_in_merge_2hz_optuna_confirm_r3_050: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego steered left out of its lane at about 6.5 m/s. It brushed actor 13 beside it, then cut into the lane of actor 56 and ran into its rear, closing from 10 m to contact without slowing. The camera smearing appears only on nearby cars as the ego leaves the recorded path; it is a result of the drift, not the cause.
- cut_in_merge_2hz_optuna_confirm_r3_052: no_brake_for_lead, policy at fault: yes. In slow, dense highway traffic going STRAIGHT, the ego followed lead car 12 in its lane and closed the gap from 9.0 m to 4.4 m. After handoff at 4.7 s it slowed only from 4.2 to 3.4 m/s and ran into the back of car 12 (front collision at 5.7 s) while staying 0.2 m from the human's path.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_036)
- S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_052)
- S3: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_024, cut_in_merge_2hz_optuna_confirm_r3_041)
- S4: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.25: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_2hz_optuna_confirm_r3_002, cut_in_merge_2hz_optuna_confirm_r3_010, cut_in_merge_2hz_optuna_confirm_r3_019, cut_in_merge_2hz_optuna_confirm_r3_025, cut_in_merge_2hz_optuna_confirm_r3_050)
- S5: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_032)
- S6: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_043)
- S7: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_054)
- S8: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_015)
- S9: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_006)
- S10: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_051)
- S11: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_009)
- S12: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_033)
- S13: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_018)
- S14: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_017)
- S15: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_008)
- S16: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_001)
- S17: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_044)
- S18: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (cut_in_merge_2hz_optuna_confirm_r3_005, cut_in_merge_2hz_optuna_confirm_r3_011, cut_in_merge_2hz_optuna_confirm_r3_020, cut_in_merge_2hz_optuna_confirm_r3_028, cut_in_merge_2hz_optuna_confirm_r3_037, cut_in_merge_2hz_optuna_confirm_r3_047)
- S19: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r3_014, cut_in_merge_2hz_optuna_confirm_r3_021, cut_in_merge_2hz_optuna_confirm_r3_029, cut_in_merge_2hz_optuna_confirm_r3_038, cut_in_merge_2hz_optuna_confirm_r3_046)
- S20: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_026)
- S21: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_004, cut_in_merge_2hz_optuna_confirm_r3_013)
- S22: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_034)
- S23: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_045, cut_in_merge_2hz_optuna_confirm_r3_049)
- S24: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_023)
- S25: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_053)
- S26: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_042)
- S27: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_optuna_confirm_r3_003, cut_in_merge_2hz_optuna_confirm_r3_012, cut_in_merge_2hz_optuna_confirm_r3_031)
- S28: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_027)
- S29: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_r3_016, cut_in_merge_2hz_optuna_confirm_r3_022, cut_in_merge_2hz_optuna_confirm_r3_030, cut_in_merge_2hz_optuna_confirm_r3_039, cut_in_merge_2hz_optuna_confirm_r3_048)
- S30: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_r3_035, cut_in_merge_2hz_optuna_confirm_r3_040)
- S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_r3_007)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 19 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
