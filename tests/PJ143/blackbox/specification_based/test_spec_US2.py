"""
Specification-based tests for US2 - School Creation Validation

Testing the validation functions used in school creation
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


def test_valid_school_name():
    """Valid school name should be accepted"""
    is_valid, msg = validate_school_name("Springfield Elementary")

    assert is_valid is True
    assert msg == "Accepted"


def test_empty_name():
    """Empty name should be rejected"""
    is_valid, msg = validate_school_name("")

    assert is_valid is False
    assert "cannot be empty" in msg


def test_name_only_whitespace():
    """Name with only spaces should be rejected"""
    is_valid, msg = validate_school_name("    ")

    assert is_valid == False
    assert "cannot be empty" in msg


def test_name_too_short():
    """Name with less than 5 characters should fail"""
    is_valid, msg = validate_school_name("Test")

    assert not is_valid
    assert "at least 5 characters" in msg


def test_name_exactly_5_chars():
    """Name with exactly 5 characters should be valid"""
    is_valid, msg = validate_school_name("Hello")

    assert is_valid is True


def test_name_with_whitespace():
    """Name with leading/trailing spaces should be trimmed and validated"""
    is_valid, msg = validate_school_name("  Valid School  ")

    assert is_valid == True
    assert msg == "Accepted"


def test_valid_level_1():
    """Level choice '1' should be valid"""
    is_valid, msg = validate_school_level("1")

    assert is_valid is True
    assert msg == "Accepted"


def test_valid_level_2():
    """Level choice '2' should be valid"""
    is_valid, msg = validate_school_level("2")
    assert is_valid is True


def test_valid_level_3():
    """Level choice '3' should be valid"""
    is_valid, msg = validate_school_level("3")
    assert is_valid is True


def test_invalid_level_4():
    """Level choice '4' should be invalid"""
    is_valid, msg = validate_school_level("4")

    assert not is_valid
    assert "select 1, 2, or 3" in msg


def test_invalid_level_text():
    """Non-numeric level should be invalid"""
    is_valid, msg = validate_school_level("primary")

    assert is_valid == False


def test_valid_location():
    """Valid location should be accepted"""
    is_valid, msg = validate_school_location("London")

    assert is_valid is True
    assert msg == "Accepted"


def test_empty_location():
    """Empty location should be rejected"""
    is_valid, msg = validate_school_location("")

    assert is_valid is False
    assert "cannot be empty" in msg


def test_location_too_short():
    """Location with less than 3 characters should fail"""
    is_valid, msg = validate_school_location("AB")

    assert not is_valid
    assert "at least 3 characters" in msg


def test_location_exactly_3_chars():
    """Location with exactly 3 characters should be valid"""
    is_valid, msg = validate_school_location("NYC")

    assert is_valid == True


def test_no_duplicate_when_list_empty():
    """No duplicate when school list is empty"""
    schools = []
    is_unique, msg = check_duplicate_school(schools, "School", "London")

    assert is_unique is True
    assert msg == "Accepted"


def test_no_duplicate_different_name():
    """No duplicate when name is different"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School B", "London")

    assert is_unique is True


def test_no_duplicate_different_location():
    """No duplicate when location is different"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "School", "Aye")

    assert is_unique == True


def test_duplicate_detected_exact_match():
    """Duplicate should be detected for exact match"""
    schools = [{"name": "Test School", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "Test School", "London")

    assert is_unique is False
    assert "already exists" in msg


def test_duplicate_case_insensitive():
    """Duplicate check should be case insensitive"""
    schools = [{"name": "Test School", "location": "London"}]
    is_unique, msg = check_duplicate_school(schools, "TEST SCHOOL", "LONDON")

    assert not is_unique
    assert "already exists" in msg
