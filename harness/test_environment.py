"""environment.py: cleanup touches only containers from this checkout."""

from environment import ROOT, stale_container_ids


def _container(container_id: str, working_dir: str) -> dict:
    labels = f"com.docker.compose.project=p,com.docker.compose.project.working_dir={working_dir}"
    return {"ID": container_id, "Labels": labels}


def test_only_wizard_runs_under_this_checkout_are_stale():
    containers = [
        _container("ours", f"{ROOT}/diag/b2_001"),
        _container("other_project", "/home/someone/else"),
        {"ID": "no_compose", "Labels": ""},
    ]
    assert stale_container_ids(containers) == ["ours"]
