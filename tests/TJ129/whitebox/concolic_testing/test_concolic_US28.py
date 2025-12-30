"""
White-box concolic-style tests for US28 - View Favourite Schools

Runs the function with different concrete inputs to traverse paths.
"""

from app.reviews import view_favourite_schools, FAVOURITES
from app.data_store import set_current_user, clear_current_user


def reset_state():
    FAVOURITES.clear()
    clear_current_user()


def test_concolic_drives_cancel_then_empty_then_has_favourites():
    # Path 1: cancel
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    inputs = iter(["0"])
    ok1, _ = view_favourite_schools(input_func=lambda _: next(inputs, ""), print_func=lambda _: None)
    assert ok1 is False

    # Path 2: empty favourites
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    ok2, result2 = view_favourite_schools(input_func=lambda _: "", print_func=lambda _: None)
    assert ok2 is True
    assert result2 == []

    # Path 3: has favourites
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    FAVOURITES.append({"user_id": 1, "school_id": "5"})
    ok3, result3 = view_favourite_schools(input_func=lambda _: "", print_func=lambda _: None)
    assert ok3 is True
    assert len(result3) == 1
