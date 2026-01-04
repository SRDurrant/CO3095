"""
Concolic testing for US4 - Delete School

Concrete execution paths
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def test_path_no_schools():
    """Path: no schools exist -> exit immediately"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_exit_immediately():
    """Path: schools exist -> user enters 0 -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False
    assert len(SCHOOLS) == 1


def test_path_empty_id_then_exit():
    """Path: empty ID -> error -> retry with 0 -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_path_invalid_id_then_exit():
    """Path: invalid ID -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_successful_delete_then_exit():
    """Path: delete school -> choose not to continue -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_path_delete_then_continue():
    """Path: delete -> continue (1) -> delete another -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "ScholA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SChoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "1", "2", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_path_non_numeric_retry_success():
    """Path: non-numeric ID -> retry with valid -> delete"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["abc", "1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_path_delete_all_then_no_schools():
    """Path: delete last school -> continue -> no schools left"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Last", "level": "primary", "location": "London"})

    inputs = iter(["1", "1", ""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_path_multiple_invalid_then_valid():
    """Path: multiple validation errors before success"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["", "abc", "999", "5", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0
