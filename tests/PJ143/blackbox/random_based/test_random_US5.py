"""
Random testing for US5 - View School Profile

Using randomized inputs
"""

import random
import string
from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_str(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_school_view():
    """View random school from list"""
    random.seed(25)

    SCHOOLS.clear()
    for i in range(5):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_str(5)}",
            "level": random.choice(["primary", "secondary", "combined"]),
            "location": rand_str(6)
        })

    view_id = random.randint(1, 5)
    inputs = iter([str(view_id), ""])

    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_random_ratings():
    """View school with random ratings"""
    random.seed(55)

    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # add random number of ratings
    num_ratings = random.randint(1, 10)
    for _ in range(num_ratings):
        RATINGS.append({"school_id": "1", "value": random.randint(1, 5)})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    # should have some average displayed
    assert any("School Details" in s for s in outputs)


def test_random_invalid_then_valid():
    """Try random invalid ID then valid"""
    random.seed(85)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test1", "level": "primary", "location": "London"})

    invalid_id = random.randint(10, 50)
    inputs = iter([str(invalid_id), "5", ""])

    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True
