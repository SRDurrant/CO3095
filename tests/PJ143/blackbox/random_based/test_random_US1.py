"""
Random testing for US1

Using random inputs to test the system
"""

import random
import string
from app.admin_actions import add_new_school
from app.data_store import SCHOOLS


def generate_random_string(length):
    """Generate a random string of given length"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def test_random_valid_school():
    """Add school with random valid inputs"""
    random.seed(42)

    SCHOOLS.clear()
    name = "School " + generate_random_string(10)
    location = generate_random_string(8)
    level = str(random.randint(1, 3))

    inputs = iter([name, level, location, "2"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1


def test_random_multiple_schools():
    """Add multiple schools with random data"""
    random.seed(100)
    SCHOOLS.clear()

    name1 = "School " + generate_random_string(7)
    name2 = "School " + generate_random_string(8)
    loc1 = generate_random_string(6)
    loc2 = generate_random_string(7)

    inputs = iter([
        name1, "1", loc1, "1",
        name2, "2", loc2, "2"
    ])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 2


def test_random_retry_after_error():
    """Test retrying after validation error with random data"""
    random.seed(200)
    SCHOOLS.clear()

    # first try with short name, then valid
    short_name = generate_random_string(3)  # too short
    valid_name = "School " + generate_random_string(6)
    location = generate_random_string(5)

    inputs = iter([short_name, valid_name, "1", location, "2"])
    outputs = []

    result = add_new_school(lambda _: next(inputs), outputs.append)

    assert result is True
    assert len(SCHOOLS) == 1
    assert any("at least 5 characters" in s for s in outputs)
