# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r3`: 57 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 10 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Repeats confirmed two of the five settings the brief asked for, and only one of those is clearly the policy's failure. On 096988dd (S2), with the car 2 s earlier at 2x speed and the ego at 1.4x, the policy steered left out of its lane and hit the car beside it in every kept run. That range only just clears 0.5. On 1c45ce3a (S30), with the car 1.5 s later at 1.0x and the ego at 0.8x, every run also failed. In most of those runs, though, a replayed car (actor 24) merged into the ego from the right after the slower ego had fallen about 20 m behind its recorded position. That points to a side effect of replaying traffic that doesn't react to the ego, more than a policy fault. The best unconfirmed candidate is 187e6244 (S20: car 2 s later at 1.0x, ego 1.2x). All of its failures were the policy drifting left into a car coming up alongside, but its range still runs below 0.5. Seven of the ten scenes had no failures at any setting tried, and most settings ran only once, so their ranges stay wide.

## Findings

- On 096988dd, with the car 2 s earlier at 2x speed and the ego at 1.4x, every kept run failed, and each failure was the policy's fault. The ego steered left against a STRAIGHT/RIGHT route command and hit actor 41 in the left lane. This setting is confirmed, though its lower bound is only just above 0.5.
  - S2: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_040_a2, car_conflicts_3knobs_2hz_optuna_confirm_r3_041, car_conflicts_3knobs_2hz_optuna_confirm_r3_051)
- On 1c45ce3a, with the car 1.5 s later at 1.0x speed and the ego at 0.8x, every run failed and the setting counts as confirmed. However, only one failure was the policy's fault (the ego drifted right into actor 24). In the others, actor 24 merged left into an ego that was about 20 m behind its recorded position. Those were judged not the policy's fault or unclear, so this case mostly reflects non-reactive replay, not a policy weakness.
  - S30: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_018, car_conflicts_3knobs_2hz_optuna_confirm_r3_021, car_conflicts_3knobs_2hz_optuna_confirm_r3_031, car_conflicts_3knobs_2hz_optuna_confirm_r3_047_a2)
- The other failures on 1c45ce3a were single runs, all at ego 0.8x. Each had the same cause: actor 24 hit the ego from the right, with fault judged unclear or no. On that scene, single runs at ego 0.6x and 1.2x did not fail. These failures add nothing new: they share S30's scene, so they can't count as distinct cases, and they share its replay explanation.
  - S24: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_058)
  - S25: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_048)
  - S28: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_036_a2)
  - S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_039)
  - S31: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_037_a2)
  - S32: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_049)
- On 187e6244, with the car 2 s later at 1.0x speed and the ego at 1.2x, most runs failed. Every failure was the policy's fault: behind slow lead car 48, the ego drifted left against a RIGHT command and hit actor 7 coming up in the left lane. The range still reaches below 0.5, so it is a strong but unconfirmed candidate. Nearby settings on the same scene, including a faster car (1.5x) or a slower ego (0.8x), did not fail in single runs.
  - S20: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_009, car_conflicts_3knobs_2hz_optuna_confirm_r3_011, car_conflicts_3knobs_2hz_optuna_confirm_r3_022, car_conflicts_3knobs_2hz_optuna_confirm_r3_032, car_conflicts_3knobs_2hz_optuna_confirm_r3_042, car_conflicts_3knobs_2hz_optuna_confirm_r3_052)
  - S21: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_015)
  - S19: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_019)
  - S16: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_002)
  - S17: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_017)
  - S18: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_056)
- The failures that are the policy's fault share one pattern. On multi-lane highways, the planned path bends out of the lane, against the route command, into a car travelling alongside in the next lane. They are not failures to brake for the retimed lead car.
  - S2: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_040_a2, car_conflicts_3knobs_2hz_optuna_confirm_r3_041, car_conflicts_3knobs_2hz_optuna_confirm_r3_051)
  - S20: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_009, car_conflicts_3knobs_2hz_optuna_confirm_r3_011, car_conflicts_3knobs_2hz_optuna_confirm_r3_022, car_conflicts_3knobs_2hz_optuna_confirm_r3_032, car_conflicts_3knobs_2hz_optuna_confirm_r3_042, car_conflicts_3knobs_2hz_optuna_confirm_r3_052)
- No failures appeared on 023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41 or 19f339ba. Even the most repeated of these settings (19f339ba at shift 0 s, car 1.25x, ego 0.6x) bounds the failure rate well below 0.5. Most other settings on these scenes ran only once, which rules little out.
  - S22: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_010, car_conflicts_3knobs_2hz_optuna_confirm_r3_012, car_conflicts_3knobs_2hz_optuna_confirm_r3_024, car_conflicts_3knobs_2hz_optuna_confirm_r3_034, car_conflicts_3knobs_2hz_optuna_confirm_r3_044, car_conflicts_3knobs_2hz_optuna_confirm_r3_053)
  - S1: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_027, car_conflicts_3knobs_2hz_optuna_confirm_r3_045, car_conflicts_3knobs_2hz_optuna_confirm_r3_054)
  - S12: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_016, car_conflicts_3knobs_2hz_optuna_confirm_r3_023, car_conflicts_3knobs_2hz_optuna_confirm_r3_043)
  - S13: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_026, car_conflicts_3knobs_2hz_optuna_confirm_r3_033, car_conflicts_3knobs_2hz_optuna_confirm_r3_055)
  - S14: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_020_a2, car_conflicts_3knobs_2hz_optuna_confirm_r3_025, car_conflicts_3knobs_2hz_optuna_confirm_r3_035)
  - S4: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_003)
  - S5: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_001, car_conflicts_3knobs_2hz_optuna_confirm_r3_013)
  - S6: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_038)
  - S7: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_006_a2)
  - S8: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_008)
  - S9: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_007, car_conflicts_3knobs_2hz_optuna_confirm_r3_014)
  - S10: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_050)
  - S11: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_004)
  - S15: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_059)
  - S23: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_005_a2)
- The near misses that rank next are the highest-criticality settings that didn't fail. These are 187e6244 at car +2 s, 1.0x, ego 0.8x and at car −2 s, 0.5x, ego 1.4x, and 023b7fcc at car +1.5 s, 1.0x, ego 1.4x.
  - S19: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_019)
  - S16: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_002)
  - S1: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_027, car_conflicts_3knobs_2hz_optuna_confirm_r3_045, car_conflicts_3knobs_2hz_optuna_confirm_r3_054)

## Open

- Whether S20 on 187e6244 is above 0.5: a few more repeats at car +2 s, 1.0x, ego 1.2x would settle it. If they keep failing at the same rate, the range should clear 0.5 and this becomes the third distinct confirmed case.
- Whether S30 on 1c45ce3a counts as a policy failure: most of its failures come from replayed actor 24 merging into an ego that was put behind its recorded position. Rerunning with reactive traffic, or scoring only at-fault collisions, would show whether anything is left.
- S2 on 096988dd rests on three runs and only just clears 0.5. Two or three more repeats would make it firm.
- Three more distinct scenes are needed. Seven scenes had no failures, mostly from single runs. More search on the near-miss settings (187e6244 at S19 and S16, 023b7fcc near S1) and their neighbours, and on 096988dd near S2, would show whether further cases exist.
- Three runs on 1c45ce3a at ego 1.4x halted and were not kept, so that corner of the space is untested there.
- Whether the seed-to-seed variation at one setting is the only source of failures: repeats at S20 both failed and passed, so the policy's lane-drift behaviour looks stochastic. Its rate is still uncertain.

## Why the runs failed (triage from the video and log)

turned_into_actor 8, actor_hit_ego 6

- car_conflicts_3knobs_2hz_optuna_confirm_r3_011: turned_into_actor, policy at fault: yes. On a straight multi-lane highway at about 5–6 m/s, the ego's plan bent left away from the recorded path and it drifted into the lane on its left, ending about 2.1 m off the human's trajectory. Vehicle 7 was coming up in that lane from behind-left, and by 12.2 s the ego's front corner had cut into it alongside, which counts as an at-fault front collision.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_018: actor_hit_ego, policy at fault: no. The ego was going straight in its highway lane at about 8.5 m/s and stayed within 0.6 m of the recorded path. A car coming up from behind in the right lane (actor 24) moved alongside and angled into the ego's front-right corner at 9.2 s. The ego was about 20 m behind where the real car was at that moment, so the replayed car likely merged into space that was empty in the original drive; the camera smear at impact is just the close-range actor.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_021: actor_hit_ego, policy at fault: no. The ego was going straight and staying in its lane at about 8.5 m/s, but it was about 19 m behind where the recorded human car was. Actor 24 came up from behind in the lane to the right, passed alongside and drifted left over the lane line, clipping the ego's front-right corner at 9.2s; the replayed actor never reacted to the ego.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_031: turned_into_actor, policy at fault: yes. On a straight freeway with the STRAIGHT command, the ego slowed gradually from 8.7 to 7.8 m/s while its planned path bent right toward the right lane line. Actor 24 was overtaking in the adjacent right lane, and the ego's front-right corner clipped it as the ego drifted about 0.5 m right of the recorded path, which counted as an at-fault front collision.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_032: turned_into_actor, policy at fault: yes. The ego was told to go RIGHT and the recorded route continued straight or bore right. Instead, the policy's planned path drifted left: it slowed behind lead car 48 and moved over the left lane line, ending up 1.8 m off the recorded path. Actor 7 was coming up in the left lane, and the ego's left side hit it at 8.2 s (lateral collision).
- car_conflicts_3knobs_2hz_optuna_confirm_r3_036_a2: actor_hit_ego, policy at fault: no. The ego was driving straight in its lane on a highway at about 8 m/s, slowing a little, and stayed within 0.6 m of the recorded path. Actor 24 came up from behind on the right and moved left into the ego's lane, hitting the ego's right-front side (rear contact was also flagged). The ego was about 20 m behind where the human driver was at that moment, so the replayed actor merged into space the ego now occupied; the ego made no lateral move into the actor.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_040_a2: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy steered left toward the adjacent lane, even though the route command was STRAIGHT and then RIGHT and the recorded path stayed in lane. Its front corner hit vehicle 41, which was travelling alongside in that left lane.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_041: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 7.9 to 5.0 m/s and drifted left out of its lane, away from the recorded path and opposite to the RIGHT route command. It moved into the adjacent left lane and its front clipped actor 41, which was travelling alongside there. The car is clearly visible at the left edge of the camera view at impact.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_042: turned_into_actor, policy at fault: yes. Behind slow lead car 48, the ego drifted left out of its lane at about 3–4 m/s, even though the route command was RIGHT and the recorded path stayed in the lane. It moved into the lane of actor 7, which was coming up from behind on the left, and the two collided side-on at 8.2 s.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_048: actor_hit_ego, policy at fault: unclear. The ego was holding its lane at about 8 m/s on a straight multi-lane road. Actor 24 came up from behind in the lane to the right, drew level with the ego, then moved left across the lane line into the ego's front-right corner at 9.2 s. The ego followed the recorded path closely (0.6 m) but was about 20 m behind where the human driver was at that point, so the logged merge of actor 24 landed on the ego instead of behind it.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_047_a2: actor_hit_ego, policy at fault: unclear. The ego was cruising straight in its lane at about 8.5 m/s, staying within 0.6 m of the recorded path, while lead car 14 pulled away ahead. Actor 24 came up from behind on the right and drifted over the lane line into the ego's right-front side, a likely cut-in. The ego was about 19 m behind where the recorded car was at that time, so the replayed actor merged into space the original car had already left.
- car_conflicts_3knobs_2hz_optuna_confirm_r3_051: turned_into_actor, policy at fault: yes. On a wet multi-lane freeway with the command STRAIGHT (RIGHT in the last frame), the policy's planned path curved left and the ego drifted from its lane toward the left lane, while the recorded human path stayed straight. Its left side hit actor 41, which was traveling alongside in that left lane (a lateral collision at 7.2s).
- car_conflicts_3knobs_2hz_optuna_confirm_r3_052: turned_into_actor, policy at fault: yes. On a multi-lane freeway, the ego slowed behind lead car 48. Its planned path then bent left, away from the recorded route and against the RIGHT command, and the ego moved onto the lane line on its left. At 8.2s its left side hit actor 7, which was coming up alongside in the left lane (lateral collision, ego 1.7 m off the recorded path).
- car_conflicts_3knobs_2hz_optuna_confirm_r3_058: actor_hit_ego, policy at fault: unclear. The ego was going straight on a highway at about 8 m/s, slower than the recorded drive, and fell nearly 20 m behind where the human car was. Actor 24 came up from behind in the lane to the right, passed the ego and moved left into the ego's lane while still beside it. The actor's rear corner clipped the ego's front-right, which was counted as an at-fault front collision even though the ego hardly moved sideways.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_027, car_conflicts_3knobs_2hz_optuna_confirm_r3_045, car_conflicts_3knobs_2hz_optuna_confirm_r3_054)
- S2: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_040_a2, car_conflicts_3knobs_2hz_optuna_confirm_r3_041, car_conflicts_3knobs_2hz_optuna_confirm_r3_051)
- S3: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_030)
- S4: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_003)
- S5: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_001, car_conflicts_3knobs_2hz_optuna_confirm_r3_013)
- S6: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_038)
- S7: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_006_a2)
- S8: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_008)
- S9: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_007, car_conflicts_3knobs_2hz_optuna_confirm_r3_014)
- S10: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_050)
- S11: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_004)
- S12: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_016, car_conflicts_3knobs_2hz_optuna_confirm_r3_023, car_conflicts_3knobs_2hz_optuna_confirm_r3_043)
- S13: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_026, car_conflicts_3knobs_2hz_optuna_confirm_r3_033, car_conflicts_3knobs_2hz_optuna_confirm_r3_055)
- S14: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_020_a2, car_conflicts_3knobs_2hz_optuna_confirm_r3_025, car_conflicts_3knobs_2hz_optuna_confirm_r3_035)
- S15: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_059)
- S16: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_002)
- S17: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_017)
- S18: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_056)
- S19: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_019)
- S20: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_009, car_conflicts_3knobs_2hz_optuna_confirm_r3_011, car_conflicts_3knobs_2hz_optuna_confirm_r3_022, car_conflicts_3knobs_2hz_optuna_confirm_r3_032, car_conflicts_3knobs_2hz_optuna_confirm_r3_042, car_conflicts_3knobs_2hz_optuna_confirm_r3_052)
- S21: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_015)
- S22: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_010, car_conflicts_3knobs_2hz_optuna_confirm_r3_012, car_conflicts_3knobs_2hz_optuna_confirm_r3_024, car_conflicts_3knobs_2hz_optuna_confirm_r3_034, car_conflicts_3knobs_2hz_optuna_confirm_r3_044, car_conflicts_3knobs_2hz_optuna_confirm_r3_053)
- S23: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_005_a2)
- S24: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_058)
- S25: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_048)
- S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_039)
- S27: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_029)
- S28: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_036_a2)
- S29: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_028)
- S30: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_018, car_conflicts_3knobs_2hz_optuna_confirm_r3_021, car_conflicts_3knobs_2hz_optuna_confirm_r3_031, car_conflicts_3knobs_2hz_optuna_confirm_r3_047_a2)
- S31: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_037_a2)
- S32: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r3_049)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r3_005: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_006: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_020: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_036: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_037: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_040: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_046: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r3_047: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r3_057: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r3_060: not kept: HALT

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 32 s; every count above is computed from the queue, not written by the model.

0 of 67 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
