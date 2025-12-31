"""
Black-box testing for US7 - Filter Schools by Attributes

Tests the filter schools flow with various inputs
"""

from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def run_filter_schools(inputs):
    inputs_iter = iter(inputs)
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )
    return outputs


def test_filter_by_location():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})

    outputs = run_filter_schools(["1", "London", "", "0"])

    assert any("School A" in line for line in outputs)
    assert not any("School B" in line for line in outputs)


def test_filter_by_level_primary():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Manchester"})

    outputs = run_filter_schools(["2", "1", "", "0"])

    assert any("School A" in line for line in outputs)
    assert not any("School B" in line for line in outputs)


def test_filter_by_rating():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 5})
    RATINGS.append({"school_id": "2", "value": 2})

    outputs = run_filter_schools(["3", "4", "", "0"])

    assert any("School A" in line for line in outputs)
    assert not any("School B" in line for line in outputs)


def test_empty_location():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["1", "", "0"])

    assert any("cannot be empty" in line for line in outputs)


def test_no_schools_in_location():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["1", "Paris", "0"])

    assert any("No schools found" in line for line in outputs)


def test_invalid_level():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["2", "5", "0"])

    assert any("Invalid selection" in line for line in outputs)


def test_invalid_rating():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["3", "abc", "0"])

    assert any("must be a number" in line for line in outputs)


def test_rating_out_of_range():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["3", "6", "0"])

    assert any("between 1 and 5" in line for line in outputs)


def test_exit_immediately():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_filter_schools(["0"])

    assert any("Exiting Filtering" in line for line in outputs)
