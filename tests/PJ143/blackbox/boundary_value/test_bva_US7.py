"""
Black-box tests for US7 - Boundary Value Analysis

Tests boundary conditions for filter validation
"""

from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def run_filter_schools(inputs):
    """Captures ouptut of filter schools function by simulating user inputs"""
    inputs_iter = iter(inputs)
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )
    return outputs


def test_rating_exactly_1():
    """Minimum valid rating"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    outputs = run_filter_schools(["3", "1", "", "0"])

    assert any("Test School" in line for line in outputs)


def test_rating_exactly_5():
    """Maximum valid rating"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    outputs = run_filter_schools(["3", "5", "", "0"])

    assert any("Test School" in line for line in outputs)


def test_rating_6_invalid():
    """Just above maximum"""
    SCHOOLS.clear()

    outputs = run_filter_schools(["3", "6", "0"])

    assert any("between 1 and 5" in line for line in outputs)


def test_level_choice_1():
    """Minimum valid level"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["2", "1", "", "0"])

    assert any("Test" in line for line in outputs)


def test_level_choice_3():
    """Maximum valid level"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "combined", "location": "London"})

    outputs = run_filter_schools(["2", "3", "", "0"])

    assert any("Test School" in line for line in outputs)
