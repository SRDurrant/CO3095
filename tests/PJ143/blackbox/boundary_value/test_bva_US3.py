"""
Boundary Value Analysis for US3 - Update School Details

Testing boundary conditions for update validation
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def test_name_exactly_5_chars():
    """Boundary: minimum valid name length"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Old Name", "level": "primary", "location": "London"})

    inputs = iter(["1", "ABCDE", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "ABCDE"


def test_name_4_chars_invalid():
    """Boundary: just below minimum length"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Old", "level": "primary", "location": "London"})

    inputs = iter(["1", "ABCD", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("at least 5 characters" in s for s in outputs)


def test_location_exactly_3_chars():
    """Boundary: minimum valid location length"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "Old"})

    inputs = iter(["1", "School", "1", "ABC", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["location"] == "ABC"


def test_location_2_chars_invalid():
    """Boundary: just below minimum"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "AB", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("at least 3 characters" in s for s in outputs)


def test_level_choice_1():
    """Boundary: minimum level choice"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "secondary", "location": "London"})

    inputs = iter(["1", "School", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["level"] == "primary"


def test_level_choice_3():
    """Boundary: maximum level choice"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "3", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["level"] == "combined"


def test_level_choice_4_invalid():
    """Boundary: above maximum"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "4", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("Invalid input" in s for s in outputs)


def test_school_id_1_valid():
    """Boundary: school ID = 1"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "London", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
