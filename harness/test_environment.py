"""environment.py: cleanup touches only containers from this checkout."""

from environment import ROOT, in_flight_runs, stale_container_ids


def _container(container_id: str, working_dir: str) -> dict:
    labels = f"com.docker.compose.project=p,com.docker.compose.project.working_dir={working_dir}"
    return {"ID": container_id, "Labels": labels}


def test_only_ended_runs_under_this_checkout_are_stale(tmp_path, monkeypatch):
    import environment

    monkeypatch.setattr(environment, "ROOT", tmp_path)
    (tmp_path / "diag").mkdir()
    (tmp_path / "diag" / "ended_exit_code").write_text("0\n")
    containers = [
        _container("ended", f"{tmp_path}/diag/ended"),
        _container("running", f"{tmp_path}/diag/running"),
        _container("other_project", "/home/someone/else"),
        {"ID": "no_compose", "Labels": ""},
    ]
    assert stale_container_ids(containers) == ["ended"]
    assert in_flight_runs(containers) == [tmp_path / "diag" / "running"]


def test_the_checkout_root_is_the_repository():
    assert (ROOT / "research").is_dir()
