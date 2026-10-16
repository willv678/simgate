# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_r3`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: only one combination is confirmed as challenging. On scene 096988dd, with the car at its recorded timing, the car at 1.25x speed and the ego at 1.2x, every repeat failed (S3). In each of those runs the policy drifted left out of its lane and hit a car overtaking in the left lane. The other strong candidate is scene 19f339ba with the car at 2x. There most runs failed at ego 1.2x and 1.4x (S24, S25), but the ranges still reach below 0.5, so neither is confirmed. The failures there follow one pattern: the policy brakes hard for no visible reason and drifts left into the car alongside. On the eight other scenes the study found no failure the policy caused. Most settings there got only one or two runs, and large parts of the space were never tried, so this does not show those scenes are safe.

## Findings

- On 096988dd, with the car at its recorded timing and 1.25x speed, raising the ego's speed to 1.2x turns a passing setting into one that failed in every repeat. This is the one confirmed challenging case. All its failures were the policy's: it drifted left into vehicle 41, which was overtaking in the left lane, even though the route command was RIGHT.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_019, car_conflicts_3knobs_2hz_hybrid_r3_021, car_conflicts_3knobs_2hz_hybrid_r3_022, car_conflicts_3knobs_2hz_hybrid_r3_023)
  - S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_002, car_conflicts_3knobs_2hz_hybrid_r3_017)
- On the same scene, raising the car's speed to 1.5x at the recorded ego speed also failed in the same way, a leftward drift into vehicle 41. It rests on a single run, so it is a hint, not a rate.
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_018)
- On 19f339ba, the car at 2x speed is where failures appear. Lower car speeds there did not fail. At 2x, failures were mixed at the recorded ego speed and more frequent at ego 1.2x and 1.4x, but none of these settings is confirmed above 0.5.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 2/5 failed, rate 14%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_028, car_conflicts_3knobs_2hz_hybrid_r3_031, car_conflicts_3knobs_2hz_hybrid_r3_032, car_conflicts_3knobs_2hz_hybrid_r3_033, car_conflicts_3knobs_2hz_hybrid_r3_049)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_048, car_conflicts_3knobs_2hz_hybrid_r3_047_a2, car_conflicts_3knobs_2hz_hybrid_r3_055, car_conflicts_3knobs_2hz_hybrid_r3_056)
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_051, car_conflicts_3knobs_2hz_hybrid_r3_052, car_conflicts_3knobs_2hz_hybrid_r3_053, car_conflicts_3knobs_2hz_hybrid_r3_054)
  - S20: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_029)
  - S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_004)
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_020)
- The failures on 19f339ba share one cause that is the policy's fault: hard braking on an open road with no close lead, combined with a drift left until the ego's front or side hits actor 1 in the adjacent lane. The rear-end hits that followed came from the braking and do not count.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 2/5 failed, rate 14%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_028, car_conflicts_3knobs_2hz_hybrid_r3_031, car_conflicts_3knobs_2hz_hybrid_r3_032, car_conflicts_3knobs_2hz_hybrid_r3_033, car_conflicts_3knobs_2hz_hybrid_r3_049)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_048, car_conflicts_3knobs_2hz_hybrid_r3_047_a2, car_conflicts_3knobs_2hz_hybrid_r3_055, car_conflicts_3knobs_2hz_hybrid_r3_056)
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_051, car_conflicts_3knobs_2hz_hybrid_r3_052, car_conflicts_3knobs_2hz_hybrid_r3_053, car_conflicts_3knobs_2hz_hybrid_r3_054)
- In both failing scenes, the car the ego hit was a neighbour in the left lane, not the retimed cut-in or lead car (track 2 on 096988dd, track 18 on 19f339ba). Retiming seems to set up the conditions, and the policy's lateral drift causes the crash.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_019, car_conflicts_3knobs_2hz_hybrid_r3_021, car_conflicts_3knobs_2hz_hybrid_r3_022, car_conflicts_3knobs_2hz_hybrid_r3_023)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_018)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 2/5 failed, rate 14%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_028, car_conflicts_3knobs_2hz_hybrid_r3_031, car_conflicts_3knobs_2hz_hybrid_r3_032, car_conflicts_3knobs_2hz_hybrid_r3_033, car_conflicts_3knobs_2hz_hybrid_r3_049)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_048, car_conflicts_3knobs_2hz_hybrid_r3_047_a2, car_conflicts_3knobs_2hz_hybrid_r3_055, car_conflicts_3knobs_2hz_hybrid_r3_056)
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_051, car_conflicts_3knobs_2hz_hybrid_r3_052, car_conflicts_3knobs_2hz_hybrid_r3_053, car_conflicts_3knobs_2hz_hybrid_r3_054)
- The failures on 1c45ce3a, with the car 0.5 s earlier at 1.25x, were not shown to be the policy's. In one, the triage cleared the policy; in the other, fault was unclear. In both, replayed actor 24 came up from behind and moved into the slower ego. This setting does not count as a challenging case, and its range already stays below 0.5.
  - S27: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 2/8 failed, rate 9%-54% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_026, car_conflicts_3knobs_2hz_hybrid_r3_034, car_conflicts_3knobs_2hz_hybrid_r3_035, car_conflicts_3knobs_2hz_hybrid_r3_036, car_conflicts_3knobs_2hz_hybrid_r3_041, car_conflicts_3knobs_2hz_hybrid_r3_042, car_conflicts_3knobs_2hz_hybrid_r3_043, car_conflicts_3knobs_2hz_hybrid_r3_044)
- On 1c45ce3a, no other setting tried failed, including four repeats with the car 0.5 s later at 1.5x.
  - S26: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_045, car_conflicts_3knobs_2hz_hybrid_r3_046)
  - S28: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_010, car_conflicts_3knobs_2hz_hybrid_r3_011)
  - S29: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_013)
  - S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_012)
  - S31: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_027)
  - S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_057, car_conflicts_3knobs_2hz_hybrid_r3_058, car_conflicts_3knobs_2hz_hybrid_r3_059, car_conflicts_3knobs_2hz_hybrid_r3_060)
- No failure was found on 09a95ffa, 12855a41 or 0e899dd3 across the car speeds from 1.25x to 2x and the ego speeds from 1x to 1.2x tried there. Most of these settings got only one run.
  - S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_037)
  - S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_008, car_conflicts_3knobs_2hz_hybrid_r3_014)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_016)
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_015, car_conflicts_3knobs_2hz_hybrid_r3_050)
  - S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_025)
  - S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_024)
  - S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_009)
  - S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_038)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_040)
  - S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_003)
  - S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_039)
  - S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_030)
- 023b7fcc, 0cf6368d, 0dbb91dd and 187e6244 got a single run each, all at one setting: car 1.25x, recorded timing, recorded ego speed. None failed, so these scenes are essentially unexplored.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_001)
  - S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_007)
  - S12: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_006)
  - S19: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_005)

## Open

- Whether 19f339ba with the car at 2x is a confirmed case: a few more repeats at ego 1.2x and 1.4x (S24, S25) would settle whether the rate lies above 0.5. If every new run fails, that would bring this scene to a second confirmed case.
- Whether the car at 1.5x on 096988dd (S4) fails as reliably as S3: repeats there would show whether the scene fails across a range of car speeds or only near one combination. It would not add a new scene, though.
- Large parts of the space were never tried on any scene: the car slower than recorded (0.5x to 1x, the natural stress for lead-vehicle scenes), the ego slower than recorded (0.6x to 1x), and timing shifts beyond ±1 s. Runs in those regions are needed before anyone concludes that the eight non-failing scenes are hard to break.
- Four scenes (023b7fcc, 0cf6368d, 0dbb91dd, 187e6244) got only one run each. A few runs per scene with a faster ego and a slower or earlier car would show whether they hold any failures at all.
- On 1c45ce3a, it is still unclear whether the policy's unexplained slowdown (which let actor 24 merge into it) counts as the policy's failure. The triage cleared the policy in one case and left the other unclear. A decision on how to score replay cars that merge into a slowed ego would settle whether this setting counts.
- The confirmed failures come from a leftward drift into adjacent-lane traffic, which does not depend on the retimed car. It is open whether this is a general weakness of the policy on multi-lane highways at 2 Hz. Repeating the failing scenes with the retimed car left at its recorded setting but with a faster ego would separate the two effects.

## Why the runs failed (triage from the video and log)

turned_into_actor 13, actor_hit_ego 2

- car_conflicts_3knobs_2hz_hybrid_r3_018: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (turning to RIGHT at the end), the policy planned a drift into the lane on its left, away from the recorded path that kept to its lane or went right. Vehicle 41 was overtaking in that left lane, and the ego's front-left cut into it as the car came alongside at about 4.6 m/s.
- car_conflicts_3knobs_2hz_hybrid_r3_019: turned_into_actor, policy at fault: yes. On a multi-lane highway with a RIGHT command, the ego drifted left about 1.6 m from the recorded path, into the left lane. Actor 41, a white pickup, was overtaking on its left in that lane, and the ego's front corner hit it as the pickup came alongside and pulled ahead.
- car_conflicts_3knobs_2hz_hybrid_r3_021: turned_into_actor, policy at fault: yes. On a multi-lane highway, the planned route bore right (the command changed from STRAIGHT to RIGHT), but the ego drifted left out of its lane. By 7.7s it was about 1.7 m left of the recorded path, and its front corner hit car 41, which was driving alongside in the left lane. The car ahead stayed about 20 m away until the impact, so this was not a failure to brake for a lead vehicle; the ego moved sideways into a neighbouring car.
- car_conflicts_3knobs_2hz_hybrid_r3_022: turned_into_actor, policy at fault: yes. On a multi-lane highway, the command switched from STRAIGHT to RIGHT, but the policy's orange plan bent left. The ego slowed from 6.7 to 4.3 m/s and drifted left toward the next lane, about 1.6 m off the recorded path. Its front hit pickup 41, which was passing on its left in that lane.
- car_conflicts_3knobs_2hz_hybrid_r3_023: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego drifted left out of its lane, toward the left lane line, even though the route command was RIGHT. Its front clipped vehicle 41, which was driving alongside in the adjacent left lane, at about 4.4 m/s.
- car_conflicts_3knobs_2hz_hybrid_r3_026: actor_hit_ego, policy at fault: no. On a straight highway, the ego stayed in its lane on the recorded path (0.1 m off) but slowed from 9.8 to 8.1 m/s and fell about 23 m behind where the human car was at that point. Replayed actor 24 came up from behind on the right and cut into the ego's front-right corner at 10.2 s, so the contact was logged as an at-fault front collision; the ego was also rear-ended at some point in the run.
- car_conflicts_3knobs_2hz_hybrid_r3_028: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy slowed from 16.9 to 9.3 m/s for no apparent reason and drifted left off the recorded path onto the lane line. Its front corner hit actor 1, which was driving normally in the adjacent left lane; the later rear contact came after this, likely caused by the unexplained braking.
- car_conflicts_3knobs_2hz_hybrid_r3_034: actor_hit_ego, policy at fault: unclear. The ego held its lane on the recorded path (0.17 m off) but drove slower than the human with no lead ahead (10.1 to 8.4 m/s), so by 9.7 s it was 18 m behind where the logged car was. Actor 24 came up from behind on the right and moved into the ego's lane, hitting its right side. Most likely the replayed actor was merging into a gap that existed in the log but that the slower ego was now occupying.
- car_conflicts_3knobs_2hz_hybrid_r3_048: turned_into_actor, policy at fault: yes. On a straight highway with nothing ahead, the policy braked hard for no visible reason (20.6 to 9.8 m/s) and drifted about 1 m left toward the next lane. Its front-left corner then struck actor 1, which was beside it in the left lane. The ego was also hit from behind at some point, probably because of the unneeded braking, but the at-fault contact was the ego's front clipping the car alongside as it drifted left.
- car_conflicts_3knobs_2hz_hybrid_r3_049: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the ego braked hard for no reason, slowing from 16.9 to 9.6 m/s with no lead closer than about 50 m, and fell behind where the human drove. At the same time it drifted left toward the adjacent lane. Its front-left clipped the rear of actor 1 in that lane, and it was also rear-ended because of the sudden braking.
- car_conflicts_3knobs_2hz_hybrid_r3_051: turned_into_actor, policy at fault: yes. On an open highway with the nearest car ahead more than 40 m away, the ego braked hard for no visible reason, slowing from 23.7 to 7.5 m/s. At the same time it drifted left toward the next lane, and its side hit vehicle 1, which was coming up alongside on its left.
- car_conflicts_3knobs_2hz_hybrid_r3_053: turned_into_actor, policy at fault: yes. After handoff the ego braked hard (23.7 to 7.4 m/s) on an open highway with no close lead, while drifting left toward the lane line. Actor 1, which had been behind in the left lane, drew level as the ego slowed, and the ego's front-left corner hit its side.
- car_conflicts_3knobs_2hz_hybrid_r3_054: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the ego braked hard for no visible reason, from 23.7 to 7.3 m/s, with no lead within 43 m. As it slowed, it wobbled and angled left, and its side hit actor 1, which was coming up alongside in the left lane. The ego was also rear-ended during the run, and a smear in the reconstructed road ahead may have prompted the phantom braking, but the at-fault side impact came from the ego drifting left.
- car_conflicts_3knobs_2hz_hybrid_r3_055: turned_into_actor, policy at fault: yes. On an open highway with nothing close ahead, the ego braked hard (20 → 9 m/s) for no visible reason and drifted about 1.35 m left of the recorded path, toward the left lane line. Actor 1, which was driving in the left lane, came up alongside it, and the ego's front-left clipped that car. The heavy braking also explains the separate rear-end contact.
- car_conflicts_3knobs_2hz_hybrid_r3_056: turned_into_actor, policy at fault: yes. After handoff the ego braked hard for no visible reason, from 20.3 to 9.2 m/s, while the human's recorded car kept going ahead. It also drifted left toward the lane line, so actor 1, overtaking in the left lane, ended up beside the ego's front-left corner, and the ego clipped it. The ego was later rear-ended too, probably as a result of the hard braking.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_001)
- S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_002, car_conflicts_3knobs_2hz_hybrid_r3_017)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_019, car_conflicts_3knobs_2hz_hybrid_r3_021, car_conflicts_3knobs_2hz_hybrid_r3_022, car_conflicts_3knobs_2hz_hybrid_r3_023)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_018)
- S5: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_037)
- S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_008, car_conflicts_3knobs_2hz_hybrid_r3_014)
- S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_016)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_015, car_conflicts_3knobs_2hz_hybrid_r3_050)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_025)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_024)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_007)
- S12: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_006)
- S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_009)
- S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_038)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_040)
- S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_003)
- S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_039)
- S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_030)
- S19: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_005)
- S20: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_029)
- S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_004)
- S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_020)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 2/5 failed, rate 14%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_028, car_conflicts_3knobs_2hz_hybrid_r3_031, car_conflicts_3knobs_2hz_hybrid_r3_032, car_conflicts_3knobs_2hz_hybrid_r3_033, car_conflicts_3knobs_2hz_hybrid_r3_049)
- S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_048, car_conflicts_3knobs_2hz_hybrid_r3_047_a2, car_conflicts_3knobs_2hz_hybrid_r3_055, car_conflicts_3knobs_2hz_hybrid_r3_056)
- S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.4: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_051, car_conflicts_3knobs_2hz_hybrid_r3_052, car_conflicts_3knobs_2hz_hybrid_r3_053, car_conflicts_3knobs_2hz_hybrid_r3_054)
- S26: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_045, car_conflicts_3knobs_2hz_hybrid_r3_046)
- S27: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 2/8 failed, rate 9%-54% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_026, car_conflicts_3knobs_2hz_hybrid_r3_034, car_conflicts_3knobs_2hz_hybrid_r3_035, car_conflicts_3knobs_2hz_hybrid_r3_036, car_conflicts_3knobs_2hz_hybrid_r3_041, car_conflicts_3knobs_2hz_hybrid_r3_042, car_conflicts_3knobs_2hz_hybrid_r3_043, car_conflicts_3knobs_2hz_hybrid_r3_044)
- S28: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_010, car_conflicts_3knobs_2hz_hybrid_r3_011)
- S29: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_013)
- S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_012)
- S31: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_027)
- S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_r3_057, car_conflicts_3knobs_2hz_hybrid_r3_058, car_conflicts_3knobs_2hz_hybrid_r3_059, car_conflicts_3knobs_2hz_hybrid_r3_060)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_r3_047: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 28 s; every count above is computed from the queue, not written by the model.

0 of 61 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
