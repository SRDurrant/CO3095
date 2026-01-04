"""
Symbolic execution tests for US3 - Update School Details

Testing symbolic path conditions
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def test_symbolic_schools_empty():
    """Symbolic: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_id_equals_zero():
    """Symbolic: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_symbolic_id_empty():
    """Symbolic: not school_id_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_symbolic_id_not_digit():
    """Symbolic: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_school_not_exists():
    """Symbolic: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_symbolic_name_equals_zero():
    """Symbolic: new_name == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_symbolic_name_equals_empty():
    """Symbolic: new_name == ''"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Original", "level": "primary", "location": "London"})

    inputs = iter(["1", "", "1", "London", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == "Original"


def test_symbolic_name_validation_false():
    """Symbolic: is_valid_name is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["1", "ABC", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_symbolic_level_equals_zero():
    """Symbolic: level_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Asdfg", "level": "primary", "location": "London"})

    inputs = iter(["1", "Current", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_symbolic_level_equals_empty_primary():
    """Symbolic: level_input == '' and current_level == 'primary'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["level"] == "primary"


def test_symbolic_level_equals_empty_secondary():
    """Symbolic: level_input == '' and current_level == 'secondary'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "secondary", "location": "London"})

    inputs = iter(["1", "School", "", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["level"] == "secondary"


def test_symbolic_level_validation_false():
    """Symbolic: is_valid_level is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "5", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_symbolic_location_equals_zero():
    """Symbolic: new_location == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "SChool", "1", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_location_equals_empty():
    """Symbolic: new_location == ''"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["location"] == "London"


def test_symbolic_location_validation_false():
    """Symbolic: is_valid_location is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "School", "1", "AB", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert not result


def test_symbolic_is_unique_false():
    """Symbolic: is_unique is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Aye"})

    inputs = iter(["2", "SchoolA", "1", "London", "0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_choice_equals_one():
    """Symbolic: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "SchoolAA", "1", "Loc1", "1", "2", "SchoolBB", "1", "Loc2", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_symbolic_updated_any_false():
    """Symbolic: updated_any remains False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_updated_any_true():
    """Symbolic: updated_any becomes True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    inputs = iter(["1", "Updated", "1", "London", "2"])
    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
