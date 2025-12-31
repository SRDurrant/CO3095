"""
White-box tests for US7 - Symbolic Execution

Targets specific path conditions in filter_schools
"""

from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_choice_zero():
    """Condition: choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_choice_one():
    """Condition: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "London", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test" in line for line in outputs)


def test_symbolic_location_zero():
    """Condition: location == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_location_empty():
    """Condition: not location"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("cannot be empty" in line for line in outputs)


def test_symbolic_filtered_empty():
    """Condition: not filtered (location)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "Burton", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("No schools found" in line for line in outputs)


def test_symbolic_choice_two():
    """Condition: choice == '2'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["2", "1", "", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_level_zero():
    """Condition: level_choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["2", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_level_not_in_map():
    """Condition: level_choice not in level_map"""
    SCHOOLS.clear()

    inputs_iter = iter(["2", "5", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid selection" in line for line in outputs)


def test_symbolic_choice_three():
    """Condition: choice == '3'"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs_iter = iter(["3", "3", "", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_rating_zero():
    """Condition: min_rating_input == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_rating_not_digit():
    """Condition: not min_rating_input.isdigit()"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "abc", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("must be a number" in line for line in outputs)


def test_symbolic_rating_greater_than_five():
    """Condition: min_rating > 5"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "6", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("between 1 and 5" in line for line in outputs)
