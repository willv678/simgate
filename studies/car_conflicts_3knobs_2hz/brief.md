# Car conflicts, three knobs at once (2 Hz planning)

## Question
In scenes where another car cuts in ahead of the ego or slows ahead of it,
which combinations of that car's timing, that car's speed and the ego's own
speed when the policy takes over make the policy collide or leave the road?
Find the 5 most challenging cases, each on a different scene, confirmed by
repeats.

## Scope
Scenes tagged merge_cut_in or lead_vehicle that pass as recorded (no failure
at the recorded setting), so that failures are rare and have to be found.
Retime the recorded cars (class automobile): up to 2 s earlier or later,
0.5x to 2x speed; and vary the ego's speed at hand-off (0.6x to 1.4x its
recorded speed). Replay traffic as recorded.

## Budget
About 60 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.

## Planning rate
The policy plans every 500 ms (2 Hz, VaVAM's own rhythm). At 2 Hz it fails
less than at 10 Hz (HZ.md), which is the point here: this study tests the
search methods where failures are rare and the space is large (three knobs
instead of two).
