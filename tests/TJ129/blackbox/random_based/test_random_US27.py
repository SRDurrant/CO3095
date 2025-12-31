"""
Black-box random-based tests for US27 - Remove Favourite School

Randomly generates favourites and removes one -> count should drop by 1
"""

import random

from app.data_store import set_current_user, clear_current_user
from app.reviews import (
    FAVOURITES,
    clear_favourites,
    add_favourite_record,
    remove_favourite_school,
)


def reset_state():
    clear_current_user()
    clear_favourites()


def test_random_remove_one_favourite_reduces_count():
    reset_state()
    random.seed(99)

    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    # add random favourites
    fav_ids = []
    for _ in range(5):
        sid = f"SCH-{random.randint(1, 50)}"
        fav_ids.append(sid)
        add_favourite_record(1, sid)

    before = len(FAVOURITES)
    target = fav_ids[0]

    inputs_iter = iter([target])
    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is True
    assert result is True
    assert len(FAVOURITES) == before - 1
