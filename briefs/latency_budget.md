# Latency budget

## Question
At what planner delay does the policy start failing? I need a rough latency
budget per scene for deciding how much onboard compute time the planner gets.

## Scope
Delay only, no perception error. Pick scenes where a delay effect can show:
ones that drive cleanly with no delay. A mix of slow and faster scenes if
there are any.

## Budget
About 30 runs, overnight.

## What counts
A crash with the front or side, or leaving the road.
