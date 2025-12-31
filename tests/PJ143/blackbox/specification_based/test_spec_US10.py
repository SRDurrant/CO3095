"""
Black-box testing for US10 - Compare Two Schools

Tests the compare two schools functionality with various inputs
"""

from app.school_actions import compare_two_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def run_compare_schools(inputs):
    inputs_iter = iter(inputs)
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )
    return outputs


def test_compare_two_schools_success():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "2", "value": 5})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)
    assert any("Comparison Summary" in line for line in outputs)


def test_compare_same_level():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("Both schools are primary level" in line for line in outputs)


def test_compare_different_levels():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("primary level" in line and "secondary level" in line for line in outputs)


def test_compare_same_location():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "London"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("Both schools are located in London" in line for line in outputs)


def test_compare_different_locations():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("London" in line and "Leeds" in line for line in outputs)


def test_compare_higher_rating():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 5})
    RATINGS.append({"school_id": "2", "value": 3})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("higher rating" in line for line in outputs)


def test_compare_no_ratings():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("Neither school has ratings yet" in line for line in outputs)


def test_no_schools():
    SCHOOLS.clear()

    outputs = run_compare_schools([""])

    assert any("No schools found" in line for line in outputs)


def test_only_one_school():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})

    outputs = run_compare_schools([""])

    assert any("At least two schools are required" in line for line in outputs)


def test_invalid_first_id():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["999", "0"])

    assert any("does not exist" in line for line in outputs)


def test_same_school_twice():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "1", "0"])

    assert any("select a different school" in line for line in outputs)


def test_exit_at_first_id():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["0"])

    assert any("Exiting School Comparison" in line for line in outputs)


def test_exit_at_second_id():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    outputs = run_compare_schools(["1", "0"])

    assert any("Exiting School Comparison" in line for line in outputs)


def test_multiple_comparisons():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})
    SCHOOLS.append({"school_id": 3, "name": "School C", "level": "combined", "location": "Burton"})

    outputs = run_compare_schools(["1", "2", "1", "2", "3", "0"])

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)
    assert any("School C" in line for line in outputs)
