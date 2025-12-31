"""
White-box testing for US7 - Branch Coverage

Tests internal branches in filter_schools
"""

from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_choice_zero_branch():
    """Test choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should exit cleanly


def test_choice_one_location_branch():
    """Test choice == '1' (filter by location)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "London", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test" in line for line in outputs)


def test_location_zero_branch():
    """Test location == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should exit


def test_location_empty_branch():
    """Test not location"""
    SCHOOLS.clear()

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("cannot be empty" in line for line in outputs)


def test_no_filtered_location():
    """Test not filtered (location)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "Derby", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("No schools found" in line for line in outputs)


def test_choice_two_level_branch():
    """Test choice == '2' (filter by level)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["2", "1", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test" in line for line in outputs)


def test_level_zero_branch():
    """Test level_choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["2", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should exit


def test_level_not_in_map():
    """Test level_choice not in level_map"""
    SCHOOLS.clear()

    inputs_iter = iter(["2", "5", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid selection" in line for line in outputs)


def test_choice_three_rating_branch():
    """Test choice == '3' (filter by rating)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs_iter = iter(["3", "3", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Test" in line for line in outputs)


def test_rating_zero_branch():
    """Test min_rating_input == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "0"])
    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should exit


def test_rating_not_digit():
    """Test not min_rating_input.isdigit()"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "abc", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("must be a number" in line for line in outputs)


def test_rating_above_range():
    """Test min_rating > 5"""
    SCHOOLS.clear()

    inputs_iter = iter(["3", "6", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("between 1 and 5" in line for line in outputs)
