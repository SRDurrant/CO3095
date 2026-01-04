"""
Random testing for US2 - School Creation Validation

Using random inputs to test validation
"""

import random
import string
from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def test_random_valid_names():
    """Test with random valid names"""

    for _ in range(5):
        name = generate_random_string(random.randint(5, 20))
        is_valid, _ = validate_school_name(name)
        assert is_valid is True


def test_random_invalid_names():
    """Test with random invalid names (too short)"""

    for _ in range(5):
        name = generate_random_string(random.randint(1, 4))
        is_valid, _ = validate_school_name(name)
        assert is_valid is False


def test_random_valid_locations():
    """Test with random valid locations"""

    for _ in range(5):
        location = generate_random_string(random.randint(3, 15))
        is_valid, _ = validate_school_location(location)
        assert is_valid == True


def test_random_level_choices():
    """Test random valid level choices"""

    for _ in range(10):
        level = str(random.randint(1, 3))
        is_valid, _ = validate_school_level(level)
        assert is_valid is True


def test_random_invalid_levels():
    """Test random invalid level choices"""

    invalid_choices = ["4", "5", "10", "abc", ""]
    for choice in invalid_choices:
        is_valid, _ = validate_school_level(choice)
        assert not is_valid


def test_random_duplicate_check():
    """Test duplicate checking with random schools"""

    schools = []
    for i in range(5):
        school = {
            "name": f"School{i}",
            "location": generate_random_string(5)
        }
        schools.append(school)

    # check against existing school
    is_unique, _ = check_duplicate_school(schools, "School0", schools[0]["location"])
    assert is_unique is False

    # check new school
    is_unique, _ = check_duplicate_school(schools, "NewSchool", "NewLocation")
    assert is_unique == True
