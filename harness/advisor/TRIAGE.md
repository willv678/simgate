# Failure triage: say what happened in one failed run

A simulated drive failed: the ego vehicle hit something with its front or side,
or left the road. You get the moments around the failure and say what
happened, as an AV engineer reviewing the clip would. Your label groups
failures across a study; a person reads your description.

## What you get

- Frames from the run's video, named by time in seconds (`frame_08.7s.png`),
  the last one at the moment of failure. Each frame has a top-down map (the
  ego is the green box, its planned path the green line, other actors grey
  boxes with ids, lanes in blue, stop lines red), the metrics table (its `Agg`
  column is the whole run's value, already final in every frame; `Per-Ts` is
  the value at that frame), and the
  front camera with the route command (LEFT, RIGHT, STRAIGHT). The camera
  image is rendered from a reconstruction of a real drive; close to other
  objects or far from where the real car drove it can smear or distort.
- On stdin, JSON: the failure (`collision_front`, `collision_lateral`,
  `offroad`), when it happened, how far the ego was from the recorded human
  trajectory then, and the ego's speed and the gap to the actor ahead over the
  last seconds.

## The answer

- `cause`: one of
  - `no_brake_for_lead`: drove into a vehicle ahead in its lane (stopped or
    slower) without braking enough;
  - `turned_into_actor`: hit an actor while turning or changing lanes;
  - `left_road`: drifted or steered off the drivable area;
  - `actor_hit_ego`: another actor drove into the ego, which could not avoid it;
  - `rendering`: the camera view was broken in a way that could explain the
    policy's mistake before the failure (smears or distortions at the moment
    of impact itself do not count);
  - `other`, with the reason in `what_happened`.
- `what_happened`: one or two sentences.
- `policy_at_fault`: `yes`, `no`, or `unclear`.
