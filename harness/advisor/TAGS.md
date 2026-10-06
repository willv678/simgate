# Scene tagging: say what kind of driving scenario a scene is

A study of a driving policy groups recorded scenes into stress-test
categories. You look at three moments of one scene and say what the scene
holds, as an AV engineer sorting clips would. Rules computed from the
recorded tracks tag the same scenes independently; a person checks a sample
of both.

## What you get

Three frames from the scene's video, named by time in seconds
(`frame_00.5s.png`, the middle, and near the end of a 12 s clip). Each frame
has a top-down map (the ego is the green box, its planned path the green
line, other actors grey boxes with ids and pink lines for their motion,
lanes in blue, stop lines red), a metrics table (ignore it), and the front
camera with the route command (LEFT, RIGHT, STRAIGHT) in its corner. The
camera image is rendered from a reconstruction of a real drive. The ego in
the video is driven by a policy and can stray from the recorded drive; tag
the scene, its road, its traffic and the route the command asks for, not
how well the policy drove.

## The answer

- `road_type`: `urban` (city streets, dense buildings), `suburban` (houses,
  low-rise, wider streets), `highway` (divided, multi-lane, ramps), or
  `parking` (a parking lot or garage).
- `intersection_present`, `crosswalk_visible`, `pedestrians_visible`,
  `traffic_lights_visible`: true if any frame shows one.
- `ego_maneuver`: what the ego is asked to do over the clip: `straight`
  (follows its lane, curves included), `left_turn`, `right_turn`,
  `lane_change`, or `merge` (joins traffic from a ramp or a lane that ends).
- `categories`: every category that applies, each with a one-line `reason`
  naming what you saw (actor ids from the map help); none if none applies.
  - `lead_vehicle`: a vehicle ahead in the ego's lane that the ego follows,
    and that slows or stops (or is stopped ahead in the lane).
  - `unprotected_left`: the ego turns left across the path of oncoming
    traffic without a protected arrow.
  - `merge_cut_in`: the ego changes lanes or merges, or another vehicle
    moves into the ego's lane close ahead of it.
  - `intersection`: the ego crosses or turns at an intersection, or traffic
    crosses its path.
  - `pedestrian_crossing`: pedestrians cross, or are on the road close to,
    the ego's path (on a crosswalk or not); people on a sidewalk away from
    the road do not count.

Tag only what the frames show; if a frame is too broken to read, rely on the
others.
