# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `random_confirm_r6`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 7 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 2 of the 5 cases it aimed for, so the goal was not met. Only one of the two is clearly the policy's failure. On 187e6244 (S25), the slow lead car arrives early (−1.5 s, 0.5x) while the ego takes over fast (1.2x). Every run there failed the same way: the policy braked too late and hit the lead car's rear. On 1c45ce3a (S33: −0.5 s, 1.0x, ego 0.8x), every run also failed, but each time a replayed car (actor 24, not the retimed car) cut in from the right and clipped the ego. Triage did not fault the policy for this, so S33 is mostly a log-replay effect. Three other settings, on 09a95ffa and 023b7fcc, failed once each with the policy steering left against its route into a neighbouring car. These are hints, not confirmed rates, and one of them (S1) may be a simulator artifact.

## Findings

- Confirmed policy failure on 187e6244: with the lead car 1.5 s early at half speed and the ego at 1.2x speed at hand-off, every run ended in a front collision. The policy braked too late and too gently for a lead it was closing on, and the 90% range lies above 0.5.
  - S25: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_004, car_conflicts_3knobs_2hz_random_confirm_r6_011, car_conflicts_3knobs_2hz_random_confirm_r6_021)
- On 187e6244, nearby settings did not fail in single runs: the same early, slow lead with the ego even faster (1.4x), and settings with a later or faster lead and a slower ego. One run each is too few to rule failure out, but the failure looks tied to the closing speed at hand-off.
  - S24: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_026)
  - S26: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_029_a2)
  - S27: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_006)
  - S28: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_039)
- The setting on 1c45ce3a counts as confirmed, but its failures are not clearly the policy's. In every run, replayed actor 24 came up from behind on the right and cut into the ego's lane, clipping the ego. The ego never steered into it. Triage judged one run not the policy's fault and two unclear: the ego slowed with no lead nearby and fell about 21 m behind its recorded position, so the unreactive replay car ran into it.
  - S33: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_028, car_conflicts_3knobs_2hz_random_confirm_r6_031, car_conflicts_3knobs_2hz_random_confirm_r6_041)
- On 09a95ffa, the single run with the lead car 1.5 s late at recorded speeds failed. The policy bent left against a STRAIGHT/RIGHT route and side-swiped vehicle 33 in the left lane. With one run, this is a candidate, not a rate.
  - S7: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_057)
- 023b7fcc shows a recurring policy fault: drifting left against a RIGHT route into another lane's car (cars 37 and 56, not the retimed car 12). At each of the two settings, only some runs failed, so neither is confirmed. The S1 failure ended about 6 m off the recorded path and is flagged as a possible rendering artifact.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%), 1 possibly the simulator's (car_conflicts_3knobs_2hz_random_confirm_r6_010, car_conflicts_3knobs_2hz_random_confirm_r6_015, car_conflicts_3knobs_2hz_random_confirm_r6_024_a2, car_conflicts_3knobs_2hz_random_confirm_r6_035)
  - S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_048, car_conflicts_3knobs_2hz_random_confirm_r6_051)
- Six scenes showed no failures at any setting tried: 096988dd, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41 and 19f339ba. Settings repeated several times keep upper bounds below 0.5, so these combinations are unlikely to fail often. On 0dbb91dd the retimed car never came close to the ego (criticality zero).
  - S31: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_001, car_conflicts_3knobs_2hz_random_confirm_r6_013, car_conflicts_3knobs_2hz_random_confirm_r6_025_a2, car_conflicts_3knobs_2hz_random_confirm_r6_033, car_conflicts_3knobs_2hz_random_confirm_r6_044, car_conflicts_3knobs_2hz_random_confirm_r6_054)
  - S19: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_009, car_conflicts_3knobs_2hz_random_confirm_r6_014, car_conflicts_3knobs_2hz_random_confirm_r6_034, car_conflicts_3knobs_2hz_random_confirm_r6_045, car_conflicts_3knobs_2hz_random_confirm_r6_053)
  - S17: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_003, car_conflicts_3knobs_2hz_random_confirm_r6_012, car_conflicts_3knobs_2hz_random_confirm_r6_023, car_conflicts_3knobs_2hz_random_confirm_r6_032_a2)
  - S12: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_037, car_conflicts_3knobs_2hz_random_confirm_r6_042, car_conflicts_3knobs_2hz_random_confirm_r6_055)
  - S13: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_046)
  - S14: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_030)
  - S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_060)
  - S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_059)
  - S6: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_002)
  - S9: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_005)
  - S10: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_020)
  - S11: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_027)
  - S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_007)
  - S16: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_040, car_conflicts_3knobs_2hz_random_confirm_r6_052)
  - S18: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_038_a2, car_conflicts_3knobs_2hz_random_confirm_r6_043)
  - S20: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_049)
  - S21: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_058)
  - S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_018)
  - S23: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_036)
  - S29: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_056)
  - S30: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_008)

## Open

- Three of the five cases are still unconfirmed. About 3 to 4 more repeats each at S7 (09a95ffa) and S2 (023b7fcc) would show whether they lie above 0.5. If they do, they would be the third and fourth policy failures, after S25.
- Whether S1's failure is the policy's or the simulator's: check its video (it ended about 6 m off the recorded path, flagged as a possible artifact), and add repeats only if the failure is real.
- Whether S33 should count as a policy failure: test whether the ego's slowdown below its recorded speed is the policy's choice. Rerun 1c45ce3a at ego 1.0x or 1.2x, or with reactive traffic, to separate the policy from the replay car cutting in.
- A fifth scene: none of the other six scenes produced a failure. The best next step is to probe near S25's pattern (early, slow lead with a faster ego) on 19f339ba, 12855a41 and 0e899dd3.
- Budget use: many repeats went to settings that never failed (S31, S19, S17, S12). Spending them on S7 and S2 would likely have settled more cases.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 3, turned_into_actor 3, actor_hit_ego 3

- car_conflicts_3knobs_2hz_random_confirm_r6_004: no_brake_for_lead, policy at fault: yes. Going straight on a freeway, the ego was closing on the slower car 48 ahead in its lane (gap 14.3 m down to 6.2 m by the 4.7 s handoff). After taking over, the policy braked too late and too gently (6.6 to 3.7 m/s) and hit car 48's rear at 5.7 s. The rear contact on the ego came after this front collision.
- car_conflicts_3knobs_2hz_random_confirm_r6_011: no_brake_for_lead, policy at fault: yes. The ego was going straight on a multi-lane highway and closing on slower lead car 48 in its own lane. At handoff (4.7 s) the gap was about 6.2 m and shrinking at roughly 3.8 m/s. The policy braked only gently in the first half-second, then hard (6.6 → 3.7 m/s), which was too late, and the ego's front hit 48 at 5.7 s; a following car also hit the ego's rear.
- car_conflicts_3knobs_2hz_random_confirm_r6_015: turned_into_actor, policy at fault: yes. The route said RIGHT and the recorded path stayed to the right, but the policy steered left into the next lane and ended up close behind the slower car 37. It slowed only a little, from 6.8 to 5.8 m/s, while the gap shrank from 5.5 to 4.4 m, and its front hit 37's rear at 9.7 s, about 6.3 m off the recorded path.
- car_conflicts_3knobs_2hz_random_confirm_r6_021: no_brake_for_lead, policy at fault: yes. The ego was following slower lead car 48 in its own lane on a straight highway. When the policy took over at 4.7s, the gap was 6.2 m and still shrinking. The ego only braked hard late (6.6 m/s at 4.7s, 3.7 m/s at 5.7s) and hit car 48 with its front at 5.7s. The ego was also rear-ended, but that contact came after the front collision.
- car_conflicts_3knobs_2hz_random_confirm_r6_028: actor_hit_ego, policy at fault: no. The ego was going straight in its lane at about 8 m/s, staying within 0.4 m of the recorded path. Actor 24 came up from behind on the right, passed the ego, and cut left into its lane just ahead of it, clipping the ego's front-right corner at 9.2 s. The front collision is a log-replay actor merging into the ego, not a steering or braking mistake by the policy.
- car_conflicts_3knobs_2hz_random_confirm_r6_031: actor_hit_ego, policy at fault: unclear. On a straight multi-lane highway the ego kept its lane but drove more slowly than the recorded drive (8.7→7.3 m/s, about 21 m behind its recorded position). Actor 24 came up on its right, passed it, and cut left into the ego's lane right in front of it (the gap went from none to 2.9 m), so the ego's front hit the cutting-in car's side or rear.
- car_conflicts_3knobs_2hz_random_confirm_r6_041: actor_hit_ego, policy at fault: unclear. The ego was going straight and staying in its lane, but it slowed gradually with no lead nearby (8.6 → 7.3 m/s) and fell about 21 m behind the recorded drive. Actor 24, replayed from the log, came up from behind on the right, passed alongside and cut left into the ego's lane, hitting the ego's front-right corner. The ego never steered into it.
- car_conflicts_3knobs_2hz_random_confirm_r6_048: turned_into_actor, policy at fault: yes. After handoff the ego sped up from 2.5 to 5.8 m/s. The route command was RIGHT and the recorded human moved right, but the ego's plan drifted left toward actor 15's lane, putting it about 2 m left of the recorded path and across the lane line. There it side-swiped the vehicle coming up alongside in the left lane, probably actor 56. That is a lateral collision, followed by rear contact.
- car_conflicts_3knobs_2hz_random_confirm_r6_057: turned_into_actor, policy at fault: yes. After handoff, the ego slowed from 7.9 to about 4 m/s behind lead vehicle 1. Its planned path (orange) bent left toward the adjacent lane, even though the route command was STRAIGHT and then RIGHT, and the ego drifted about 1.2 m left of the recorded trajectory. Vehicle 33 was coming up from behind in that left lane, and the ego's left side struck it (collision_lateral).

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%), 1 possibly the simulator's (car_conflicts_3knobs_2hz_random_confirm_r6_010, car_conflicts_3knobs_2hz_random_confirm_r6_015, car_conflicts_3knobs_2hz_random_confirm_r6_024_a2, car_conflicts_3knobs_2hz_random_confirm_r6_035)
- S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_048, car_conflicts_3knobs_2hz_random_confirm_r6_051)
- S3: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_050)
- S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_060)
- S5: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_059)
- S6: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_002)
- S7: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_057)
- S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_019_a2)
- S9: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_005)
- S10: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_020)
- S11: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_027)
- S12: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_037, car_conflicts_3knobs_2hz_random_confirm_r6_042, car_conflicts_3knobs_2hz_random_confirm_r6_055)
- S13: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_046)
- S14: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_030)
- S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_007)
- S16: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_040, car_conflicts_3knobs_2hz_random_confirm_r6_052)
- S17: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_003, car_conflicts_3knobs_2hz_random_confirm_r6_012, car_conflicts_3knobs_2hz_random_confirm_r6_023, car_conflicts_3knobs_2hz_random_confirm_r6_032_a2)
- S18: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_038_a2, car_conflicts_3knobs_2hz_random_confirm_r6_043)
- S19: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_009, car_conflicts_3knobs_2hz_random_confirm_r6_014, car_conflicts_3knobs_2hz_random_confirm_r6_034, car_conflicts_3knobs_2hz_random_confirm_r6_045, car_conflicts_3knobs_2hz_random_confirm_r6_053)
- S20: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_049)
- S21: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_058)
- S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_018)
- S23: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_036)
- S24: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_026)
- S25: 187e6244 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_004, car_conflicts_3knobs_2hz_random_confirm_r6_011, car_conflicts_3knobs_2hz_random_confirm_r6_021)
- S26: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_029_a2)
- S27: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_006)
- S28: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_039)
- S29: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_056)
- S30: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_008)
- S31: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_001, car_conflicts_3knobs_2hz_random_confirm_r6_013, car_conflicts_3knobs_2hz_random_confirm_r6_025_a2, car_conflicts_3knobs_2hz_random_confirm_r6_033, car_conflicts_3knobs_2hz_random_confirm_r6_044, car_conflicts_3knobs_2hz_random_confirm_r6_054)
- S32: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_047_a2)
- S33: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_028, car_conflicts_3knobs_2hz_random_confirm_r6_031, car_conflicts_3knobs_2hz_random_confirm_r6_041)
- S34: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_016)
- S35: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r6_017, car_conflicts_3knobs_2hz_random_confirm_r6_022)

## Not kept by the gate

- car_conflicts_3knobs_2hz_random_confirm_r6_019: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_024: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_025: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_029: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_032: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_038: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r6_047: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 26 s; every count above is computed from the queue, not written by the model.

0 of 67 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
