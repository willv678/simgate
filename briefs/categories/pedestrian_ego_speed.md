# Pedestrian crossing: ego speed against pedestrian timing

## Question
In scenes where a pedestrian crosses or walks near the ego's path, which
combinations of the ego's speed when the driving policy takes over and the
pedestrian's step-out time make the policy hit the pedestrian or leave the
road? Find the 5 most challenging cases, each on a different scene, confirmed
by repeats.

## Scope
Scenes tagged pedestrian_crossing. Vary the ego's speed at hand-off (0.6x to
1.4x its recorded speed) and retime the recorded pedestrians (class person):
step out up to 2 s earlier or later, at their recorded walking speed. Replay
the other traffic as recorded so the scenario is scripted, as in Euro NCAP
pedestrian tests, where the test vehicle's speed and the pedestrian's timing
are the two parameters. No delay or perception error.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.
