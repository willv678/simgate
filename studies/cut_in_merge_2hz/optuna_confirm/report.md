# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `optuna_confirm`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not find the 5 cases: no setting was confirmed with a failure rate surely above one half, which matches the goal verdict. Two settings came close. In 1c45ce3a, with cars 0.5 s earlier at recorded speed (S30), most runs failed and the range stops just short of the bar. In 09a95ffa, with cars 2 s later at 0.75x speed (S16), most runs failed but the range is wider. In nearly all of these failures the policy was not clearly at fault. The ego slowed for no visible reason or drifted about 2 m left, fell behind its recorded position, and a replayed car that cannot react came up from behind and hit its side or front corner. So these settings may show what non-reactive replay traffic does to a slow ego, more than a cut-in the policy failed to handle. No failures were flagged as possible rendering artifacts.

## Findings

- The strongest candidate is 1c45ce3a with cars shifted 0.5 s earlier at 1.0x speed. Most runs failed, but the 90% range still reaches just below one half, so it is not confirmed. In every failure the ego stayed in its lane but kept slowing with no close car ahead, ended up well behind its recorded position, and replayed car 24 came up on the right and sideswiped it or swept into its front-right corner. The policy's fault is unclear.
  - S30: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 4/5 failed, rate 44%-95% (90%) (cut_in_merge_2hz_optuna_confirm_015, cut_in_merge_2hz_optuna_confirm_020, cut_in_merge_2hz_optuna_confirm_029, cut_in_merge_2hz_optuna_confirm_038, cut_in_merge_2hz_optuna_confirm_046)
- The second candidate is 09a95ffa with cars shifted 2 s later at 0.75x speed. Most runs failed, but the range is too wide to clear the bar. In these failures the ego slowed and sat about 2 m left of the recorded path, often straddling the lane line. Replayed car 1 clipped its rear and then its right side; in one run the ego steered right, back into car 1. The policy's fault is unclear.
  - S16: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 0.75: 4/6 failed, rate 35%-88% (90%) (cut_in_merge_2hz_optuna_confirm_018, cut_in_merge_2hz_optuna_confirm_019, cut_in_merge_2hz_optuna_confirm_028, cut_in_merge_2hz_optuna_confirm_033, cut_in_merge_2hz_optuna_confirm_037, cut_in_merge_2hz_optuna_confirm_047)
- Other settings on these two scenes did not fail in the runs made: other timings and speeds in 09a95ffa, and earlier or faster or slower cars in 1c45ce3a. Most were run only once, so this is a hint and not evidence that they are safe.
  - S10: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_044)
  - S11: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_034)
  - S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_043)
  - S13: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_041)
  - S14: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_023)
  - S15: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_008)
  - S17: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_042)
  - S18: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_032)
  - S29: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_035)
  - S31: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_054)
  - S32: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_045)
  - S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_006)
- The only failure where triage found the policy at fault was in 096988dd, with cars 0.5 s earlier at 0.75x speed. The command was RIGHT, but the ego drifted left into the next lane at low speed and was sideswiped by a car coming up in that lane. This is one failure over a few runs, so it is a lead, not a rate.
  - S7: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.75: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_optuna_confirm_036, cut_in_merge_2hz_optuna_confirm_040, cut_in_merge_2hz_optuna_confirm_049)
- Two settings look unlikely to fail at all: 0e899dd3 with cars 1 s earlier at 1.5x speed, and 054b5901 at recorded timing with 1.5x speed. Neither failed in repeated runs, and their ranges stay below one half.
  - S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_017, cut_in_merge_2hz_optuna_confirm_021, cut_in_merge_2hz_optuna_confirm_030, cut_in_merge_2hz_optuna_confirm_039, cut_in_merge_2hz_optuna_confirm_048)
  - S4: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_optuna_confirm_005, cut_in_merge_2hz_optuna_confirm_010, cut_in_merge_2hz_optuna_confirm_022, cut_in_merge_2hz_optuna_confirm_031)
- Six scenes produced no failure at any setting tried: 023b7fcc, 054b5901, 0cf6368d, 0e899dd3, 12855a41 and 19f339ba. Most of their settings had only one or two runs, so this does not show the scenes are safe.
  - S1: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_002, cut_in_merge_2hz_optuna_confirm_013)
  - S2: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_027)
  - S3: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_053)
  - S4: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_optuna_confirm_005, cut_in_merge_2hz_optuna_confirm_010, cut_in_merge_2hz_optuna_confirm_022, cut_in_merge_2hz_optuna_confirm_031)
  - S5: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_050)
  - S19: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_016)
  - S20: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_004)
  - S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_017, cut_in_merge_2hz_optuna_confirm_021, cut_in_merge_2hz_optuna_confirm_030, cut_in_merge_2hz_optuna_confirm_039, cut_in_merge_2hz_optuna_confirm_048)
  - S22: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_051)
  - S23: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_001, cut_in_merge_2hz_optuna_confirm_011)
  - S24: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_026)
  - S25: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_014)
  - S26: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_009, cut_in_merge_2hz_optuna_confirm_012)
  - S27: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_007)
  - S28: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_024)

## Open

- Is S30 (1c45ce3a, -0.5 s, 1.0x) truly above one half? A few more repeats at this setting would settle it.
- Is S16 (09a95ffa, +2 s, 0.75x) truly above one half? Several more repeats are needed to narrow its range.
- Does S7 (096988dd, -0.5 s, 0.75x) fail reliably? It is the only setting with a failure where the policy was at fault, and it needs repeats.
- Are the failures the policy's? The near-cases come from non-reactive replayed cars hitting a slowed or drifted ego from behind or the side. Rerunning S30 and S16 with reactive traffic would show whether these are real policy failures or a side effect of replay.
- Why does the ego slow down with no close lead, and why does it drift left even when the command is RIGHT? The study cannot explain this. Comparing the logs with the 10 Hz study cut_in_merge at the same settings would show whether the 2 Hz planning rate causes it. This study has no data to compare the two rates.
- Do the four remaining confirmable scenes exist? Near-misses that were run only once were never repeated, for example S11 (09a95ffa, -0.5 s, 0.5x) and S3 (054b5901, -1.5 s, 1.0x). The scenes with no failure need more search before a case can be confirmed there.

## Why the runs failed (triage from the video and log)

actor_hit_ego 7, turned_into_actor 2

- cut_in_merge_2hz_optuna_confirm_018: actor_hit_ego, policy at fault: unclear. On a multi-lane freeway, the ego ended up about 2 m left of the recorded human path, mostly in the lane to the left, even though the command was RIGHT. It also slowed from 5.5 to 4.6 m/s. Actor 1, which replays its recorded path just behind and to the right, first touched the ego's rear and then ran into its right side at 9.6 s while the ego kept going straight in its own lane.
- cut_in_merge_2hz_optuna_confirm_019: actor_hit_ego, policy at fault: unclear. The ego slowed to about 4.5 m/s, fell 6–13 m behind its recorded position and drifted about 2 m left of the recorded path. Actor 1 drove up from behind along the recorded path and first rear-ended the ego (around 7.6 s). Actor 1 then pushed up along the ego's right side, and its overlap with the ego's front-right corner was scored as a front collision at 9.6 s. There was no lead vehicle within 13 m, so it was not a braking failure, but the ego's slow, drifting driving set up the conflict with the actor following the recording.
- cut_in_merge_2hz_optuna_confirm_020: actor_hit_ego, policy at fault: unclear. The ego was going straight down its freeway lane, right on the recorded path (0.1 m lateral offset), and slowing from 9.9 to 7.9 m/s even though the nearest car ahead was 42–55 m away and pulling further off. Actor 24 came up from behind in the right lane, drew level, and sideswiped the ego's side at 9.7 s; the ego didn't steer toward it, but it was about 20 m behind where the recorded car was at that moment, which is probably why the replayed actor ran into it.
- cut_in_merge_2hz_optuna_confirm_028: actor_hit_ego, policy at fault: unclear. The ego moved left of its recorded lane, straddling the line about 2.3 m off the logged path, and slowed to about 4.5 m/s. Actor 1, which replays the log, came up from behind in the recorded lane. It struck the ego's rear by 7.6 s and then side-swiped its right side at 9.6 s; nothing in front was close (gap to the lead was 12–20 m).
- cut_in_merge_2hz_optuna_confirm_029: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane, staying on the recorded path laterally (0.1 m off), but it slowed from 9.9 to 7.9 m/s with no close lead (gap 50 m or more), so it ended up about 20 m behind where the human car was. Actor 24, a log-replayed car coming up from behind in the right lane, then pulled alongside and sideswiped the ego, which counted as a lateral collision plus rear contact.
- cut_in_merge_2hz_optuna_confirm_038: actor_hit_ego, policy at fault: unclear. The ego stayed centered in its freeway lane on STRAIGHT but kept slowing from 9.5 to 7.5 m/s with no lead closer than about 46 m, so by 10.2 s it was 25 m behind where the human had been. Actor 24 came up on the ego's right and, following its recorded cut-in into the ego's lane, swept into the ego's front-right corner, which counted as a front collision; there was also rear contact.
- cut_in_merge_2hz_optuna_confirm_046: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane on a clear highway, staying within 0.4 m of the recorded path, but it kept slowing for no visible reason (10.3 to 8.3 m/s, nothing within 42 m ahead) and fell about 15 m behind where the human car was at that point. Replayed actor 24, coming up from behind in the lane to the right, then ran into the ego's right rear side, which was logged as a side collision with rear contact.
- cut_in_merge_2hz_optuna_confirm_047: turned_into_actor, policy at fault: unclear. After handoff, the ego slowed from 5.6 to 4.3 m/s and sat about 2 m left of the recorded path. Actor 1, which follows its recorded path and does not react, was close behind and clipped the ego's rear at about 7.6 s. At 9.6 s the ego steered right back toward its route and side-swiped actor 1, which was now alongside it on the right.
- cut_in_merge_2hz_optuna_confirm_049: turned_into_actor, policy at fault: yes. The command was RIGHT and the planned path pointed right, but after takeover the ego drifted left and ended up across the line into the left lane, moving slowly at about 3 m/s. Actor 41 was coming up from behind in that lane and sideswiped the ego's left side, which was recorded as a lateral at-fault collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_002, cut_in_merge_2hz_optuna_confirm_013)
- S2: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_027)
- S3: 054b5901 at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_053)
- S4: 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_optuna_confirm_005, cut_in_merge_2hz_optuna_confirm_010, cut_in_merge_2hz_optuna_confirm_022, cut_in_merge_2hz_optuna_confirm_031)
- S5: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_050)
- S6: 096988dd at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_025)
- S7: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.75: 1/3 failed, rate 8%-75% (90%) (cut_in_merge_2hz_optuna_confirm_036, cut_in_merge_2hz_optuna_confirm_040, cut_in_merge_2hz_optuna_confirm_049)
- S8: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_003)
- S9: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_052)
- S10: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_044)
- S11: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_034)
- S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_043)
- S13: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_041)
- S14: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_023)
- S15: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_008)
- S16: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 0.75: 4/6 failed, rate 35%-88% (90%) (cut_in_merge_2hz_optuna_confirm_018, cut_in_merge_2hz_optuna_confirm_019, cut_in_merge_2hz_optuna_confirm_028, cut_in_merge_2hz_optuna_confirm_033, cut_in_merge_2hz_optuna_confirm_037, cut_in_merge_2hz_optuna_confirm_047)
- S17: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_042)
- S18: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_032)
- S19: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_016)
- S20: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_004)
- S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/5 failed, rate 0%-35% (90%) (cut_in_merge_2hz_optuna_confirm_017, cut_in_merge_2hz_optuna_confirm_021, cut_in_merge_2hz_optuna_confirm_030, cut_in_merge_2hz_optuna_confirm_039, cut_in_merge_2hz_optuna_confirm_048)
- S22: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_051)
- S23: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_001, cut_in_merge_2hz_optuna_confirm_011)
- S24: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_026)
- S25: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_014)
- S26: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_optuna_confirm_009, cut_in_merge_2hz_optuna_confirm_012)
- S27: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_007)
- S28: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_024)
- S29: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_035)
- S30: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.0: 4/5 failed, rate 44%-95% (90%) (cut_in_merge_2hz_optuna_confirm_015, cut_in_merge_2hz_optuna_confirm_020, cut_in_merge_2hz_optuna_confirm_029, cut_in_merge_2hz_optuna_confirm_038, cut_in_merge_2hz_optuna_confirm_046)
- S31: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_054)
- S32: 1c45ce3a at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_045)
- S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_optuna_confirm_006)

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
