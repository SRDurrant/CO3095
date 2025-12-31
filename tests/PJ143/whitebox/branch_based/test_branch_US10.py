"""
White-box testing for US10 - Branch Coverage

Tests internal branches in compare_two_schools
"""

from app.school_actions import compare_two_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_schools_empty_branch():
    """Test not schools"""
    SCHOOLS.clear()

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_schools_less_than_two_branch():
    """Test len(schools) < 2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})

    inputs_iter = iter([""])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_first_id_zero_branch():
    """Test school_id_1_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_first_id_empty_branch():
    """Test not school_id_1_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("cannot be empty" in line for line in outputs)


def test_first_id_not_digit_branch():
    """Test not school_id_1_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["abc", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("must be a number" in line for line in outputs)


def test_first_id_not_exists_branch():
    """Test school_exists == False for first ID"""
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


def test_second_id_zero_branch():
    """Test school_id_2_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_second_id_same_as_first_branch():
    """Test school_id_2 == school_id_1"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "1", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("select a different school" in line for line in outputs)


def test_avg_greater_than_zero_both():
    """Test avg_1 > 0 and avg_2 > 0"""
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


def test_avg_1_greater_than_avg_2():
    """Test avg_1 > avg_2"""
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


def test_avg_2_greater_than_avg_1():
    """Test avg_2 > avg_1"""
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


def test_avg_equal():
    """Test avg_1 == avg_2"""
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


def test_only_avg_1_has_rating():
    """Test avg_1 > 0 and avg_2 == 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "B", "level": "primary", "location": "Leeds"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("no ratings yet" in line for line in outputs)


def test_choice_zero_exit():
    """Test choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_choice_one_continue():
    """Test choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "1", "1", "2", "0"])
    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )


def test_level_equal_branch():
    """Test level_1 == level_2"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Both schools are primary level" in line for line in outputs)


def test_location_equal_branch():
    """Test location_1 == location_2"""
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
