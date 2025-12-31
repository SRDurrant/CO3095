"""
White-box tests for US9 - Concolic Testing

Uses concrete executions to drive different paths
"""

from app.school_actions import sort_schools_by_rating
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_concolic_exit_immediately():
    """Path: exit at main menu"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_sort_high_to_low():
    """Path: choose highest to lowest -> view -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Highest to Lowest" in line for line in outputs)


def test_concolic_sort_low_to_high():
    """Path: choose lowest to highest -> view -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Lowest to Highest" in line for line in outputs)


def test_concolic_invalid_then_exit():
    """Path: invalid choice -> retry -> exit"""
    SCHOOLS.clear()

    inputs_iter = iter(["5", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid option" in line for line in outputs)


def test_concolic_both_sorts():
    """Path: sort high to low -> sort low to high -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "", "2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Highest to Lowest" in line for line in outputs)
    assert any("Lowest to Highest" in line for line in outputs)


def test_concolic_no_ratings():
    """Path: sort schools with no ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("No ratings yet" in line for line in outputs)


def test_concolic_mixed_ratings():
    """Path: sort schools with some rated, some unrated"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)
