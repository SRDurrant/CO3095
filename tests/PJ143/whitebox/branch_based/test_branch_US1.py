"""
Branch coverage testing for US1

Testing all the different execution paths
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS


def test_name_equals_zero():
    """Branch: name == '0'"""
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)
    assert result is False


def test_name_validation_fails():
    """Branch: is_valid_name is False"""
    SCHOOLS.clear()
    inputs = iter(["AB", "0"])  # too short
    outputs = []

    result = add_new_school(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("at least 5 characters" in s for s in outputs)


def test_name_validation_passes():
    """Branch: is_valid_name is True"""
    SCHOOLS.clear()
    inputs = iter(["Valid School", "0"])

    add_new_school(lambda _: next(inputs), lambda _: None)
    # continues to level prompt


def test_level_equals_zero():
    """Branch: level_input == '0'"""
    SCHOOLS.clear()
    inputs = iter(["School Name", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_level_validation_fails():
    """Branch: is_valid_level is False"""
    SCHOOLS.clear()
    inputs = iter(["School Name", "5", "0"])
    outputs = []

    result = add_new_school(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("Invalid input" in s for s in outputs)


def test_level_validation_passes():
    """Branch: is_valid_level is True"""
    SCHOOLS.clear()
    inputs = iter(["School Name", "1", "0"])

    add_new_school(lambda _: next(inputs), lambda _: None)
    # continues to location


def test_location_equals_zero():
    """Branch: location == '0'"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_location_validation_fails():
    """Branch: is_valid_location is False"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "AB", "0"])
    outputs = []

    result = add_new_school(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("at least 3 characters" in s for s in outputs)


def test_duplicate_check_fails():
    """Branch: is_unique is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test School", "1", "London", "0"])
    outputs = []

    result = add_new_school(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("already exists" in s for s in outputs)


def test_duplicate_check_passes():
    """Branch: is_unique is True - school gets added"""
    SCHOOLS.clear()
    inputs = iter(["Unique School", "1", "Aye", "2"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1


def test_choice_equals_one():
    """Branch: choice == '1' - add another"""
    SCHOOLS.clear()
    inputs = iter(["First", "1", "London", "1", "Second", "2", "Paris", "2"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 2


def test_choice_not_one():
    """Branch: choice != '1' - exit"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "London", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1


def test_added_any_false():
    """Branch: added_any is False when exiting early"""
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)
    assert result is False


def test_added_any_true():
    """Branch: added_any is True after adding school"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "London", "2"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_level_mapping_primary():
    """Test level_map for '1' -> 'primary'"""
    SCHOOLS.clear()
    inputs = iter(["School", "1", "Location", "2"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    assert SCHOOLS[0]["level"] == "primary"


def test_level_mapping_secondary():
    """Test level_map for '2' -> 'secondary'"""
    SCHOOLS.clear()
    inputs = iter(["School", "2", "Location", "2"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    assert SCHOOLS[0]["level"] == "secondary"


def test_level_mapping_combined():
    """Test level_map for '3' -> 'combined'"""
    SCHOOLS.clear()
    inputs = iter(["School", "3", "Location", "2"])
    add_new_school(lambda _: next(inputs), lambda _: None)
    assert SCHOOLS[0]["level"] == "combined"
