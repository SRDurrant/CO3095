"""
Random testing for US4 - Delete School

Using randomized inputs
"""

import random
import string
from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def rand_string(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def test_random_single_deletion():
    """Delete random school from list"""
    random.seed(50)

    SCHOOLS.clear()
    for i in range(5):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{rand_string(5)}",
            "level": "primary",
            "location": rand_string(6)
        })

    delete_id = random.randint(1, 5)
    inputs = iter([str(delete_id), "2"])

    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 4


def test_random_multiple_deletions():
    """Delete multiple random schools"""
    random.seed(80)

    SCHOOLS.clear()
    for i in range(6):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{i}",
            "level": "primary",
            "location": rand_string(5)
        })

    # delete 3 schools
    ids_to_delete = random.sample(range(1, 7), 3)
    inputs_list = []
    for idx, school_id in enumerate(ids_to_delete):
        inputs_list.append(str(school_id))
        if idx < len(ids_to_delete) - 1:
            inputs_list.append("1")
        else:
            inputs_list.append("2")

    inputs = iter(inputs_list)
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 3


def test_random_invalid_then_valid():
    """Try random invalid ID then valid one"""
    random.seed(110)

    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    invalid_id = random.randint(10, 100)
    inputs = iter([str(invalid_id), "1", "2"])

    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0
