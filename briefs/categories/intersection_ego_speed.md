# Intersection: ego speed against the crossing car's timing

## Question
In scenes where the ego crosses or turns at an intersection with crossing
traffic, which combinations of the ego's speed when the driving policy takes
over and the crossing car's arrival time make the policy collide or leave the
road? Find the 5 most challenging cases, each on a different scene, confirmed
by repeats.

## Scope
Scenes tagged intersection with a recorded crossing vehicle. Vary the ego's
speed at hand-off (0.6x to 1.4x its recorded speed) and retime the crossing
car (class automobile): arrive up to 2 s earlier or later, at its recorded
speed. Replay the other traffic as recorded, as in Euro NCAP crossing tests,
where the test vehicle's speed and the target's timing are the parameters.
No delay or perception error.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.
