"""
White-box tests for US2 - Validate School Creation Input

These tests will target the internal functions used for the validation functions used
by the school creation logic to ensure all branches and condtitions are exercised
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)

def test_validate_school_name_empty():
    """
    Tests that validate_school_name fails when name is empty
    """

    is_valid, msg = validate_school_name("")
    assert is_valid is False
    assert "School name cannot be empty" in msg


def test_validate_school_name_too_short():
    """
    Tests that validate_school_name fails when name is too short
    """

    is_valid, msg = validate_school_name("AB")
    assert is_valid is False
    assert "School name must be at least 5 characters long" in msg


def test_validate_school_name_valid():
    """
    Tests that validate_school_name passes for valid school names
    """

    is_valid, msg = validate_school_name("London School")
    assert is_valid is True
    assert msg == "Accepted"


def test_validate_school_level_valid_primary():
    """
    Tests that validate_school_level passes for level "1"
    """

    is_valid, msg = validate_school_level("1")
    assert is_valid is True
    assert msg == "Accepted"


def test_validate_school_level_valid_secondary():
    """
    Tests that validate_school_level passes for level "2"
    """

    is_valid, msg = validate_school_level("2")
    assert is_valid is True
    assert msg == "Accepted"


def test_validate_school_level_valid_combined():
    """
    Tests that validate_school_level passes for level "3"
    """

    is_valid, msg = validate_school_level("3")
    assert is_valid is True
    assert msg == "Accepted"


def test_validate_school_level_invalid_choice():
    """
    Tests that validate_school_level fails for invalid choices
    """

    is_valid, msg = validate_school_level("4")
    assert is_valid is False
    assert "Invalid input. Please select 1, 2, or 3" in msg


def test_validate_school_location_empty():
    """
    Tests that validate_school_location fails when location is empty
    """

    is_valid, msg = validate_school_location("")
    assert is_valid is False
    assert "School location cannot be empty" in msg


def test_validate_school_location_too_short():
    """
    Tests that validate_school_location fails when location is too short
    """

    is_valid, msg = validate_school_location("A")
    assert is_valid is False
    assert "School location must be at least 3 characters long" in msg


def test_validate_school_location_valid():
    """
    Tests that validate_school_location passes for valid locations
    """

    is_valid, msg = validate_school_location("London")
    assert is_valid is True
    assert msg == "Accepted"


def test_check_duplicate_school_no_duplicate():
    """
    Test that check_duplicate_school passes when no duplicate exists
    """

    schools = [
        {"school_id": 1, "name": "Existing School", "level": "primary", "location": "London"}
    ]

    is_unique, msg = check_duplicate_school(schools, "New School", "London")
    assert is_unique is True
    assert msg == "Accepted"


def test_check_duplicate_school_same_name_only():
    """
    Tests that check_duplicate_school passes when name is same but location differs
    """

    schools = [
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ]

    is_unique, msg = check_duplicate_school(schools, "Test School", "Manchester")
    assert is_unique is True
    assert msg == "Accepted"


def test_check_duplicate_school_same_location_only():
    """
    Tests that check_duplicate_school passes when location is same but name differs
    """

    schools = [
        {"school_id": 1, "name": "School A", "level": "primary", "location": "London"}
    ]

    is_unique, msg = check_duplicate_school(schools, "School B", "London")
    assert is_unique is True
    assert msg == "Accepted"


def test_check_duplicate_school_exact_match():
    """
    Tests that check_duplicate_school fails when both name and location match
    """

    schools = [
        {"school_id": 1, "name": "Existing School", "level": "primary", "location": "London"}
    ]

    is_unique, msg = check_duplicate_school(schools, "Existing School", "London")
    assert is_unique is False
    assert "A school with this name and location already exists" in msg
