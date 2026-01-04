"""
Concolic testing for US2 - School Creation Validation

Combining concrete and symbolic execution paths
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


def test_name_empty_path():
    """Path: empty name -> error"""
    is_valid, msg = validate_school_name("")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_name_too_short_path():
    """Path: valid format but too short -> error"""
    is_valid, msg = validate_school_name("Test")
    assert is_valid == False
    assert "at least 5 characters" in msg


def test_name_valid_path():
    """Path: all checks pass -> success"""
    is_valid, msg = validate_school_name("Valid School")
    assert is_valid is True
    assert msg == "Accepted"


def test_level_valid_1_path():
    """Path: level is '1' -> valid"""
    is_valid, msg = validate_school_level("1")
    assert is_valid == True


def test_level_valid_2_path():
    """Path: level is '2' -> valid"""
    is_valid, msg = validate_school_level("2")
    assert is_valid is True


def test_level_invalid_path():
    """Path: level not in list -> error"""
    is_valid, msg = validate_school_level("4")
    assert not is_valid
    assert "Invalid input" in msg


def test_location_empty_path():
    """Path: empty location -> error"""
    is_valid, msg = validate_school_location("")
    assert is_valid is False


def test_location_too_short_path():
    """Path: location too short -> error"""
    is_valid, msg = validate_school_location("AB")
    assert is_valid == False


def test_location_valid_path():
    """Path: valid location -> success"""
    is_valid, msg = validate_school_location("Loc")
    assert is_valid is True


def test_duplicate_found_path():
    """Path: duplicate found in list -> error"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School", "London")
    assert is_unique is False
    assert "already exists" in msg


def test_duplicate_not_found_path():
    """Path: no duplicate in list -> success"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School B", "Aye")
    assert is_unique == True


def test_duplicate_case_insensitive_path():
    """Path: different case but same school -> duplicate"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "SCHOOL", "LONDON")
    assert not is_unique
