"""healing_ledger: a run's retries, how it ended, and whether a retry kept its settings."""

from pathlib import Path

from healing_ledger import ending, lineages, same_settings


def _entry(name, attempt=1, parent=None, resolution="ACCEPT", skill=None, params=None, **config):
    diagnosis = {"skill": skill, "params": params or {}} if skill else None
    return {"name": name, "attempt": attempt, "parent": parent, "resolution": resolution,
            "diagnosis": diagnosis, "config": {"ego_speed_scale": 1.0, **config}}


def test_a_healed_run_is_one_lineage_that_ends_kept():
    queue = Path("q")
    entries = [
        (queue / "001_a.json", _entry("a", resolution="RE-RUN", skill="RE-RUN")),
        (queue / "002_b.json", _entry("b")),
        (queue / "003_a_a2.json", _entry("a_a2", attempt=2, parent="001_a.json")),
    ]
    chains = lineages(entries)
    assert [[p.name for p, _ in c] for c in chains] == [["001_a.json", "003_a_a2.json"], ["002_b.json"]]
    assert ending(chains[0]) == "kept"
    assert same_settings(chains[0])


def test_a_retry_that_changed_the_experiment_is_caught():
    queue = Path("q")
    chain = [(queue / "001_a.json", _entry("a", resolution="RE-RUN", skill="RE-RUN")),
             (queue / "002_a_a2.json", _entry("a_a2", attempt=2, parent="001_a.json", ego_speed_scale=1.4))]
    assert not same_settings(chain)


def test_configure_may_change_only_the_knob_it_names():
    queue = Path("q")
    parent = _entry("a", resolution="CONFIGURE", skill="CONFIGURE", params={"trafficsim_device": "cpu"})
    child = _entry("a_a2", attempt=2, parent="001_a.json", trafficsim_device="cpu")
    assert same_settings([(queue / "001_a.json", parent), (queue / "002_a_a2.json", child)])


def test_a_stopped_run_ends_stopped():
    queue = Path("q")
    assert ending([(queue / "001_a.json", _entry("a", resolution="HALT", skill="HALT"))]) == "stopped"
