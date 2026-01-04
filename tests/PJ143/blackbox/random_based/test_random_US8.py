"""
Random testing for US8 - Search Schools by Name

Using randomized inputs
"""

import random
import string
from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_str(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_keyword_search():
    """Search with random keyword"""
    random.seed(40)

    SCHOOLS.clear()
    for i in range(5):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_str(5)}",
            "level": "primary",
            "location": "London"
        })

    # search for "School" which should match all
    inputs = iter(["School", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Found 5 school" in s for s in outputs)


def test_random_partial_match():
    """Random partial search"""
    random.seed(70)

    SCHOOLS.clear()
    school_name = f"Random{rand_str(6)}"
    SCHOOLS.append({"school_id": 1, "name": school_name, "level": "primary", "location": "London"})

    # search with first 6 chars
    keyword = school_name[:6]
    inputs = iter([keyword, "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any(school_name in s for s in outputs)


def test_random_no_match():
    """Random search with no matches"""
    random.seed(100)

    SCHOOLS.clear()
    SCHOOLS.append({
        "school_id": 1,
        "name": f"School{rand_str(8)}",
        "level": "primary",
        "location": "London"
    })

    # random unrelated keyword
    keyword = rand_str(10)
    inputs = iter([keyword, "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_random_with_ratings():
    """Search school with random ratings"""
    random.seed(130)

    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "TestSchool", "level": "primary", "location": "London"})

    # add random ratings
    for _ in range(random.randint(1, 5)):
        RATINGS.append({"school_id": "1", "value": random.randint(1, 5)})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("TestSchool" in s for s in outputs)
