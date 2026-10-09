"""A mirrored run: launched from the mirror checkout, checked from its log."""

from knobs import run_config
from read_state import MIRROR_CHECKOUT, MIRROR_MARKER, ROOT, mirror_not_applied
from run_experiment import launch_root, mirror_args, wizard_command

SCENE = "clipgt-0e002edd-c307-437c-9b97-6a1f6d28ac91"


def _entry(tmp_path, mirror: bool, logged: bool) -> dict:
    run = tmp_path / "run"
    run.mkdir()
    console = tmp_path / "run_console.log"
    console.write_text(f"starting\n{MIRROR_MARKER if logged else ''}\n")
    config = run_config(SCENE, {}, {}, "linear") | ({"mirror": True} if mirror else {})
    return {"run_dir": str(run), "config": config}


def test_a_mirrored_run_launches_from_the_mirror_checkout(tmp_path):
    config = run_config(SCENE, {}, {}, "linear") | {"mirror": True}
    assert launch_root(config) == MIRROR_CHECKOUT
    assert "+driver.model.mirror=true" in wizard_command(config, tmp_path / "run")
    plain = run_config(SCENE, {}, {}, "linear")
    assert launch_root(plain) == ROOT and mirror_args(plain) == []


def test_the_driver_must_log_the_mirror_when_asked(tmp_path):
    assert mirror_not_applied(_entry(tmp_path, mirror=True, logged=True)) is None
    (tmp_path / "b").mkdir()
    assert "did not log" in mirror_not_applied(
        _entry(tmp_path / "b", mirror=True, logged=False)
    )


def test_an_ordinary_run_must_not_be_mirrored(tmp_path):
    assert mirror_not_applied(_entry(tmp_path, mirror=False, logged=False)) is None
    (tmp_path / "b").mkdir()
    assert "requested False" in mirror_not_applied(
        _entry(tmp_path / "b", mirror=False, logged=True)
    )
