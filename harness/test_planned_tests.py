import pytest

from planned_tests import holm, permutation_p


def test_complete_separation_of_five_against_five_gives_the_smallest_p():
    assert permutation_p([5, 5, 5, 5, 4], [1, 2, 1, 2, 1]) == 2 / 252


def test_identical_groups_give_p_one():
    assert permutation_p([3, 3, 3], [3, 3, 3]) == 1.0


def test_holm_multiplies_by_rank_and_stays_monotone():
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
