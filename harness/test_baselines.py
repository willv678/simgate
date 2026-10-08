"""baselines.py: the search proposers propose legal runs, LHS spreads them
evenly, and Optuna and the GA climb toward the critical settings."""

from collections import Counter

import pytest
from baselines import ga_proposals, lhs_proposals, optuna_proposals
from knobs import DELAYS_US, SCENARIO, rejection

SCENES = ["clipgt-a", "clipgt-b", "clipgt-c"]
DELAY = ("planner_delay_us",)
ALL = tuple(SCENARIO)


def _lhs(scenes, count, history, varied, seed):
    return lhs_proposals(scenes, count, len(history), varied, seed)


def _optuna(scenes, count, history, varied, seed):
    pytest.importorskip("optuna")
    return optuna_proposals(scenes, count, history, varied, seed)


PROPOSERS = [_lhs, _optuna, ga_proposals]


def _criticality(run):
    return run["planner_delay_us"] / DELAYS_US[-1]


def _kept(runs, start):
    """The proposed runs as kept history rows, scored by delay alone."""
    return [
        {
            "run": f"r{start + i}",
            **{k: v for k, v in run.items() if k != "why"},
            "verdict": "kept",
            "criticality": _criticality(run),
        }
        for i, run in enumerate(runs)
    ]


def _rounds(proposer, rounds, count, seed, varied=DELAY):
    """Proposals of each round, every run kept before the next round."""
    history, proposed = [], []
    for _ in range(rounds):
        runs = proposer(SCENES, count, history, varied, seed)["runs"]
        proposed.append(runs)
        history += _kept(runs, len(history))
    return proposed


def _mean_delay(runs):
    return sum(run["planner_delay_us"] for run in runs) / len(runs)


@pytest.mark.parametrize("proposer", PROPOSERS)
@pytest.mark.parametrize("varied", [DELAY, ALL])
def test_every_proposer_returns_exactly_count_legal_runs(proposer, varied):
    for runs in _rounds(proposer, 4, 7, 0, varied):
        assert len(runs) == 7
        assert all(rejection(run, set(SCENES), varied) is None for run in runs)


def test_lhs_covers_each_knob_and_the_scenes_evenly():
    runs = lhs_proposals(SCENES, 36, 0, ALL, 0)["runs"]
    for name, values in [("scene_id", SCENES)] + [(k, SCENARIO[k]) for k in ALL]:
        counts = Counter(run[name] for run in runs)
        assert set(counts) == set(values)
        # 36 runs over 3 to 9 values: every value equally often, up to one.
        assert max(counts.values()) - min(counts.values()) <= 1
    # Fewer runs than values: no two runs in the same stratum.
    few = lhs_proposals(SCENES, 5, 0, DELAY, 0)["runs"]
    assert len({run["planner_delay_us"] for run in few}) == 5


def test_lhs_is_set_by_the_seed_and_the_runs_already_proposed():
    assert lhs_proposals(SCENES, 8, 3, ALL, 1) == lhs_proposals(SCENES, 8, 3, ALL, 1)
    assert lhs_proposals(SCENES, 8, 3, ALL, 1) != lhs_proposals(SCENES, 8, 11, ALL, 1)


@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("proposer", [_optuna, ga_proposals])
def test_search_moves_toward_the_critical_delays(proposer, seed):
    # Uniform over the legal delays averages 200 ms.
    proposed = _rounds(proposer, 10, 8, seed)
    assert _mean_delay(proposed[0]) < 250_000
    assert _mean_delay([run for runs in proposed[5:] for run in runs]) > 275_000


@pytest.mark.parametrize("proposer", [_optuna, ga_proposals])
def test_search_is_deterministic_given_the_seed(proposer):
    assert _rounds(proposer, 3, 6, 4) == _rounds(proposer, 3, 6, 4)
    assert _rounds(proposer, 3, 6, 4) != _rounds(proposer, 3, 6, 5)


def test_only_kept_runs_breed():
    kept = _kept([{"scene_id": "clipgt-a", "planner_delay_us": 400_000}] * 2, 0)
    # A run the gate did not keep has no outcome, so no criticality.
    lost = [
        {
            "run": f"x{i}",
            "scene_id": "clipgt-a",
            "planner_delay_us": 0,
            "verdict": "not kept: REJECT",
        }
        for i in range(9)
    ]
    runs = ga_proposals(SCENES, 20, kept + lost, DELAY, 0)["runs"]
    # Mutation moves a delay by at most one step from 400 ms.
    assert all(run["planner_delay_us"] >= 350_000 for run in runs)
