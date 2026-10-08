"""study_page.py: the chart draws every setting of the results table, with
its runs, and the page's knob values read in plain units."""

from html.parser import HTMLParser

from goals import rate_range
from study_page import chart_svg, knob_text

VARIED = ("planner_delay_us",)


def _table():
    """A results table as outer.results() makes it: three settings on two
    scenes, four kept runs."""
    settings = [
        ("S1", "clipgt-aaaaaaaa-1", 0, ["r1"], 0),
        ("S2", "clipgt-aaaaaaaa-1", 100_000, ["r2", "r3"], 1),
        ("S3", "clipgt-bbbbbbbb-2", 150_000, ["r4"], 1),
    ]
    return [
        {
            "id": setting,
            "scene_id": scene,
            "planner_delay_us": delay,
            "runs": len(runs),
            "failed": failed,
            "failure_rate_90": rate_range(failed, len(runs)),
            "possible_artifacts": 0,
            "run_names": runs,
        }
        for setting, scene, delay, runs, failed in settings
    ]


class _Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        self.found.append((tag, dict(attrs)))


def _tags(html: str) -> list[tuple[str, dict]]:
    parser = _Tags()
    parser.feed(html)
    return parser.found


def test_chart_has_one_range_bar_per_setting_and_one_square_per_run():
    table = _table()
    outcomes = {"r1": False, "r2": False, "r3": True, "r4": True}
    tags = _tags(chart_svg(table, VARIED, outcomes))
    classes = [attrs.get("class") for _, attrs in tags]
    assert classes.count("range") == len(table) == 3
    assert classes.count("rate") == 3
    assert classes.count("run fail") == 2
    assert classes.count("run pass") == 2
    assert [tag for tag, _ in tags].count("svg") == 2  # one panel per scene


def test_knob_values_read_in_plain_units():
    assert knob_text("planner_delay_us", 150_000) == "150 ms"
    assert knob_text("lateral_bias_m", -0.3) == "-0.3 m"


def test_an_ab_table_charts_each_controller_at_each_setting():
    from outer import results
    from study_page import system_rows

    rows = [
        {
            "run": f"r{i}_{controller}",
            "scene_id": "clipgt-aaaaaaaa-1",
            "planner_delay_us": delay,
            "controller": controller,
            "verdict": "kept",
            "failed": controller == "linear",
            "criticality": 1.0,
        }
        for i, delay in enumerate((0, 100_000))
        for controller in ("linear", "nonlinear")
    ]
    table = system_rows(results(rows, VARIED, {"a": "linear", "b": "nonlinear"}))
    assert [(r["id"], r["controller"]) for r in table] == [
        ("S1", "linear"),
        ("S1", "nonlinear"),
        ("S2", "linear"),
        ("S2", "nonlinear"),
    ]
    outcomes = {r["run"]: r["failed"] for r in rows}
    svg = chart_svg(table, (*VARIED, "controller"), outcomes)
    classes = [attrs.get("class") for _, attrs in _tags(svg)]
    assert classes.count("range") == 4
    assert knob_text("controller", "nonlinear") == "nonlinear"
