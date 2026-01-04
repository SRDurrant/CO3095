"""
Specification-based tests for US3 - Update School Details

Testing the update school functionality
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def test_update_all_fields():
    """Update all fields of a school"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Old Name", "level": "primary", "location": "London"})

    inputs = iter(["1", "New Name", "2", "Aye", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "New Name"
    assert SCHOOLS[0]["level"] == "secondary"
    assert SCHOOLS[0]["location"] == "Aye"


def test_update_only_name():
    """Update only the name field"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Olden", "level": "primary", "location": "London"})

    inputs = iter(["1", "New Name", "", "", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["name"] == "New Name"
    assert SCHOOLS[0]["level"] == "primary"
    assert SCHOOLS[0]["location"] == "London"


def test_keep_current_name():
    """Press Enter to keep current name"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Current", "level": "primary", "location": "London"})

    inputs = iter(["1", "", "2", "Manny", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "Current"
    assert SCHOOLS[0]["level"] == "secondary"


def test_keep_current_level():
    """Press Enter to keep current level"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "secondary", "location": "London"})

    inputs = iter(["1", "School", "", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["level"] == "secondary"


def test_keep_current_location():
    """Press Enter to keep current location"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["location"] == "London"


def test_no_schools_in_system():
    """Should return False when no schools exist"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_invalid_school_id():
    """Non-existent school ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("does not exist" in s for s in outputs)


def test_empty_school_id():
    """Empty school ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("cannot be empty" in s for s in outputs)


def test_non_numeric_school_id():
    """Non-numeric school ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("must be a number" in s for s in outputs)


def test_duplicate_name_location():
    """Should reject duplicate name+location combination"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Qwe"})

    inputs = iter(["2", "School A", "1", "London", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("already exists" in s for s in outputs)


def test_exit_at_id_prompt():
    """Exit at school ID prompt"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_exit_at_name_prompt():
    """Exit at name prompt"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_update_multiple_schools():
    """Update multiple schools in one session"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Pre"})

    inputs = iter(["1", "AWAW A", "2", "Aye", "1", "2", "MMMM B", "1", "Uio", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["name"] == "AWAW A"
    assert SCHOOLS[1]["name"] == "Uio B"


def test_invalid_name_then_retry():
    """Invalid name, then retry with valid"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "AB", "Valid Name", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "Valid Name"
