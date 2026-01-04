"""
Random testing for US3 - Update School Details

Using randomized inputs
"""

import random
import string
from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS


def rand_string(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_name_update():
    """Update with random name"""
    random.seed(30)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    new_name = "School " + rand_string(10)
    inputs = iter(["1", new_name, "1", "London", "2"])

    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == new_name


def test_random_location_update():
    """Update with random location"""
    random.seed(60)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "Loc"})

    new_loc = rand_string(8)
    inputs = iter(["1", "School", "1", new_loc, "0"])

    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["location"] == new_loc


def test_random_multiple_updates():
    """Update multiple schools with random data"""
    random.seed(90)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    name1 = "School " + rand_string(5)
    name2 = "School " + rand_string(6)

    inputs = iter([
        "1", name1, "2", rand_string(5), "1",
        "2", name2, "1", rand_string(6), "0"
    ])

    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert SCHOOLS[0]["name"] == name1
    assert SCHOOLS[1]["name"] == name2


def test_random_level_changes():
    """Randomly change levels"""
    random.seed(120)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School", "level": "primary", "location": "London"})

    new_level = str(random.randint(1, 3))
    inputs = iter(["1", "School", new_level, "London", "0"])

    result = update_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
