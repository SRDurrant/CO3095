"""
White-box tests for US9 - Symbolic Execution

Targets specific path conditions in sort_schools_by_rating
"""

from app.school_actions import sort_schools_by_rating
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_choice_zero():
    """Condition: choice == '0'"""
    SCHOOLS.clear()

    inputs_iter = iter(["0"])
    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_choice_one():
    """Condition: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Highest to Lowest" in line for line in outputs)


def test_symbolic_choice_two():
    """Condition: choice == '2'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Lowest to Highest" in line for line in outputs)


def test_symbolic_choice_else():
    """Condition: choice not in ['0', '1', '2']"""
    SCHOOLS.clear()

    inputs_iter = iter(["99", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Invalid option" in line for line in outputs)


def test_symbolic_avg_greater_than_zero():
    """Condition: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("3.00" in line for line in outputs)


def test_symbolic_avg_not_greater_than_zero():
    """Condition: avg <= 0 (no ratings)"""
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


def test_symbolic_reverse_true():
    """Condition: reverse=True (highest to lowest)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 1})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    high_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    low_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    assert high_idx < low_idx


def test_symbolic_reverse_false():
    """Condition: reverse=False (lowest to highest)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 1})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    low_idx = next(i for i, line in enumerate(outputs) if "School A" in line)
    high_idx = next(i for i, line in enumerate(outputs) if "School B" in line)
    assert low_idx < high_idx


def test_symbolic_lambda_key_function():
    """Condition: lambda s: averages.get(str(s.get('school_id')), 0.0)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Derby"})
    SCHOOLS.append({"school_id": 3, "name": "School C", "level": "primary", "location": "Burton"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "2", "value": 5})
    RATINGS.append({"school_id": "3", "value": 1})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # B (5.00) should be first, then A (3.00), then C (1.00)
    b_idx = next(i for i, line in enumerate(outputs) if " School B " in line)
    a_idx = next(i for i, line in enumerate(outputs) if " School A " in line)
    c_idx = next(i for i, line in enumerate(outputs) if " School C " in line)
    assert b_idx < a_idx < c_idx


def test_symbolic_continue_branch():
    """Condition: continue statement after displaying results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "0"])

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should loop back to menu after continue


def test_symbolic_while_loop_iteration():
    """Condition: while True continues until choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs_iter = iter(["1", "", "2", "", "1", "", "0"])

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    # Should iterate multiple times before exiting
