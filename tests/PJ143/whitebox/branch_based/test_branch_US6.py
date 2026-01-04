"""
Branch coverage tests for US6 - List All Schools

Testing all execution branches
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_schools_empty_branch():
    """Branch: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_schools_not_empty_branch():
    """Branch: schools exist"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Schools" in s for s in outputs)


def test_choice_equals_zero():
    """Branch: choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_equals_one():
    """Branch: choice == '1' calls view_school_profile"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_equals_two():
    """Branch: choice == '2' calls filter_schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["2", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_equals_three():
    """Branch: choice == '3' calls sort_schools_by_rating"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["3", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_invalid_branch():
    """Branch: else (invalid choice)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["9", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_avg_greater_than_zero():
    """Branch: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("4.00" in s for s in outputs)


def test_avg_equals_zero():
    """Branch: avg <= 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_for_loop_iteration():
    """Branch: for school in schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("SchoolA" in s for s in outputs)
    assert any("SchoolB" in s for s in outputs)


def test_while_loop_continues():
    """Branch: while True continues after invalid choice"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["5", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_strip_method():
    """Branch: choice.strip()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # input with spaces
    inputs = iter(["  0  "])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_get_with_default():
    """Branch: school.get() with default"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1})  # missing name

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("?" in s for s in outputs)


def test_averages_dict_get():
    """Branch: averages.get() returns 0.0 default"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    # school has no rating, should show "No ratings yet"
    assert any("No ratings yet" in s for s in outputs)
