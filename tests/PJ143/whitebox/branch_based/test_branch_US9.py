"""
White-box testing for US9 - Branch Coverage

Tests internal branches in sort_schools_by_rating
"""

from app.school_actions import sort_schools_by_rating
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_choice_zero_branch():
    """Test choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should exit cleanly


def test_choice_one_branch():
    """Test choice == '1' (highest to lowest)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Highest to Lowest" in line for line in outputs)


def test_choice_two_branch():
    """Test choice == '2' (lowest to highest)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Lowest to Highest" in line for line in outputs)


def test_invalid_choice_branch():
    """Test else branch for invalid choice"""
    SCHOOLS.clear()

    inputs_iter = iter(["5", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid option" in line for line in outputs)


def test_avg_greater_than_zero():
    """Test avg > 0 branch"""
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

    assert any("4.00" in line for line in outputs)


def test_avg_equals_zero():
    """Test avg == 0 branch (no ratings)"""
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


def test_reverse_true_branch():
    """Test reverse=True for highest to lowest"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # High should appear before Low
    high_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    low_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    assert high_idx > low_idx


def test_reverse_false_branch():
    """Test reverse=False for lowest to highest"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # Low should appear before High
    low_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    high_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    assert low_idx < high_idx


def test_continue_after_display():
    """Test continue after displaying results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "0"])

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should loop back to menu


def test_multiple_iterations():
    """Test while loop continues"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "2", "", "0"])

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should handle multiple iterations
