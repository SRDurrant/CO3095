"""
Random testing for US6 - List All Schools

Using randomized inputs
"""

import random
import string
from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def rand_str(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_schools():
    """List random number of schools"""
    random.seed(35)

    SCHOOLS.clear()
    num_schools = random.randint(1, 8)

    for i in range(num_schools):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_str(4)}",
            "level": random.choice(["primary", "secondary", "combined"]),
            "location": rand_str(6)
        })

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("School" in s for s in outputs)


def test_random_ratings():
    """Schools with random ratings"""
    random.seed(65)

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(5):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{i + 1}",
            "level": "primary",
            "location": "London"
        })

        # randomly add ratings
        if random.random() > 0.5:
            num_ratings = random.randint(1, 3)
            for _ in range(num_ratings):
                RATINGS.append({"school_id": str(i + 1), "value": random.randint(1, 5)})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert len(outputs) > 0


def test_random_menu_choice():
    """Choose random valid menu option"""
    random.seed(95)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # random invalid choice then exit
    invalid_choice = str(random.randint(5, 10))
    inputs = iter([invalid_choice, "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)
