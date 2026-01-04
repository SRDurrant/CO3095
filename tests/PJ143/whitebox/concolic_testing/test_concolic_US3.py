"""
Concolic testing for US3 - Update School Details

Concrete execution paths
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def test_path_no_schools():
    """Path: no schools exist -> exit"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_exit_at_id():
    """Path: exit at ID prompt"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_path_exit_at_name():
    """Path: select school -> exit at name"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_path_exit_at_level():
    """Path: valid ID -> valid name -> exit at level"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "New Name", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_exit_at_location():
    """Path: valid ID -> name -> level -> exit at location"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "New Name", "2", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_path_successful_update():
    """Path: complete update successfully"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "New Name", "2", "Ess", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "New Name"


def test_path_keep_all_current():
    """Path: press Enter to keep all current values"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "", "", "", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["name"] == "AAAAA"
    assert SCHOOLS[0]["level"] == "primary"
    assert SCHOOLS[0]["location"] == "London"


def test_path_invalid_name_retry():
    """Path: invalid name -> retry -> success"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "AB", "Valid Name", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "Valid Name"


def test_path_update_multiple():
    """Path: update -> continue -> update another"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAAA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "BBBBBB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "AAAAA", "1", "Loc1", "1", "2", "BBBBB", "1", "Loc2", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "AAAAA"
    assert SCHOOLS[1]["name"] == "BBBBB"


def test_path_duplicate_retry():
    """Path: duplicate detected -> retry with different location"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAAA", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "BBBBBB", "level": "primary", "location": "Aye"})

    inputs = iter(["2", "AAAAAA", "1", "London", "Asd", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[1]["location"] == "Asd"
