"""
Branch coverage tests for US3 - Update School Details

Testing all execution paths
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def test_schools_empty_branch():
    """Branch: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_school_id_zero_branch():
    """Branch: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_school_id_empty_branch():
    """Branch: not school_id_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = update_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("cannot be empty" in s for s in outputs)


def test_school_id_not_digit_branch():
    """Branch: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_school_not_exists_branch():
    """Branch: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_name_zero_branch():
    """Branch: new_name == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_name_empty_keep_current():
    """Branch: new_name == '' (keep current)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Original", "level": "primary", "location": "London"})

    inputs = iter(["1", "", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "Original"


def test_name_validation_fails():
    """Branch: is_valid_name is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["1", "AB", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_level_zero_branch():
    """Branch: level_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["1", "Test", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_level_empty_keep_current_primary():
    """Branch: level_input == '' and current_level == 'primary'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["level"] == "primary"


def test_level_empty_keep_current_secondary():
    """Branch: level_input == '' and current_level == 'secondary'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Tests", "level": "secondary", "location": "London"})

    inputs = iter(["1", "Tests", "", "London", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["level"] == "secondary"


def test_level_validation_fails():
    """Branch: is_valid_level is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "5", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_location_empty_keep_current():
    """Branch: new_location == ''"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["location"] == "London"


def test_location_validation_fails():
    """Branch: is_valid_location is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "AB", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_duplicate_check_fails():
    """Branch: is_unique is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Aye"})

    inputs = iter(["2", "SchoolA", "1", "London", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_choice_one_continue():
    """Branch: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "AAAAA", "1", "Loc1", "1", "2", "BBBBB", "1", "Loc2", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 2


def test_updated_any_false():
    """Branch: updated_any remains False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_updated_any_true():
    """Branch: updated_any becomes True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "London"})

    inputs = iter(["1", "Updated", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
