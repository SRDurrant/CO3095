"""
Symbolic execution tests for US2 - School Creation Validation

Testing symbolic path conditions
"""

from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)

# Symbolic conditions for validate_school_name
def test_symbolic_name_empty():
    """Symbolic: name == ''"""
    is_valid, _ = validate_school_name("")
    assert not is_valid


def test_symbolic_name_strip_not_empty():
    """Symbolic: name.strip() != ''"""
    is_valid, _ = validate_school_name("Valid")
    # continues to length check


def test_symbolic_len_cleaned_less_5():
    """Symbolic: len(cleaned) < 5"""
    is_valid, msg = validate_school_name("ABCD")
    assert is_valid is False
    assert "at least 5 characters" in msg


def test_symbolic_len_cleaned_equals_5():
    """Symbolic: len(cleaned) == 5"""
    is_valid, _ = validate_school_name("ABCDE")
    assert is_valid == True


def test_symbolic_len_cleaned_greater_5():
    """Symbolic: len(cleaned) > 5"""
    is_valid, _ = validate_school_name("ABCDEF")
    assert is_valid is True


# Symbolic conditions for validate_school_level
def test_symbolic_level_in_valid():
    """Symbolic: level_input in valid_levels (True)"""
    is_valid, msg = validate_school_level("1")
    assert is_valid is True
    assert msg == "Accepted"


def test_symbolic_level_not_valid():
    """Symbolic: level_input in valid_levels (False)"""
    is_valid, msg = validate_school_level("4")
    assert not is_valid
    assert "Invalid input" in msg


# Symbolic conditions for validate_school_location
def test_symbolic_location_is_none():
    """Symbolic: location is None"""
    is_valid, _ = validate_school_location(None)
    assert is_valid == False


def test_symbolic_location_len_less_3():
    """Symbolic: len(cleaned) < 3"""
    is_valid, msg = validate_school_location("AB")
    assert not is_valid
    assert "at least 3 characters" in msg


def test_symbolic_location_len_equals_3():
    """Symbolic: len == 3"""
    is_valid, _ = validate_school_location("ABC")
    assert is_valid is True


def test_symbolic_location_len_greater_3():
    """Symbolic: len > 3"""
    is_valid, _ = validate_school_location("ABCD")
    assert is_valid == True


# Symbolic conditions for check_duplicate_school
def test_symbolic_schools_empty_list():
    """Symbolic: schools list is empty"""
    is_unique, _ = check_duplicate_school([], "School", "London")
    assert is_unique is True


def test_symbolic_name_and_location_match():
    """Symbolic: existing_name == new_name AND existing_location == new_location"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "School", "London")
    assert is_unique is False


def test_symbolic_name_matches_location_not():
    """Symbolic: existing_name == new_name but existing_location != new_location"""
    schools = [{"name": "School", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "School", "Ris")
    assert is_unique == True


def test_symbolic_location_matches_name_not():
    """Symbolic: existing_location == new_location but existing_name != new_name"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "School B", "London")
    assert is_unique is True


def test_symbolic_neither_match():
    """Symbolic: both name and location are different"""
    schools = [{"name": "School A", "location": "London"}]
    is_unique, _ = check_duplicate_school(schools, "School B", "Qwer")
    assert is_unique == True
