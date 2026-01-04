"""
Specification-based tests for US4 - Delete School

Testing the school deletion functionality
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def test_delete_single_school():
    """Delete a single school successfully"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_delete_school_from_multiple():
    """Delete one school when multiple exist"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Luton"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 1
    assert SCHOOLS[0]["school_id"] == 2


def test_delete_multiple_schools():
    """Delete multiple schools in one session"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})
    SCHOOLS.append({"school_id": 3, "name": "SchoolC", "level": "primary", "location": "Loc3"})

    inputs = iter(["1", "1", "2", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1


def test_no_schools_to_delete():
    """Should return False when no schools exist"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_invalid_school_id():
    """Non-existent ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("does not exist" in s for s in outputs)


def test_empty_school_id():
    """Empty ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("cannot be empty" in s for s in outputs)


def test_non_numeric_id():
    """Non-numeric ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("must be a number" in s for s in outputs)


def test_exit_at_id_prompt():
    """Exit when user enters 0"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False
    assert len(SCHOOLS) == 1


def test_delete_then_exit():
    """Delete one school then exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_invalid_then_valid_id():
    """Retry after invalid ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_delete_all_schools():
    """Delete all schools one by one"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "1", "2", ""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0
