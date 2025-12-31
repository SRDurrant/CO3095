"""
Black-box testing for US9 - Sort Schools by Rating

Tests the sort schools functionality with various inputs
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


def test_sort_highest_to_lowest():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    outputs = run_sort_schools(["1", "", "0"])

    # High School should appear before Low School
    high_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    low_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    assert high_idx > low_idx


def test_sort_lowest_to_highest():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    outputs = run_sort_schools(["2", "", "0"])

    # Low School should appear before High School
    low_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    high_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    assert low_idx > high_idx


def test_schools_no_ratings():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("No ratings yet" in line for line in outputs)


def test_exit_immediately():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_sort_schools(["0"])

    assert any("Exiting Sort Schools" in line for line in outputs)


def test_invalid_option():
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    outputs = run_sort_schools(["5", "0"])

    assert any("Invalid option" in line for line in outputs)


def test_multiple_sorts():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "2", "value": 4})

    outputs = run_sort_schools(["1", "", "2", "", "0"])

    # Should contain both sort headers
    assert any("Highest to Lowest" in line for line in outputs)
    assert any("Lowest to Highest" in line for line in outputs)


def test_sort_with_mixed_ratings():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "2", "value": 5})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)


def test_sort_displays_full_info():
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    outputs = run_sort_schools(["1", "", "0"])

    assert any("ID: 1" in line for line in outputs)
    assert any("Test School" in line for line in outputs)
    assert any("Primary" in line for line in outputs)
    assert any("London" in line for line in outputs)
    assert any("4.00" in line for line in outputs)
