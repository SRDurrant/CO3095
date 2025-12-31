"""
White-box tests for US7 - Concolic Testing

Uses concrete executions to drive different paths
"""

from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_concolic_exit_immediately():
    """Path: exit at main menu"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_filter_location_success():
    """Path: filter by location -> show results -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "London", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test School" in line for line in outputs)


def test_concolic_filter_location_exit():
    """Path: choose location filter -> exit at location prompt"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_filter_level_success():
    """Path: filter by level -> show results -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["2", "1", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test School" in line for line in outputs)


def test_concolic_filter_rating_success():
    """Path: filter by rating -> show results -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs_iter = iter(["3", "4", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test School" in line for line in outputs)


def test_concolic_empty_location_retry():
    """Path: empty location -> retry -> exit"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("cannot be empty" in line for line in outputs)


def test_concolic_invalid_level_retry():
    """Path: invalid level -> retry -> exit"""
    SCHOOLS.clear()

    inputs_iter = iter(["2", "5", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid selection" in line for line in outputs)


def test_concolic_invalid_rating_retry():
    """Path: invalid rating -> retry -> exit"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "abc", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("must be a number" in line for line in outputs)
