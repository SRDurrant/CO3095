"""
Black-box tests for US7 - Random Testing

Uses randomized inputs to test school filtering
"""

import random
import string
from app.school_actions import filter_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_text(n):
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_filter_location():
    """Filter by random location"""
    random.seed(70)

    SCHOOLS.clear()
    loc = rand_text(8)
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": loc})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": rand_text(7)})

    inputs_iter = iter(["1", loc, "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("School A" in line for line in outputs)


def test_random_filter_rating():
    """Filter by random rating value"""
    random.seed(80)

    SCHOOLS.clear()
    RATINGS.clear()
    min_rating = random.randint(1, 5)

    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Manchester"})
    RATINGS.append({"school_id": "1", "value": 5})
    RATINGS.append({"school_id": "2", "value": 1})

    inputs_iter = iter(["3", str(min_rating), "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # Should find high rating school if min_rating <= 5
    if min_rating <= 5:
        assert any("School A" in line for line in outputs)


def test_random_multiple_filters():
    """Apply multiple random filters"""
    random.seed(90)

    SCHOOLS.clear()
    loc1 = rand_text(6)
    loc2 = rand_text(7)

    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": loc1})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": loc2})

    inputs_iter = iter(["1", loc1, "", "2", "2", "", "0"])
    outputs = []

    filter_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("School A" in line for line in outputs) or any("School B" in line for line in outputs)
