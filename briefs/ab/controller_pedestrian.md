# Linear or nonlinear MPC: which is safer when a pedestrian steps out early?

## Question
Is the nonlinear MPC safer than the linear one when pedestrians step out
early? The driving policy and everything else stay the same; only the
controller that steers and brakes along the policy's plan changes. Compare the
linear MPC (a) with the nonlinear MPC (b).

## Scope
Scenes tagged pedestrian_crossing with a pedestrian close to the ego's path.
Retime only that key pedestrian: step out up to 2 s earlier than recorded,
walking 1x to 2x their recorded speed. Replay the other traffic as recorded so
both controllers face the same scripted scenario. No delay or perception
error. Leave out scenes that already fail without any change: they cannot
show a difference between the controllers.

## Budget
About 50 runs, counting each controller's run separately.

## What counts
A front or side collision, or leaving the road. The answer is which
controller fails less over all the timings tried, or that the runs show no
difference.
