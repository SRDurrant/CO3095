"""
White-box tests for US10 - Symbolic Execution

Targets specific path conditions in compare_two_schools
"""

from app.school_actions import compare_two_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_schools_empty():
    """Condition: not schools"""
    SCHOOLS.clear()

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_schools_less_than_two():
    """Condition: len(schools) < 2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_first_id_zero():
    """Condition: school_id_1_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_first_id_empty():
    """Condition: not school_id_1_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("cannot be empty" in line for line in outputs)


def test_symbolic_first_id_not_digit():
    """Condition: not school_id_1_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["abc", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("must be a number" in line for line in outputs)


def test_symbolic_first_id_not_exists():
    """Condition: school_exists == False (first ID)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["999", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("does not exist" in line for line in outputs)


def test_symbolic_second_id_zero():
    """Condition: school_id_2_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["1", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_second_id_equals_first():
    """Condition: school_id_2 == school_id_1"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["1", "1", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("select a different school" in line for line in outputs)


def test_symbolic_level_equal():
    """Condition: level_1 == level_2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "sss"})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Both schools are primary level" in line for line in outputs)


def test_symbolic_level_not_equal():
    """Condition: level_1 != level_2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("primary level" in line and "secondary level" in line for line in outputs)


def test_symbolic_location_equal():
    """Condition: location_1 == location_2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "London"})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Both schools are located in London" in line for line in outputs)


def test_symbolic_avg_both_greater_than_zero():
    """Condition: avg_1 > 0 and avg_2 > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "2", "value": 3})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("4.00" in line for line in outputs)


def test_symbolic_avg_1_greater():
    """Condition: avg_1 > avg_2"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 5})
    RATINGS.append({"school_id": "2", "value": 3})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("higher rating" in line for line in outputs)


def test_symbolic_avg_2_greater():
    """Condition: avg_2 > avg_1"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 2})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("higher rating" in line for line in outputs)


def test_symbolic_avg_equal():
    """Condition: avg_1 == avg_2"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "2", "value": 4})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("same rating" in line for line in outputs)


def test_symbolic_only_avg_1():
    """Condition: avg_1 > 0 and avg_2 <= 0"""
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


def test_symbolic_choice_zero():
    """Condition: choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_symbolic_choice_one():
    """Condition: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "1", "1", "2", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
