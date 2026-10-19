# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `llm_v2_r4`: 49 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The goal was met: five settings on five different scenes failed in every repeat (S1, S9, S20, S33, S37). All of them combine the fastest ego speed at hand-off (1.4x) with the slowest retimed car (0.5x). Only the timing of the car differs, from 2 s early to 1 s late. Each setting has only a few repeats, so its 90% range only just clears 0.5. These settings are confirmed as failing, but how often each one fails is not pinned down. Only two of the five are clearly the policy's fault: S9 and S37, where it drifted left into a car in the next lane. At S20 and S33 the faster replayed ego had already closed to a few metres behind a slower lead car before hand-off, with about 0.5 s left. Those failures may come from the setup rather than the policy. S1 is mixed.

## Findings

- Every confirmed failure, and every failure at all, came at ego speed 1.4x with the retimed car at 0.5x speed. The search almost never left that corner: it ran almost nothing at ego speeds below 1.4x and little at car speeds above 0.5x. So this is the only combination shown to fail, not the only one that can.
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_035, car_conflicts_3knobs_2hz_llm_v2_r4_043, car_conflicts_3knobs_2hz_llm_v2_r4_044_a2)
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_036, car_conflicts_3knobs_2hz_llm_v2_r4_041, car_conflicts_3knobs_2hz_llm_v2_r4_042)
  - S9: 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_002, car_conflicts_3knobs_2hz_llm_v2_r4_011, car_conflicts_3knobs_2hz_llm_v2_r4_012)
  - S10: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_047)
  - S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_048)
  - S20: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_022, car_conflicts_3knobs_2hz_llm_v2_r4_031, car_conflicts_3knobs_2hz_llm_v2_r4_032)
  - S33: 187e6244 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_028, car_conflicts_3knobs_2hz_llm_v2_r4_033, car_conflicts_3knobs_2hz_llm_v2_r4_034)
  - S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_005, car_conflicts_3knobs_2hz_llm_v2_r4_013, car_conflicts_3knobs_2hz_llm_v2_r4_014)
  - S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_025)
  - S6: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_024)
  - S22: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_023)
  - S27: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_046)
  - S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_026)
  - S35: 187e6244 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_029)
- On 096988dd, with the car 1 s late, the policy failed in every repeat because of its own error. On a straight freeway with a STRAIGHT command, its plan bent left and the ego drifted into the next lane and hit a car there. With the car at its recorded timing, the run on this scene did not fail.
  - S9: 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_002, car_conflicts_3knobs_2hz_llm_v2_r4_011, car_conflicts_3knobs_2hz_llm_v2_r4_012)
  - S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_001)
- On 19f339ba, at the recorded timing, the policy failed in every repeat because of its own error. With nothing close ahead, it braked hard for no visible reason and drifted left into a car overtaking in the left lane.
  - S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_005, car_conflicts_3knobs_2hz_llm_v2_r4_013, car_conflicts_3knobs_2hz_llm_v2_r4_014)
- On 0e899dd3 (car 1 s early) and 187e6244 (car 1 s early), every repeat was a rear-end hit on a slower lead car about 0.5 s after hand-off. Before hand-off the replayed ego, at 1.4x speed, had already closed to a few metres behind it. Triage marks these as not clearly the policy's fault, and one as not its fault. The policy did brake too gently, but these two confirmed cases may say more about the setup than about the policy. The same scenes at other timings did not fail.
  - S20: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_022, car_conflicts_3knobs_2hz_llm_v2_r4_031, car_conflicts_3knobs_2hz_llm_v2_r4_032)
  - S33: 187e6244 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_028, car_conflicts_3knobs_2hz_llm_v2_r4_033, car_conflicts_3knobs_2hz_llm_v2_r4_034)
  - S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_020)
  - S23: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_021)
  - S34: 187e6244 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_009)
  - S36: 187e6244 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_017)
- On 023b7fcc, with the car 2 s or 1.5 s early, every repeat hit the slower lead car from behind. In some runs the policy clearly braked too gently and steered left with time to avoid the hit. Others look like the same too-little-time-after-hand-off problem. With the car 1 s early or later, the single runs did not fail.
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_035, car_conflicts_3knobs_2hz_llm_v2_r4_043, car_conflicts_3knobs_2hz_llm_v2_r4_044_a2)
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_036, car_conflicts_3knobs_2hz_llm_v2_r4_041, car_conflicts_3knobs_2hz_llm_v2_r4_042)
  - S3: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_015)
  - S4: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_003)
  - S7: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_004)
- On 09a95ffa, with the car 2 s or 1.5 s early, single runs failed in the same rear-end pattern. This is a hint, not a confirmed rate.
  - S10: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_047)
  - S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_048)
  - S12: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_039)
  - S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_019)
  - S14: 09a95ffa at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_030)
- No failure was found on 12855a41, 0cf6368d or 0dbb91dd, although the timings tried on 12855a41 cover most of the range. Scene 1c45ce3a has no kept runs.
  - S15: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_049)
  - S16: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_040)
  - S17: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_007)
  - S18: 0dbb91dd at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_050)
  - S19: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_008)
  - S24: 12855a41 at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_038)
  - S25: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_045)
  - S26: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_010)
  - S27: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_046)
  - S28: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_037)
  - S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_006)
  - S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_026)
  - S31: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_027)
  - S32: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_016)

## Open

- Whether the rear-end failures (S1, S2, S20, S33, S10, S11) are the policy's: the ego hands off already a few metres behind the lead car. Re-running these settings with hand-off earlier, or with the ego handed off at its recorded speed and only the car slowed, would separate the policy's errors from what the setup causes.
- Whether failures happen anywhere other than the corner with ego at 1.4x and the car at 0.5x: no runs used ego speeds below 1.4x or car speeds above 1, so the rest of the three-knob space is unexplored.
- The failure rates themselves: more repeats at S1, S9, S20, S33 and S37 would move their lower bounds well above 0.5. Repeats at S10 and S11 would show whether 09a95ffa is a confirmed case.
- Scene 1c45ce3a was never run successfully (re-run, then halt), so it is untested.
- The lane drift seen at S9 and S37 also happened without a close lead car. Runs at lower car-speed changes on 096988dd and 19f339ba would show whether it depends on the knobs at all.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 13, turned_into_actor 6, other 1

- car_conflicts_3knobs_2hz_llm_v2_r4_002: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's planned path (orange) bent left, away from the recorded route (green). The ego slowed from 7.9 to 4.7 m/s while drifting into the lane to its left, and its front-left hit vehicle 41, which was travelling just ahead of it in that lane.
- car_conflicts_3knobs_2hz_llm_v2_r4_005: turned_into_actor, policy at fault: yes. On an open highway, with the nearest lead vehicle 40+ m ahead, the ego braked hard for no visible reason (23.7 → 6.9 m/s) and drifted left. Actor 1, coming up from behind in the left lane, drew level, and the ego's front-left corner swiped it.
- car_conflicts_3knobs_2hz_llm_v2_r4_011: turned_into_actor, policy at fault: yes. On a straight multi-lane freeway, the policy's planned path drifted left out of its lane while the recorded route stayed straight, then bent right. The ego's front hit actor 41, a white pickup driving alongside in the lane to the left, at 7.7 s.
- car_conflicts_3knobs_2hz_llm_v2_r4_012: turned_into_actor, policy at fault: yes. On a straight multi-lane freeway, the policy's path (orange) left the route (green) and slowly drifted the ego left into the next lane while it slowed from 7.9 to 5 m/s. Actor 41 was coming up faster in that left lane, and the ego's front-left cut into it as the two came alongside at 7.7 s.
- car_conflicts_3knobs_2hz_llm_v2_r4_013: turned_into_actor, policy at fault: yes. On an open multi-lane highway, the ego braked hard for no visible reason (23.7 to 7.2 m/s, with nothing ahead closer than about 43 m). As it slowed, it drifted left toward the lane line, and its front corner hit actor 1, which was catching up in the adjacent left lane. The rear contact flagged in the run came after this front collision.
- car_conflicts_3knobs_2hz_llm_v2_r4_014: turned_into_actor, policy at fault: yes. On an open highway with no close lead, the ego braked hard (18 to 4.4 m/s) for no reason and drifted left towards the left lane line. It hit actor 1 on the side as actor 1 overtook in the left lane; a following car (actor 28) then came up on the slowed ego from behind.
- car_conflicts_3knobs_2hz_llm_v2_r4_022: no_brake_for_lead, policy at fault: unclear. The ego was going straight in dense highway traffic at about 9.5 m/s and closing on a slower blue pickup (actor 5) in its lane. The gap shrank from 21 m to 6.3 m before the policy took over at 4.7 s. In the 0.5 s it had, the policy slowed only from 9.3 to 7.6 m/s and its front hit the pickup at 5.2 s. Actor 12 also made rear contact.
- car_conflicts_3knobs_2hz_llm_v2_r4_028: no_brake_for_lead, policy at fault: unclear. The ego was going straight on the highway and following the log (0.05–0.1 m off) when the white sedan ahead in its lane (actor 48) slowed. The gap shrank from 18.6 m to 4.8 m at handoff (4.7 s, ego at 7.7 m/s). The policy braked only slightly, to 6.7 m/s, and hit the car's rear 0.5 s later at 5.2 s. Separately, at some point an actor also hit the ego's rear.
- car_conflicts_3knobs_2hz_llm_v2_r4_031: other, policy at fault: no. The ego was still replaying the human drive and closing at about 6 m/s on slower pickup 5 ahead in its lane. When the policy took over at 4.7 s the gap was only 6.3 m, and the front collision came 0.5 s later even though the policy braked (9.3 to 7.6 m/s). At impact the ego was only 0.1–0.6 m from where the human actually drove, so the collision most likely comes from the replayed setup or the lead actor's box placement, not from a policy decision. Actor 12 also hit the ego from behind.
- car_conflicts_3knobs_2hz_llm_v2_r4_032: no_brake_for_lead, policy at fault: unclear. The ego was following a slower blue pickup (actor 5) in its lane on a multi-lane highway, and the front of the ego hit the pickup's rear at 5.2s. The policy took over at 4.7s, only 0.5s before the impact, when the ego was already 6.3m behind the pickup at 9.3 m/s and closing at about 6 m/s. In that half second it braked to 7.6 m/s, which was not enough. The ego was still on the recorded human path (0.0m off), so most of the closing happened before handoff. The collision may also partly come from a mismatch between the logged actor box and the human's actual path.
- car_conflicts_3knobs_2hz_llm_v2_r4_033: no_brake_for_lead, policy at fault: unclear. On a straight multi-lane highway, the ego was closing on a slower white sedan (actor 48) in its lane at about 5 m/s. Takeover came at 4.7 s with only 4.8 m of gap left, and the policy slowed only from 7.7 to 6.7 m/s, so the ego hit the sedan's rear 0.5 s later; the ego was also rear-ended at some point.
- car_conflicts_3knobs_2hz_llm_v2_r4_034: no_brake_for_lead, policy at fault: unclear. The ego was going straight on a busy freeway and closing on slower lead car 48 in its own lane. At handoff (4.7 s) the gap was only 4.8 m and closing at about 5 m/s. The policy slowed only from 7.7 to 6.7 m/s and planned a swerve left toward vehicle 5's lane instead of braking hard, so it hit 48 from behind at 5.2 s. The ego was rear-ended afterwards.
- car_conflicts_3knobs_2hz_llm_v2_r4_035: no_brake_for_lead, policy at fault: yes. On a multi-lane highway with the command STRAIGHT, the ego was following slower lead vehicle 12 in its own lane. The gap had been shrinking since before handoff (14 m to 6.8 m at handoff), and the policy only eased from 6.0 to 4.4 m/s while its planned path started to bend left. It hit 12's rear with its front at 5.7 s, about 1 s after taking over and before any rear contact.
- car_conflicts_3knobs_2hz_llm_v2_r4_036: no_brake_for_lead, policy at fault: unclear. The ego was following a slower dark sedan (actor 12) in its lane and closing on it, with the gap shrinking from 14.6 m to 5.5 m before the policy took over at 4.7 s. In its 0.5 s of control it braked only lightly (6.0 to 5.4 m/s) and hit the sedan's rear at 5.2 s, still within 0.6 m of where the human drove.
- car_conflicts_3knobs_2hz_llm_v2_r4_041: no_brake_for_lead, policy at fault: unclear. The ego was following slower lead car 12 in the same lane on a straight multi-lane road, and the gap kept shrinking (14.6 m to 4.1 m). It front-collided with car 12 at 5.2 s, only 0.5 s after the policy took over at 4.7 s. In that time it braked only gently (6.0 to 5.4 m/s), and the ego was still almost exactly on the recorded human path (0.0 m off), so the closing-in mostly came from the replayed part of the drive or from where the lead car's box was placed.
- car_conflicts_3knobs_2hz_llm_v2_r4_042: no_brake_for_lead, policy at fault: yes. The ego was in slow freeway traffic and closing on a slower car (actor 12) in its own lane. After the policy took over at 4.7 s (gap about 5.5 m, ego at 6 m/s), it only slowed to 5.4 m/s and planned a late swerve to the left, and its front hit actor 12 at 5.2 s. Hard braking at handoff could still have avoided the hit. A rear contact also happened, but after the front collision.
- car_conflicts_3knobs_2hz_llm_v2_r4_043: no_brake_for_lead, policy at fault: yes. The ego was going straight in slow highway traffic and closing on the slower dark sedan ahead in its lane (actor 12). The policy took over at 4.7 s with a 6.8 m gap that was shrinking by about 3.5 m/s. It braked only gently, from 6.0 to 4.4 m/s, while its plan bent left toward the next lane, and it hit actor 12 with its front at 5.7 s. A firmer brake was feasible and would likely have avoided the crash.
- car_conflicts_3knobs_2hz_llm_v2_r4_047: no_brake_for_lead, policy at fault: yes. The policy took over at 4.6 s while the ego was doing about 11 m/s and was 7.1 m from a slower SUV (actor 1) ahead in its lane, closing at about 7 m/s. It braked only lightly, to 9.7 m/s, and started planning a swerve left toward actor 36, then hit the SUV's rear at 5.1 s. A rear contact on the ego was also recorded, but the front collision started first.
- car_conflicts_3knobs_2hz_llm_v2_r4_048: no_brake_for_lead, policy at fault: unclear. On a straight multi-lane freeway, the ego was going about 11 m/s and closing on a much slower lead vehicle (actor 1) in its lane: the gap fell from 24 m to 5.3 m by the 4.6 s handoff. The policy then had only 0.5 s and braked from 11.1 to 9.6 m/s, which was not enough, and it hit actor 1 at 5.1 s; a rear contact was also flagged, but the front-collision flag points to the lead car as the main impact.
- car_conflicts_3knobs_2hz_llm_v2_r4_044_a2: no_brake_for_lead, policy at fault: unclear. On a straight multi-lane highway in slow traffic, the ego followed the same lane as the slowing lead car 12. It closed the gap from 6.8 m to 4.4 m and touched 12's rear with its front about 1 s after handoff, slowing only from 6.0 to 4.5 m/s. The ego was within 0.75 m of where the human was at that moment, so the logged gap was nearly the same. The policy had too little time to clearly avoid this, and the replayed lead car may be placed too close to the human's path.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_035, car_conflicts_3knobs_2hz_llm_v2_r4_043, car_conflicts_3knobs_2hz_llm_v2_r4_044_a2)
- S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_036, car_conflicts_3knobs_2hz_llm_v2_r4_041, car_conflicts_3knobs_2hz_llm_v2_r4_042)
- S3: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_015)
- S4: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_003)
- S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_025)
- S6: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_024)
- S7: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_004)
- S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_001)
- S9: 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_002, car_conflicts_3knobs_2hz_llm_v2_r4_011, car_conflicts_3knobs_2hz_llm_v2_r4_012)
- S10: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_047)
- S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_048)
- S12: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_039)
- S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_019)
- S14: 09a95ffa at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_030)
- S15: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_049)
- S16: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_040)
- S17: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_007)
- S18: 0dbb91dd at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_050)
- S19: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_008)
- S20: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_022, car_conflicts_3knobs_2hz_llm_v2_r4_031, car_conflicts_3knobs_2hz_llm_v2_r4_032)
- S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_020)
- S22: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_023)
- S23: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_021)
- S24: 12855a41 at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_038)
- S25: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_045)
- S26: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_010)
- S27: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_046)
- S28: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_037)
- S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_006)
- S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_026)
- S31: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_027)
- S32: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_016)
- S33: 187e6244 at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_028, car_conflicts_3knobs_2hz_llm_v2_r4_033, car_conflicts_3knobs_2hz_llm_v2_r4_034)
- S34: 187e6244 at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_009)
- S35: 187e6244 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_029)
- S36: 187e6244 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_017)
- S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_v2_r4_005, car_conflicts_3knobs_2hz_llm_v2_r4_013, car_conflicts_3knobs_2hz_llm_v2_r4_014)

## Not kept by the gate

- car_conflicts_3knobs_2hz_llm_v2_r4_018: not kept: RE-RUN
- car_conflicts_3knobs_2hz_llm_v2_r4_018_a2: not kept: HALT
- car_conflicts_3knobs_2hz_llm_v2_r4_044: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

0 of 52 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
