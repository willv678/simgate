# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `random_confirm_r4`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Repeats confirmed only 2 of the 5 cases asked for, on different scenes. On 023b7fcc the confirmed setting is timing −1.0 s, car speed 1.0x, ego speed 0.6x (S2). On 096988dd it is timing −1.5 s, car speed 2.0x, ego speed 1.4x (S5). Every repeat at both settings failed, but there are only a few repeats, so the 90% range only just clears 0.5. The strongest unconfirmed case is 19f339ba at −0.5 s, 2.0x, 1.4x (S31): most runs there failed, but its range still reaches below 0.5. Almost every failure has the same cause, and the triage blames the policy: the ego drifts left into the next lane, against a RIGHT or STRAIGHT command, and side-swipes a car coming up alongside. That car is usually not the one the study retimed, so the knobs probably matter by changing where the ego is relative to the replayed traffic rather than through the cut-in or lead car itself. No failure was flagged as a possible simulator artifact.

## Findings

- Confirmed case 1: on 023b7fcc at timing −1.0 s, car speed 1.0x and slow ego hand-off speed 0.6x, every run failed. Each time the ego sped up, drifted about 2 m left into the next lane against a RIGHT command, and side-swiped vehicle 56 coming up behind-left. That is not the retimed car 12.
  - S2: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_028, car_conflicts_3knobs_2hz_random_confirm_r4_031, car_conflicts_3knobs_2hz_random_confirm_r4_041)
- Confirmed case 2: on 096988dd at timing −1.5 s, car speed 2.0x and fast ego hand-off speed 1.4x, every run failed. Each time the ego slowed, drifted left while the command was RIGHT, and struck vehicle 41 travelling alongside in the left lane. That is not the retimed car 2. A single run at +0.5 s with the same speeds also failed this way, which hints that on this scene car speed 2.0x and ego speed 1.4x matter more than timing.
  - S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_010, car_conflicts_3knobs_2hz_random_confirm_r4_011, car_conflicts_3knobs_2hz_random_confirm_r4_021)
  - S7: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_050)
- Best unconfirmed case: on 19f339ba at −0.5 s, 2.0x, 1.4x, most runs failed, but the range does not lie surely above 0.5. In the failures the ego braked hard on an open highway for no visible reason, with no lead car within about 40 m. It also drifted about 1 m left, so actor 1 in the left lane caught up and side-swiped it. The triage calls this the policy's fault.
  - S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_004, car_conflicts_3knobs_2hz_random_confirm_r4_012, car_conflicts_3knobs_2hz_random_confirm_r4_022, car_conflicts_3knobs_2hz_random_confirm_r4_032, car_conflicts_3knobs_2hz_random_confirm_r4_042, car_conflicts_3knobs_2hz_random_confirm_r4_051)
- Weaker hints, each resting on one or two runs. On 023b7fcc at −1.5 s, 0.5x, 1.4x, a single run rear-ended the slow lead car 12 just after hand-off; the policy swerved instead of braking, and the triage could not say whether the policy was at fault. On 09a95ffa at +1.5 s, 0.75x, 0.6x, one of two runs failed when the ego moved left into the next lane and scraped actors 33 and 1.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_047)
  - S10: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_046, car_conflicts_3knobs_2hz_random_confirm_r4_053)
- Settings that held up on 09a95ffa, 0e899dd3 and 187e6244 despite high criticality. The repeated settings never failed, and their ranges sit mostly below 0.5.
  - S9: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_018, car_conflicts_3knobs_2hz_random_confirm_r4_024, car_conflicts_3knobs_2hz_random_confirm_r4_034, car_conflicts_3knobs_2hz_random_confirm_r4_044)
  - S22: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_009, car_conflicts_3knobs_2hz_random_confirm_r4_013, car_conflicts_3knobs_2hz_random_confirm_r4_035, car_conflicts_3knobs_2hz_random_confirm_r4_045, car_conflicts_3knobs_2hz_random_confirm_r4_054)
  - S29: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_016, car_conflicts_3knobs_2hz_random_confirm_r4_023, car_conflicts_3knobs_2hz_random_confirm_r4_033, car_conflicts_3knobs_2hz_random_confirm_r4_043, car_conflicts_3knobs_2hz_random_confirm_r4_052)
  - S25: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_001, car_conflicts_3knobs_2hz_random_confirm_r4_014, car_conflicts_3knobs_2hz_random_confirm_r4_055)
- No run failed on 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41, 187e6244 or 1c45ce3a. On 0dbb91dd, criticality was zero at every setting tried, meaning the ego never came near the actor.
  - S11: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_007)
  - S12: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_027)
  - S13: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_049)
  - S14: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_048)
  - S15: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_008)
  - S16: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_019)
  - S17: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_038)
  - S18: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_005)
  - S19: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_060)
  - S20: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_058)
  - S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_006, car_conflicts_3knobs_2hz_random_confirm_r4_025)
  - S22: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_009, car_conflicts_3knobs_2hz_random_confirm_r4_013, car_conflicts_3knobs_2hz_random_confirm_r4_035, car_conflicts_3knobs_2hz_random_confirm_r4_045, car_conflicts_3knobs_2hz_random_confirm_r4_054)
  - S23: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_030)
  - S24: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_036)
  - S25: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_001, car_conflicts_3knobs_2hz_random_confirm_r4_014, car_conflicts_3knobs_2hz_random_confirm_r4_055)
  - S26: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_037)
  - S27: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_002_a3)
  - S28: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_003, car_conflicts_3knobs_2hz_random_confirm_r4_015)
  - S29: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_016, car_conflicts_3knobs_2hz_random_confirm_r4_023, car_conflicts_3knobs_2hz_random_confirm_r4_033, car_conflicts_3knobs_2hz_random_confirm_r4_043, car_conflicts_3knobs_2hz_random_confirm_r4_052)
  - S35: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_029)

## Open

- Is 19f339ba at −0.5 s, 2.0x, 1.4x (S31) really above 0.5? A few more repeats would settle it and could make it the third confirmed case.
- Do 09a95ffa at +1.5 s, 0.75x, 0.6x (S10) and 096988dd at +0.5 s, 2.0x, 1.4x (S7) fail reliably? Repeats would show it; S10 could become a fourth case on a new scene.
- Is the rear-end on 023b7fcc at −1.5 s, 0.5x, 1.4x (S1) a real failure to brake for the lead car? It ran once and the fault is unclear. Repeats and a look at the video would settle it, though it shares a scene with S2.
- The fifth distinct scene is unexplored. 12855a41 and 1c45ce3a each got only one setting, and 0cf6368d got three, none of which failed. More searching there, steered by near misses, is needed.
- Does the retimed car matter at all? In most failures the ego hits an untouched replayed car. Runs that vary only ego speed with the actor knobs held at their recorded values would show whether ego speed alone drives the left drift.
- Why does the policy drift left against a RIGHT command and brake hard on 19f339ba? The study cannot explain either; both point to a policy behaviour worth examining apart from the knobs.
- Two runs at 187e6244 (−1.0 s, 1.5x, 1.2x) were thrown out by the validity gate and re-run; they are not evidence.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, other 2, no_brake_for_lead 1

- car_conflicts_3knobs_2hz_random_confirm_r4_010: turned_into_actor, policy at fault: yes. On a multi-lane highway, the route command switched to RIGHT, but after handoff the ego's planned path drifted left, toward the adjacent lane. Vehicle 41 was overtaking in that lane, coming up from behind-left, and the ego's front struck its side as the ego moved into the lane.
- car_conflicts_3knobs_2hz_random_confirm_r4_011: turned_into_actor, policy at fault: yes. On a multi-lane freeway with the command STRAIGHT and then RIGHT, the ego slowed from 7.9 to 5.0 m/s and drifted left, away from the recorded path, into the next lane. Actor 41 was coming up alongside in that lane, and the ego's front ran into it at 7.7 s.
- car_conflicts_3knobs_2hz_random_confirm_r4_012: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no lead vehicle within about 45 m, the ego braked hard for no visible reason (23.7 to 7.5 m/s) while its path wobbled left. Because it slowed so much, actor 1 (a logged car in the lane to the left and behind) caught up beside it, and the ego's leftward drift (1.3 m off the recorded path) caused a side collision; the rear contact also came from the unexplained braking.
- car_conflicts_3knobs_2hz_random_confirm_r4_021: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was slowing (7.9 to 4.9 m/s) and drifted left toward the adjacent lane, even though the command was RIGHT and the recorded path bore slightly right. It hit vehicle 41, which was travelling alongside in that left lane.
- car_conflicts_3knobs_2hz_random_confirm_r4_028: turned_into_actor, policy at fault: yes. Starting at the 4.7 s handoff, the ego sped up from about 2.5 to 5.9 m/s in slow highway traffic. Although the route command was STRAIGHT and then RIGHT, it moved about 2 m to the left of the recorded path, into the next lane, where actor 56 was coming up close behind on the left, and at 7.7 s the two collided side to side (a rear contact was also logged).
- car_conflicts_3knobs_2hz_random_confirm_r4_031: turned_into_actor, policy at fault: yes. After handoff, the ego sped up from 2.5 to 5.8 m/s and drifted left across the lane line into the adjacent left lane. The recorded path and the route command (RIGHT) both went the other way, and it side-swiped a vehicle there (likely actor 56, just behind-left) at 7.7s. The rear contact noted in the run came after this at-fault side collision.
- car_conflicts_3knobs_2hz_random_confirm_r4_032: other, policy at fault: yes. After handoff at 4.6 s, the ego braked hard on an open highway, going from 23.7 to 7.3 m/s, even though the nearest car ahead was more than 43 m away. It also drifted about 1.1 m left of the recorded path, so actor 1, coming up from behind in the left lane, sideswiped it at 7.6 s (side impact, with rear contact also reported).
- car_conflicts_3knobs_2hz_random_confirm_r4_041: turned_into_actor, policy at fault: yes. The ego was moving slowly in dense multi-lane traffic. The command was STRAIGHT, then RIGHT, and the green route curves right, but the ego drifted left onto the lane line instead, ending up 2.1 m from the recorded path. There it side-swiped vehicle 56, which was coming up in the left lane just behind and beside it. The contact was logged as a lateral at-fault collision; the rear-contact flag probably comes from the same contact with 56.
- car_conflicts_3knobs_2hz_random_confirm_r4_042: turned_into_actor, policy at fault: yes. On an open highway, the ego braked hard for no clear reason, slowing from 23.7 to 7.4 m/s even though the nearest vehicle ahead was more than 40 m away. At the same time it drifted left off the recorded path toward the left lane. Actor 1 was coming up from behind in that left lane, drew level as the ego slowed, and the ego's front-left hit it.
- car_conflicts_3knobs_2hz_random_confirm_r4_047: no_brake_for_lead, policy at fault: unclear. The ego was going straight in a highway lane and closing on slower lead car 12 (gap 14.6 m down to 5.5 m at handoff, about 6 m/s against roughly 2.5 m/s). The policy only slowed from 6.0 to 5.4 m/s and hit 12's rear 0.5 s after taking over. Its predicted path was swerving left, not braking.
- car_conflicts_3knobs_2hz_random_confirm_r4_050: turned_into_actor, policy at fault: yes. On the highway, under a STRAIGHT then RIGHT command, the ego slowed and drifted left over the lane line, about 1.9 m off the recorded path. Its front-left hit car 41, which was coming up alongside in the left lane.
- car_conflicts_3knobs_2hz_random_confirm_r4_051: other, policy at fault: yes. With no vehicle close ahead (the lead was 43–52 m away and pulling away), the ego braked hard on a clear highway, from 23.7 to 7.5 m/s in 3 s, while drifting about 1.2 m left of the recorded path. Actor 1 kept its recorded speed in the lane to the left and behind, caught up with the ego and side-swiped it. That was counted as a lateral at-fault collision, and the ego was also rear-ended.
- car_conflicts_3knobs_2hz_random_confirm_r4_053: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego left its recorded lane and moved about 2.6 m left into the next lane, directly behind actor 33 and next to actor 1. Its side scraped them (a lateral collision, already active by 9.6 s, with the gap ahead near 0 at 8.6 s). It kept going at about 7 m/s wedged against the vehicles, even though the command was RIGHT/STRAIGHT and the route stayed in the original lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_047)
- S2: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_028, car_conflicts_3knobs_2hz_random_confirm_r4_031, car_conflicts_3knobs_2hz_random_confirm_r4_041)
- S3: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_056)
- S4: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_020)
- S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_010, car_conflicts_3knobs_2hz_random_confirm_r4_011, car_conflicts_3knobs_2hz_random_confirm_r4_021)
- S6: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_040)
- S7: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_050)
- S8: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_059)
- S9: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_018, car_conflicts_3knobs_2hz_random_confirm_r4_024, car_conflicts_3knobs_2hz_random_confirm_r4_034, car_conflicts_3knobs_2hz_random_confirm_r4_044)
- S10: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_046, car_conflicts_3knobs_2hz_random_confirm_r4_053)
- S11: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_007)
- S12: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_027)
- S13: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_049)
- S14: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_048)
- S15: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_008)
- S16: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_019)
- S17: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_038)
- S18: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_005)
- S19: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_060)
- S20: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_058)
- S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_006, car_conflicts_3knobs_2hz_random_confirm_r4_025)
- S22: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_009, car_conflicts_3knobs_2hz_random_confirm_r4_013, car_conflicts_3knobs_2hz_random_confirm_r4_035, car_conflicts_3knobs_2hz_random_confirm_r4_045, car_conflicts_3knobs_2hz_random_confirm_r4_054)
- S23: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_030)
- S24: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_036)
- S25: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_001, car_conflicts_3knobs_2hz_random_confirm_r4_014, car_conflicts_3knobs_2hz_random_confirm_r4_055)
- S26: 187e6244 at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_037)
- S27: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_002_a3)
- S28: 187e6244 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_003, car_conflicts_3knobs_2hz_random_confirm_r4_015)
- S29: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_016, car_conflicts_3knobs_2hz_random_confirm_r4_023, car_conflicts_3knobs_2hz_random_confirm_r4_033, car_conflicts_3knobs_2hz_random_confirm_r4_043, car_conflicts_3knobs_2hz_random_confirm_r4_052)
- S30: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_057)
- S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 4/6 failed, rate 35%-88% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_004, car_conflicts_3knobs_2hz_random_confirm_r4_012, car_conflicts_3knobs_2hz_random_confirm_r4_022, car_conflicts_3knobs_2hz_random_confirm_r4_032, car_conflicts_3knobs_2hz_random_confirm_r4_042, car_conflicts_3knobs_2hz_random_confirm_r4_051)
- S32: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_017)
- S33: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_026)
- S34: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_039)
- S35: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_random_confirm_r4_029)

## Not kept by the gate

- car_conflicts_3knobs_2hz_random_confirm_r4_002: not kept: RE-RUN
- car_conflicts_3knobs_2hz_random_confirm_r4_002_a2: not kept: RE-RUN

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

0 of 62 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
