"""score_campaign.py on a hand-built queue."""

from enqueue import add
from faults import new_fault
from score_campaign import score


def test_lineages_are_scored_per_fault_kind(tmp_path, make_run):
    queue = tmp_path / "queue"
    clean = make_run("clean")
    clean["resolution"] = "ACCEPT"
    add(queue, clean)

    deleted = make_run("deleted", metrics=False)
    deleted["fault"] = new_fault("delete_metrics")
    deleted["resolution"] = "RE-RUN"
    deleted["diagnosis"] = {"skill": "RE-RUN"}
    first = add(queue, deleted)
    retry = make_run("deleted_a2", attempt=2)
    retry["parent"] = first.name
    retry["resolution"] = "ACCEPT"
    add(queue, retry)

    table = score(queue)
    assert table["clean"]["detected"] == 0
    assert table["clean"]["no_gate_invalid_kept"] == 0
    row = table["delete_metrics"]
    assert (row["detected"], row["recovered"], row["launches"]) == (1, 1, 2)
    assert row["skills"] == {"RE-RUN": 1}
    # Exit 0 with no metrics: a batch without the gate keeps it.
    assert (row["no_gate_kept"], row["no_gate_invalid_kept"]) == (1, 1)
    assert row["gate_invalid_kept"] == 0
