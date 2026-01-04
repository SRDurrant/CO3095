"""
Concolic testing for US1

Combines concrete execution with symbolic analysis
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS


def test_path_exit_immediately():
    """Path: enter '0' at first prompt"""
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)
    assert result is False


def test_path_exit_at_level():
    """Path: valid name -> exit at level"""
    SCHOOLS.clear()
    inputs = iter(["Test School", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_path_exit_at_location():
    """Path: valid name -> valid level -> exit at location"""
    SCHOOLS.clear()
    inputs = iter(["Test School", "1", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_path_invalid_name_then_exit():
    """Path: invalid name -> retry -> exit"""
    SCHOOLS.clear()
    inputs = iter(["ABC", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_path_invalid_level_then_exit():
    """Path: valid name -> invalid level -> retry -> exit"""
    SCHOOLS.clear()
    inputs = iter(["Test School", "5", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_path_invalid_location_then_exit():
    """Path: valid name -> valid level -> invalid location -> exit"""
    SCHOOLS.clear()
    inputs = iter(["Test School", "1", "AB", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_path_add_school_then_exit():
    """Path: add one school then choose to exit"""
    SCHOOLS.clear()
    inputs = iter(["Test School", "1", "London", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True
    assert len(SCHOOLS) == 1


def test_path_add_multiple_schools():
    """Path: add school -> continue -> add another -> exit"""
    SCHOOLS.clear()
    inputs = iter([
        "First School", "1", "London", "1",
        "Second School", "2", "Aye", "2"
    ])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True
    assert len(SCHOOLS) == 2


def test_path_duplicate_then_exit():
    """Path: try duplicate -> get error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["School", "1", "London", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is False
    assert len(SCHOOLS) == 1  # original school only


def test_path_retry_after_duplicate():
    """Path: duplicate detected -> retry with different location -> success"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["School", "1", "London", "Aye", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 2
