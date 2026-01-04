"""
Boundary Value Analysis for US2 - School Creation Validation

Testing edge cases and boundary values
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


def test_name_length_4_invalid():
    """Boundary: 4 characters is just below minimum"""
    is_valid, msg = validate_school_name("ABCD")

    assert is_valid is False
    assert "at least 5 characters" in msg


def test_name_length_5_valid():
    """Boundary: 5 characters is minimum valid length"""
    is_valid, msg = validate_school_name("ABCDE")

    assert is_valid is True
    assert msg == "Accepted"


def test_location_length_2_invalid():
    """Boundary: 2 characters is below minimum"""
    is_valid, msg = validate_school_location("AB")

    assert not is_valid
    assert "at least 3 characters" in msg


def test_location_length_3_valid():
    """Boundary: 3 characters is minimum valid"""
    is_valid, msg = validate_school_location("ABC")

    assert is_valid is True


def test_level_1_valid():
    """Boundary: 1 is minimum valid choice"""
    is_valid, msg = validate_school_level("1")

    assert is_valid is True


def test_level_3_valid():
    """Boundary: 3 is maximum valid choice"""
    is_valid, msg = validate_school_level("3")

    assert is_valid == True


def test_level_4_invalid():
    """Boundary: 4 is above maximum valid choice"""
    is_valid, msg = validate_school_level("4")

    assert not is_valid
    assert "Invalid input" in msg
