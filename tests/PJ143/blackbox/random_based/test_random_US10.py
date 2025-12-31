"""
Black-box tests for US10 - Random Testing

Uses randomized inputs to test school comparison
"""

import random
import string
from app.school_actions import compare_two_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_text(n):
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_compare_schools():
    """Compare schools with random IDs"""
    random.seed(140)

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(5):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_text(3)}",
            "level": random.choice(["primary", "secondary", "combined"]),
            "location": rand_text(6)
        })
        RATINGS.append({"school_id": str(i + 1), "value": random.randint(1, 5)})

    id1 = random.randint(1, 5)
    id2 = random.randint(1, 5)
    while id2 == id1:
        id2 = random.randint(1, 5)

    inputs_iter = iter([str(id1), str(id2), "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("Comparison Summary" in line for line in outputs)


def test_random_multiple_comparisons():
    """Random sequence of multiple comparisons"""
    random.seed(150)

    SCHOOLS.clear()
    for i in range(4):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_text(4)}",
            "level": "primary",
            "location": rand_text(5)
        })

    comparisons = []
    for _ in range(2):
        id1 = random.randint(1, 4)
        id2 = random.randint(1, 4)
        while id2 == id1:
            id2 = random.randint(1, 4)
        comparisons.extend([str(id1), str(id2), "1"])
    comparisons[-1] = "0"

    inputs_iter = iter(comparisons)
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    # Should have multiple comparisons
    assert len(outputs) > 10


def test_random_ratings():
    """Compare schools with random ratings"""
    random.seed(160)

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Leeds"})

    rating1 = random.randint(1, 5)
    rating2 = random.randint(1, 5)

    RATINGS.append({"school_id": "1", "value": rating1})
    RATINGS.append({"school_id": "2", "value": rating2})

    inputs_iter = iter(["1", "2", "0"])
    outputs = []

    compare_two_schools(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda msg: outputs.append(msg)
    )

    assert any("School A" in line for line in outputs)
    assert any("School B" in line for line in outputs)
