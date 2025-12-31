"""
Black-box tests for US10 - Boundary Value Analysis

Tests boundary conditions for compare schools validation
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


def test_exactly_two_schools():
    """Minimum required schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)


def test_exactly_one_school():
    """Just below minimum"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})

    outputs = run_compare_schools([""])

    assert any("At least two schools are required" in line for line in outputs)


def test_id_1_valid():
    """Minimum valid ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("School A" in line for line in outputs)


def test_rating_diff_0():
    """Equal ratings boundary"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "2", "value": 3})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("same rating" in line for line in outputs)


def test_rating_diff_small():
    """Small rating difference"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "2", "value": 4})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("1.00 points" in line for line in outputs)


def test_rating_diff_maximum():
    """Maximum rating difference (1 vs 5)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 1})
    RATINGS.append({"school_id": "2", "value": 5})

    outputs = run_compare_schools(["1", "2", "0"])

    assert any("4.00 points" in line for line in outputs)


def test_choice_0_exit():
    """Exit choice boundary"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "B", "level": "primary", "location": "Manchester"})

    outputs = run_compare_schools(["0"])

    assert any("Exiting School Comparison" in line for line in outputs)


def test_choice_1_continue():
    """Continue choice boundary"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "B", "level": "primary", "location": "Manchester"})

    outputs = run_compare_schools(["1", "2", "1", "1", "2", "0"])

    # Should have two comparisons
    comparison_count = sum(1 for line in outputs if "Comparison Summary" in line)
    assert comparison_count == 2
