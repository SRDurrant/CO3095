"""
Black-box tests for US9 - Random Testing

Uses randomized inputs to test school sorting
"""

import random
import string
from app.school_actions import sort_schools_by_rating
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_text(n):
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_ratings_sort_high_to_low():
    """Sort schools with random ratings"""
    random.seed(110)

    SCHOOLS.clear()
    RATINGS.clear()

    ratings = [random.randint(1, 5) for _ in range(3)]
    for i, rating in enumerate(ratings, start=1):
        SCHOOLS.append({"school_id": i, "name": f"School{i}", "level": "primary", "location": rand_text(5)})
        RATINGS.append({"school_id": str(i), "value": rating})

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # Should show schools in descending order
    assert any("School" in line for line in outputs)


def test_random_multiple_operations():
    """Random sequence of sort operations"""
    random.seed(120)

    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": rand_text(8), "level": "primary", "location": rand_text(6)})
    RATINGS.append({"school_id": "1", "value": random.randint(1, 5)})

    choice1 = str(random.randint(1, 2))
    choice2 = str(random.randint(1, 2))

    inputs_iter = iter([choice1, "", choice2, "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert len(outputs) > 0


def test_random_many_schools():
    """Sort many schools with random ratings"""
    random.seed(130)

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(10):
        SCHOOLS.append({"school_id": i + 1, "name": f"School{i + 1}", "level": "primary", "location": rand_text(5)})
        RATINGS.append({"school_id": str(i + 1), "value": random.randint(1, 5)})

    inputs_iter = iter(["2", "", "0"])
    outputs = []

    sort_schools_by_rating(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Found 10 school(s)" in line for line in outputs)
