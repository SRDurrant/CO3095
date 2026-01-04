"""
Branch coverage tests for US2 - School Creation Validation

Testing all code branches in validation functions
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


# validate_school_name branches
def test_name_not_name_branch():
    """Branch: not name"""
    is_valid, _ = validate_school_name(None)
    assert is_valid is False


def test_name_strip_empty_branch():
    """Branch: name.strip() == ''"""
    is_valid, _ = validate_school_name("   ")
    assert not is_valid


def test_name_len_short():
    """Branch: len < 5"""
    is_valid, _ = validate_school_name("Test")
    assert is_valid is False


def test_name_len_greater_equal_5():
    """Branch: len(cleaned) >= 5"""
    is_valid, _ = validate_school_name("Tests")
    assert is_valid == True


def test_name_valid_return():
    """Branch: return True, 'Accepted'"""
    is_valid, msg = validate_school_name("Valid Name")
    assert is_valid is True
    assert msg == "Accepted"


# validate_school_level branches
def test_level_in_valid_levels():
    """Branch: level_input in valid_levels"""
    is_valid, msg = validate_school_level("1")
    assert is_valid is True
    assert msg == "Accepted"


def test_level_not_in_valid_levels():
    """Branch: level_input not in valid_levels"""
    is_valid, msg = validate_school_level("5")
    assert not is_valid
    assert "Invalid input" in msg


def test_location_empty():
    """Branch: location== ''"""
    is_valid, _ = validate_school_location("")
    assert is_valid is False


def test_location_len_less_than_3():
    """Branch: len(cleaned) < 3"""
    is_valid, _ = validate_school_location("AB")
    assert not is_valid


def test_location_len_greater_equal_3():
    """Branch: len(cleaned) >= 3"""
    is_valid, _ = validate_school_location("ABC")
    assert is_valid is True


def test_location_valid_return():
    """Branch: return True, 'Accepted'"""
    is_valid, msg = validate_school_location("London")
    assert is_valid == True
    assert msg == "Accepted"


# check_duplicate_school branches
def test_duplicate_empty_schools_list():
    """Branch: empty schools list"""
    is_unique, msg = check_duplicate_school([], "School", "Location")
    assert is_unique is True
    assert msg == "Accepted"


def test_duplicate_match_found():
    """Branch: existing_name == cleaned_name and existing_location == cleaned_location"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School", "London")
    assert not is_unique
    assert "already exists" in msg


def test_duplicate_no_match():
    """Branch: no match found in loop"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School B", "Aye")
    assert is_unique is True


def test_duplicate_name_match_location_different():
    """Branch: name matches but location different"""
    schools = [{"name": "Test", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "Test", "Paris")
    assert is_unique == True


def test_duplicate_location_match_name_different():
    """Branch: location matches but name different"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "School B", "London")
    assert is_unique is True


def test_duplicate_case_conversion():
    """Branch: testing .lower() conversion"""
    schools = [{"name": "TEST", "location": "LONDON"}]
    is_unique, _ = check_duplicate_school(schools, "test", "london")
    assert is_unique is False


def test_duplicate_whitespace_strip():
    """Branch: testing .strip() on both sides"""
    schools = [{"name": "  Test  ", "location": "  London  "}]
    is_unique, _ = check_duplicate_school(schools, "Test", "London")
    assert not is_unique
