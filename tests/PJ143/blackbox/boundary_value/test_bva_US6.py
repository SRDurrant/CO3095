"""
Boundary Value Analysis for US6 - List All Schools

Testing boundary conditions
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_exactly_one_school():
    """Boundary: minimum number of schools (1)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Only School", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Only School" in s for s in outputs)


def test_zero_schools():
    """Boundary: no schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_choice_0_exits():
    """Boundary: choice 0 returns to main menu"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_1_valid():
    """Boundary: choice 1 is valid"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # choice 1 calls view_school_profile, which will exit with 0
    inputs = iter(["1", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_3_valid():
    """Boundary: choice 3 is maximum valid"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # choice 3 calls sort_schools_by_rating
    inputs = iter(["3", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_choice_4_invalid():
    """Boundary: choice 4 is above maximum"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["4", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_rating_exactly_1():
    """Boundary: minimum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 1})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("1.00" in s for s in outputs)


def test_rating_exactly_5():
    """Boundary: maximum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("5.00" in s for s in outputs)


def test_many_schools():
    """Boundary: many schools in list"""
    SCHOOLS.clear()
    for i in range(10):
        SCHOOLS.append({"school_id": i + 1, "name": f"School{i + 1}", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("School1" in s for s in outputs)
    assert any("School10" in s for s in outputs)
