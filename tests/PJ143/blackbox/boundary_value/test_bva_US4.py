"""
Boundary Value Analysis for US4 - Delete School

Testing boundary conditions for deletion
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def test_delete_school_id_1():
    """Boundary: minimum typical school ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_exactly_one_school():
    """Boundary: minimum number of schools (1)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 5, "name": "OneSchool", "level": "primary", "location": "London"})

    inputs = iter(["5", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_zero_schools():
    """Boundary: zero schools in system"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_delete_from_two_schools():
    """Boundary: two schools (one above minimum)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1


def test_choice_0_exits():
    """Boundary: choice = 0 exits"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_choice_1_continues():
    """Boundary: choice = 1 continues"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "L1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "L2"})

    inputs = iter(["1", "1", "2", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_choice_exit():
    """Boundary: choice = (not 1) exits"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_large_school_id():
    """Boundary: large school ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 100, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["100", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
