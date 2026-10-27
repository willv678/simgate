# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r7`: 56 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 6 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only one challenging case was confirmed: scene 1c45ce3a with the car shifted 2 s earlier, at recorded speed (1.0x), and the ego at 0.8x speed at hand-off. Even that case is mostly not the policy's failure. In every failure there, the policy kept its lane while driving slower than the human and fell well behind the recorded position. Replayed actor 24 then came up from behind on the right and merged into the ego's front-right corner, moving into space the real car had already left. The triage marks the policy as not at fault or unclear in each of these runs. The one failure that is clearly the policy's own is on scene 19f339ba (car 1 s earlier, 1.25x speed, ego 1.4x): the policy braked hard for no reason on an open highway, drifted left and struck a car in the next lane. That setting failed both times it ran, but two runs are a strong hint, not a confirmed rate. The other eight scenes produced no failures at any setting tried, including settings repeated five times. So within this budget, failures stayed as rare as the brief expected.

## Findings

- The only confirmed challenging case is on 1c45ce3a: car 2 s earlier, at recorded speed, ego at 0.8x. Every kept run there was a front collision.
  - S23: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_020, car_conflicts_3knobs_2hz_optuna_confirm_r7_041, car_conflicts_3knobs_2hz_optuna_confirm_r7_052, car_conflicts_3knobs_2hz_optuna_confirm_r7_058)
- On 1c45ce3a, the collisions at ego 0.8x were not caused by the policy steering into the car. The ego kept its lane but lagged behind the recorded human. Replayed actor 24, which is not the retimed car 14, merged into its front-right corner. Triage marks the policy as not at fault or unclear in every one of these runs, so these failures largely come from replayed traffic that does not react to the ego.
  - S23: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_020, car_conflicts_3knobs_2hz_optuna_confirm_r7_041, car_conflicts_3knobs_2hz_optuna_confirm_r7_052, car_conflicts_3knobs_2hz_optuna_confirm_r7_058)
  - S25: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_016, car_conflicts_3knobs_2hz_optuna_confirm_r7_046)
  - S28: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 2/3 failed, rate 25%-92% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_007, car_conflicts_3knobs_2hz_optuna_confirm_r7_011, car_conflicts_3knobs_2hz_optuna_confirm_r7_021)
- On 1c45ce3a, the single runs at ego 1.0x and 1.2x did not fail. Some ego-0.8x settings did not fail either (car 1.5x speed, or car 0.75x speed at -0.5 s). The ego's slow hand-off speed looks necessary for the conflict but not sufficient. Each of these is a single run.
  - S24: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_060)
  - S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_018_a2)
  - S26: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_037)
  - S27: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_026)
  - S23: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_020, car_conflicts_3knobs_2hz_optuna_confirm_r7_041, car_conflicts_3knobs_2hz_optuna_confirm_r7_052, car_conflicts_3knobs_2hz_optuna_confirm_r7_058)
  - S25: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_016, car_conflicts_3knobs_2hz_optuna_confirm_r7_046)
- The one failure that is the policy's own is on 19f339ba: car 1 s earlier, 1.25x speed, ego 1.4x. The policy braked hard with no car close ahead, drifted left and side-swiped a car in the adjacent lane. It failed both runs but is not yet confirmed.
  - S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_050, car_conflicts_3knobs_2hz_optuna_confirm_r7_051)
- Settings with the highest near-miss scores on 096988dd, 12855a41 and 187e6244 were repeated and never failed. Their failure rates are bounded below one half but are not shown to be zero.
  - S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_019, car_conflicts_3knobs_2hz_optuna_confirm_r7_024, car_conflicts_3knobs_2hz_optuna_confirm_r7_034, car_conflicts_3knobs_2hz_optuna_confirm_r7_044, car_conflicts_3knobs_2hz_optuna_confirm_r7_055)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_008, car_conflicts_3knobs_2hz_optuna_confirm_r7_014, car_conflicts_3knobs_2hz_optuna_confirm_r7_025, car_conflicts_3knobs_2hz_optuna_confirm_r7_035, car_conflicts_3knobs_2hz_optuna_confirm_r7_045)
  - S19: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_006, car_conflicts_3knobs_2hz_optuna_confirm_r7_022, car_conflicts_3knobs_2hz_optuna_confirm_r7_032, car_conflicts_3knobs_2hz_optuna_confirm_r7_042_a2, car_conflicts_3knobs_2hz_optuna_confirm_r7_053)
- No kept run failed on 023b7fcc, 096988dd, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41 or 187e6244. Most of these settings ran only once or twice.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_005, car_conflicts_3knobs_2hz_optuna_confirm_r7_013, car_conflicts_3knobs_2hz_optuna_confirm_r7_023)
  - S2: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_017)
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_036)
  - S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_019, car_conflicts_3knobs_2hz_optuna_confirm_r7_024, car_conflicts_3knobs_2hz_optuna_confirm_r7_034, car_conflicts_3knobs_2hz_optuna_confirm_r7_044, car_conflicts_3knobs_2hz_optuna_confirm_r7_055)
  - S5: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_009, car_conflicts_3knobs_2hz_optuna_confirm_r7_015)
  - S6: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_039)
  - S7: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_028)
  - S8: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_003)
  - S9: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_030)
  - S10: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_048)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_049)
  - S12: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_002)
  - S13: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_029, car_conflicts_3knobs_2hz_optuna_confirm_r7_033, car_conflicts_3knobs_2hz_optuna_confirm_r7_043, car_conflicts_3knobs_2hz_optuna_confirm_r7_054)
  - S14: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_059)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_008, car_conflicts_3knobs_2hz_optuna_confirm_r7_014, car_conflicts_3knobs_2hz_optuna_confirm_r7_025, car_conflicts_3knobs_2hz_optuna_confirm_r7_035, car_conflicts_3knobs_2hz_optuna_confirm_r7_045)
  - S16: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_027)
  - S17: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_010)
  - S18: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_056)
  - S19: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_006, car_conflicts_3knobs_2hz_optuna_confirm_r7_022, car_conflicts_3knobs_2hz_optuna_confirm_r7_032, car_conflicts_3knobs_2hz_optuna_confirm_r7_042_a2, car_conflicts_3knobs_2hz_optuna_confirm_r7_053)
  - S20: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_004, car_conflicts_3knobs_2hz_optuna_confirm_r7_012)
  - S21: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_001)

## Open

- Whether 19f339ba (car -1 s, 1.25x speed, ego 1.4x) is a confirmed policy failure. Three or more repeats at S22 would settle it, and nearby settings would show how wide the phantom-braking region is.
- Whether 1c45ce3a at car -1.5 s, 1.25x speed, ego 0.8x (S25) and at car -0.5 s, 1.0x speed, ego 0.8x (S28) reach a confirmed rate. Their failures share the same actor-24 replay mechanism, so confirming them would add the same non-policy case, not new scenes.
- Whether the 1c45ce3a failures should count at all. They come from replayed actor 24 merging into an ego that lags the recording. Re-running S23 with reactive traffic, or with actor 24 also retimed, would show whether the policy fails there.
- Why the car's speed and timing barely matter on 1c45ce3a. The plan retimes track 14, but the striking actor is 24, so the three-knob search may not be reaching the actor that causes the conflict.
- Five runs on 1c45ce3a, including one at the S23 setting, halted and were not kept. They are not evidence, but it is worth checking whether the halts hide failures or simulator problems in this scene.
- No settings on the other eight scenes reached a failure. Finding the remaining four distinct-scene cases needs more search budget, especially on scenes where near misses repeated (096988dd, 12855a41, 187e6244, 0e899dd3).

## Why the runs failed (triage from the video and log)

actor_hit_ego 8, turned_into_actor 2

- car_conflicts_3knobs_2hz_optuna_confirm_r7_007: actor_hit_ego, policy at fault: unclear. On a straight multi-lane road, actor 24 came up from behind in the lane to the right, drew level and moved left over the lane line into the ego at 9.2 s. The ego stayed in its lane (0.6 m off the recorded path) at about 8 m/s and did not steer toward it. The ego was about 20 m behind where the human driver was at that moment, so the replayed actor's lane change, which was timed against the human's position, landed on the ego's front-right corner.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_011: actor_hit_ego, policy at fault: unclear. On a straight highway, the ego went slower than the recorded human (it fell about 21 m behind its recorded position). Actor 24 came up from behind in the lane to the right, passed the ego, and merged left into the ego's lane right at its front-right corner, which registered as a front collision at 9.2 s. The ego kept its lane, and the replayed actor seems to have cut into the space the real car had already left, so the ego's slow pace set up the conflict but it did not steer into the actor.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_016: actor_hit_ego, policy at fault: unclear. The ego drove straight on a clear highway lane with nothing ahead, but slowly (about 8 m/s), and fell about 20 m behind the recorded car (the hollow box pulling ahead on the map). Actor 24, replaying its recorded path, came up from behind on the right and moved into the ego's lane where the real car had already passed, clipping the ego's front-right corner at 9.2 s.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_020: actor_hit_ego, policy at fault: unclear. The ego stays in its lane on a straight highway (0.5 m off the recorded path) while actor 24 comes up from behind on the right, passes, and moves left into the ego's lane right beside it. The actor's rear-left corner meets the ego's front-right corner at 9.2 s. Because the ego had slowed (8.6 to 7.5 m/s) and was about 21 m behind where the human drove, the replayed actor merged into space the ego was still in.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_041: actor_hit_ego, policy at fault: no. The ego was going straight in its lane at about 8 m/s, gently slowing and staying within 0.4 m of the recorded path. Actor 24 came up from behind in the lane to the right, passed the ego and moved left into its lane (from about x=343 to x=322 on the map), so its side met the ego's front-right corner at 9.2 s. The front collision is a contact point with a vehicle that cut in from the side. The ego had no lead vehicle ahead, and the camera smear at 9.2 s comes from the impact itself.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_046: actor_hit_ego, policy at fault: no. The ego was going straight on a highway at a steady 8–9 m/s, keeping its lane, but it fell about 20 m behind where the human drove (the faded box ahead of it on the map). Actor 24, replayed from the log, came up from behind on the right and moved left into the ego's lane. Because the ego was not where the real car had been, actor 24 cut into its front-right corner, which the metrics record as a front collision; the ego was also flagged as rear-ended.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_050: turned_into_actor, policy at fault: yes. On a clear highway with no lead car within about 43 m, the policy braked hard for no visible reason, slowing from 23.7 to 7.1 m/s. At the same time it drifted about 1 m left of its recorded line. Replayed car 1, travelling in the left lane, caught up with the slowing ego and was beside it at 7.6 s, when the ego's left side made lateral contact with it.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_051: turned_into_actor, policy at fault: yes. On an open multi-lane highway, the policy braked hard for no reason (23.7 to 7.4 m/s, with the nearest vehicle ahead 43–49 m away) while drifting left of its route, toward the next lane over. Actor 1, which had been behind in that left lane, came up alongside, and the ego's front corner hit it as the ego moved into its lane. This happened even though the route command at that moment was RIGHT.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_052: actor_hit_ego, policy at fault: no. The ego kept its lane at about 8 m/s, within 0.5 m of the human path. Actor 24 came up from behind on the right, passed it, and moved left into the ego's front-right corner at 9.2 s, which counts as a front collision. The ego was about 20 m behind where the real car was at that time, so the replayed actor merged into space the ego now occupied. The ego was driving reasonably and had little chance to avoid the contact.
- car_conflicts_3knobs_2hz_optuna_confirm_r7_058: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane at about 8 m/s, slowing slightly, with no lead vehicle. Actor 24 came up from behind in the right lane, passed alongside, and moved left into the ego's lane right beside its front-right corner, so the contact counted as a front collision. The ego stayed within 0.6 m of the human's path but was about 21 m behind where the human car was at that time. That lag is probably why the replayed actor merged into space the ego still occupied, which makes the policy's share of blame unclear.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_005, car_conflicts_3knobs_2hz_optuna_confirm_r7_013, car_conflicts_3knobs_2hz_optuna_confirm_r7_023)
- S2: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_017)
- S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_036)
- S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_019, car_conflicts_3knobs_2hz_optuna_confirm_r7_024, car_conflicts_3knobs_2hz_optuna_confirm_r7_034, car_conflicts_3knobs_2hz_optuna_confirm_r7_044, car_conflicts_3knobs_2hz_optuna_confirm_r7_055)
- S5: 09a95ffa at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_009, car_conflicts_3knobs_2hz_optuna_confirm_r7_015)
- S6: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_039)
- S7: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_028)
- S8: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_003)
- S9: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_030)
- S10: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_048)
- S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_049)
- S12: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_002)
- S13: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_029, car_conflicts_3knobs_2hz_optuna_confirm_r7_033, car_conflicts_3knobs_2hz_optuna_confirm_r7_043, car_conflicts_3knobs_2hz_optuna_confirm_r7_054)
- S14: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_059)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_008, car_conflicts_3knobs_2hz_optuna_confirm_r7_014, car_conflicts_3knobs_2hz_optuna_confirm_r7_025, car_conflicts_3knobs_2hz_optuna_confirm_r7_035, car_conflicts_3knobs_2hz_optuna_confirm_r7_045)
- S16: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_027)
- S17: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_010)
- S18: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_056)
- S19: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_006, car_conflicts_3knobs_2hz_optuna_confirm_r7_022, car_conflicts_3knobs_2hz_optuna_confirm_r7_032, car_conflicts_3knobs_2hz_optuna_confirm_r7_042_a2, car_conflicts_3knobs_2hz_optuna_confirm_r7_053)
- S20: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_004, car_conflicts_3knobs_2hz_optuna_confirm_r7_012)
- S21: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_001)
- S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_050, car_conflicts_3knobs_2hz_optuna_confirm_r7_051)
- S23: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_020, car_conflicts_3knobs_2hz_optuna_confirm_r7_041, car_conflicts_3knobs_2hz_optuna_confirm_r7_052, car_conflicts_3knobs_2hz_optuna_confirm_r7_058)
- S24: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_060)
- S25: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_016, car_conflicts_3knobs_2hz_optuna_confirm_r7_046)
- S26: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_037)
- S27: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_026)
- S28: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 2/3 failed, rate 25%-92% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_007, car_conflicts_3knobs_2hz_optuna_confirm_r7_011, car_conflicts_3knobs_2hz_optuna_confirm_r7_021)
- S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_018_a2)
- S30: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r7_047)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r7_018: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r7_031: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r7_038: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r7_040: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r7_042: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r7_057: not kept: HALT

## Provenance

Plan: `plan.json` (rationale: Scene choice: these are the scenes tagged merge_cut_in or lead_vehicle that did not fail in the earlier run at the recorded setting, have a recorded car the study can retime (lead_vehicle or cut_in), and drove far enough for a conflict to develop. Most of them already came close to another actor as recorded: 023b7fcc came within 0.02 m, 096988dd 0.01 m, 19f339ba 0.03 m, 12855a41 0.08 m, and 0dbb91dd and 187e6244 0.23 m. Those are the most promising places to look for rare failures.

Left out:
- Scenes that were nearly stationary (0fa7060f, 15dd433e, 0ac02819, 10d64934) or very slow (01d503d4, 098e2482, 11fce928, 1bfd39ec).
- Scenes with no car the study can retime (for example 04749bb9, 05f35348, 0ce6f2a3, 166fe701).
- Scenes whose only key actor is a crossing vehicle at an intersection (02eadd92, 054b5901).

Note that 01d503d4 appears twice in the scene list.

Retiming and settings:
- Traffic is replay, as the brief asks, with retime_class automobile.
- Each scene retimes only its key car. In 12855a41 that is the cut-in car 31 rather than the lead car 5.
- All three knobs span exactly the ranges in the brief: timing ±2 s, car speed 0.5x to 2x, ego speed 0.6x to 1.4x.
- The controller is linear MPC.

Goal: top_k with k=5, distinct scenes, high_min 0.5. This matches the request for the 5 most challenging cases, each confirmed by repeats.

Limits:
- The budget is tight. With 90% ranges, a setting needs roughly 5 failures out of 5 runs to lie surely above 0.5. Confirming 5 cases therefore takes about 25 runs, which leaves about 35 runs to search a 270-cell grid on 10 scenes. If failures are as rare as the brief expects, the study may end with fewer than 5 confirmed cases. It would then report the strongest candidates and the near misses, which the brief ranks next.
- The 2 Hz planning rate is not a knob in this interface. The plan assumes the runs use VaVAM's 2 Hz rhythm as configured; nothing here sets it or checks it. planner_delay_us, lateral_bias_m and waypoint_noise_std stay at their defaults.
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

0 of 62 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
