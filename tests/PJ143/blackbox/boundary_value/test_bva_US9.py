"""
Black-box tests for US9 - Boundary Value Analysis

Tests boundary conditions for sort validation
"""

from app.school_actions import sort_schools_by_rating
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def run_sort_schools(inputs):
    inputs_iter = iter(inputs)
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )
    return outputs


def test_choice_1_valid():
    """Minimum valid choice"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("Highest to Lowest" in line for line in outputs)


def test_choice_2_valid():
    """Maximum valid choice"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_sort_schools(["2", "", "0"])

    assert any("Lowest to Highest" in line for line in outputs)


def test_choice_0_exit():
    """Exit choice boundary"""
    SCHOOLS.clear()

    outputs = run_sort_schools(["0"])

    assert any("Exiting Sort Schools" in line for line in outputs)


def test_choice_3_invalid():
    """Just above maximum valid"""
    SCHOOLS.clear()

    outputs = run_sort_schools(["3", "0"])

    assert any("Invalid option" in line for line in outputs)


def test_rating_exactly_1():
    """Minimum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 1})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("1.00" in line for line in outputs)


def test_rating_exactly_5():
    """Maximum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("5.00" in line for line in outputs)
