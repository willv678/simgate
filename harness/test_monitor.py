"""monitor.py: a run counts as stalled only while its simulation is running."""

import os

from monitor import stalled_for


def _log(tmp_path, rollout: str, mtime: float):
    folder = tmp_path / "rollouts" / "scene" / rollout
    folder.mkdir(parents=True)
    log = folder / "rollout.asl"
    log.write_bytes(b"x")
    os.utime(log, (mtime, mtime))
    return folder


def test_no_log_yet_is_not_a_stall(tmp_path):
    assert stalled_for(tmp_path, now=1000.0) == 0.0


def test_a_log_that_stopped_growing_mid_simulation_is_a_stall(tmp_path):
    _log(tmp_path, "a", mtime=800.0)
    assert stalled_for(tmp_path, now=1000.0) == 200.0


def test_a_scored_rollout_is_not_a_stall(tmp_path):
    (_log(tmp_path, "a", mtime=800.0) / "metrics.parquet").write_bytes(b"")
    assert stalled_for(tmp_path, now=1000.0) == 0.0


def test_the_newest_rollout_decides_after_a_retry(tmp_path):
    (_log(tmp_path, "crashed", mtime=500.0) / "metrics.parquet").write_bytes(b"")
    _log(tmp_path, "retry", mtime=950.0)
    assert stalled_for(tmp_path, now=1000.0) == 50.0
