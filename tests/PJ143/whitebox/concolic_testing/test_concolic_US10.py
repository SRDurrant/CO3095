"""
White-box tests for US10 - Concolic Testing

Uses concrete executions to drive different paths
"""

from app.school_actions import compare_two_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_concolic_no_schools():
    """Path: no schools -> exit"""
    SCHOOLS.clear()

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_one_school():
    """Path: only one school -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_exit_at_first_id():
    """Path: exit at first ID prompt"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_exit_at_second_id():
    """Path: valid first ID -> exit at second ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_concolic_compare_success():
    """Path: compare two schools -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Comparison Summary" in line for line in outputs)


def test_concolic_invalid_first_id():
    """Path: invalid first ID -> retry -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["999", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("does not exist" in line for line in outputs)


def test_concolic_same_school_twice():
    """Path: same school selected -> retry -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leds"})

    inputs_iter = iter(["1", "1", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("select a different school" in line for line in outputs)


def test_concolic_multiple_comparisons():
    """Path: compare -> continue -> compare -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})
    SCHOOLS.append({"school_id": 3, "name": "School C", "level": "combined", "location": "Dudley"})

    inputs_iter = iter(["1", "2", "1", "2", "3", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    comparison_count = sum(1 for line in outputs if "Comparison Summary" in line)
    assert comparison_count == 2


def test_concolic_both_no_ratings():
    """Path: compare schools with no ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Lees"})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Neither school has ratings yet" in line for line in outputs)


def test_concolic_one_has_rating():
    """Path: one school has rating, other doesn't"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("no ratings yet" in line for line in outputs)
