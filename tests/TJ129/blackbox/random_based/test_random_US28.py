"""
Black-box random-based tests for US28 - View Favourite Schools

Randomly creates favourites for multiple users, then checks:
- view returns only the current user's favourites
"""

import random

from app.reviews import view_favourite_schools, FAVOURITES
from app.data_store import set_current_user, clear_current_user


def reset_state():
    FAVOURITES.clear()
    clear_current_user()


def test_random_user_only_sees_own_favourites():
    reset_state()
    random.seed(42)

    # create random favourites for users 1..3
    for _ in range(30):
        uid = random.randint(1, 3)
        sid = str(random.randint(1, 10))
        FAVOURITES.append({"user_id": uid, "school_id": sid})

    set_current_user({"user_id": 2, "username": "u2", "role": "student"})

    outputs = []
    ok, result = view_favourite_schools(input_func=lambda _: "", print_func=lambda m: outputs.append(m))

    assert ok is True
    assert all(f["user_id"] == 2 for f in result)
    assert len(result) == len([f for f in FAVOURITES if f["user_id"] == 2])
