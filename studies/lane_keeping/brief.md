# Lane keeping: perception error against ego speed

## Question
In scenes where the ego follows its lane without turning, which combinations
of a sideways error in the policy's plan (as from a perception or
localisation error) and the ego's speed when the policy takes over make it
leave its lane into another road user or off the road? Find the 5 most
challenging cases, each on a different scene, confirmed by repeats.

## Scope
Scenes whose recorded turn is none, with other traffic near the ego's path
(at least one vehicle alongside or ahead), so that leaving the lane can meet
someone. Vary the sideways shift of the plan (-0.5 m to +0.5 m, left
positive) and the ego's speed at hand-off (0.6x to 1.4x its recorded speed).
Replay the other traffic as recorded so the scenario is scripted, as in a
lane support test (Euro NCAP LSS: emergency lane keeping, road edge,
oncoming and overtaking vehicles), where the test vehicle's speed and its
lateral approach are the parameters. No delay and no waypoint noise.

## Budget
About 50 runs.

## What counts
A side or front collision, or leaving the road. Near misses rank next.
