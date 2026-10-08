# Aborted 7 Oct: a gate bug, not the policy

These arms ran with a postflight bug: a retimed actor's track id was passed to
Hydra unquoted, resolved as a number (123) while the run asked for a string
('123'), so the "requested settings landed" check failed every retimed run and
the Investigator halted it (rules: 17 of 26). The runtime logs show the
retiming was applied. Fixed in run_experiment.traffic_args (quoted) and
read_state.config_not_landed (compared as strings); the study was restarted
from scratch so the proposers' choices are not shaped by wrongly rejected
evidence. Run directories are in diag/aborted_pedestrian_7oct/.
