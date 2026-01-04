"""
Symbolic execution tests for US1

Testing path conditions symbolically
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS


def test_symbolic_name_is_zero():
    """Symbolic condition: name == '0'"""
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)
    assert result is False


def test_symbolic_name_not_zero():
    """Symbolic condition: name != '0'"""
    SCHOOLS.clear()
    inputs = iter(["Valid Name", "0"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    # execution continues past name check


def test_symbolic_validate_name_false():
    """Symbolic: is_valid_name returns False"""
    SCHOOLS.clear()
    inputs = iter(["AB", "0"])
    outputs = []
    result = add_new_school(lambda _: next(inputs), outputs.append)
    assert result is False
    assert any("at least 5 characters" in s for s in outputs)


def test_symbolic_validate_name_true():
    """Symbolic: is_valid_name returns True"""
    SCHOOLS.clear()
    inputs = iter(["Valid School", "0"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    # passes name validation


def test_symbolic_level_is_zero():
    """Symbolic: level_input == '0'"""
    SCHOOLS.clear()
    inputs = iter(["School", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_symbolic_validate_level_false():
    """Symbolic: is_valid_level returns False"""
    SCHOOLS.clear()
    inputs = iter(["School", "9", "0"])
    outputs = []
    result = add_new_school(lambda _: next(inputs), outputs.append)
    assert result is False


def test_symbolic_validate_level_true():
    """Symbolic: is_valid_level returns True"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "0"])
    add_new_school(lambda _: next(inputs), lambda _: None)


def test_symbolic_location_is_zero():
    """Symbolic: location == '0'"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_symbolic_validate_location_false():
    """Symbolic: is_valid_location returns False"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "X", "0"])
    outputs = []
    result = add_new_school(lambda _: next(inputs), outputs.append)
    assert result is False


def test_symbolic_validate_location_true():
    """Symbolic: is_valid_location returns True"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "London", "2"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True


def test_symbolic_is_unique_false():
    """Symbolic: is_unique returns False (duplicate)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})
    inputs = iter(["School", "1", "London", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is False


def test_symbolic_is_unique_true():
    """Symbolic: is_unique returns True"""
    SCHOOLS.clear()
    inputs = iter(["Unique School", "1", "London", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True


def test_symbolic_choice_is_one():
    """Symbolic: choice == '1'"""
    SCHOOLS.clear()
    inputs = iter(["School1", "1", "Aye", "1", "School2", "2", "Ste", "2"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert len(SCHOOLS) == 2


def test_symbolic_choice_not_one():
    """Symbolic: choice != '1'"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "Location", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True
    assert len(SCHOOLS) == 1


def test_symbolic_added_any_remains_false():
    """Symbolic: added_any stays False"""
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)
    assert result is False


def test_symbolic_added_any_becomes_true():
    """Symbolic: added_any becomes True"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "Loc", "2"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result is True


def test_symbolic_strip_whitespace():
    """Symbolic: name.strip() removes spaces"""
    SCHOOLS.clear()
    inputs = iter(["  School  ", "1", "  Loc  ", "0"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    assert SCHOOLS[0]["name"] == "School"
    assert SCHOOLS[0]["location"] == "Loc"
