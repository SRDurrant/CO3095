"""
White-box symbolic-execution style tests for US28 - View Favourite Schools

We pick concrete values to satisfy path conditions:
- current_user is None
- choice == "0"
- favourites list empty
- favourites list non-empty
"""

from app.reviews import view_favourite_schools, FAVOURITES
from app.data_store import set_current_user, clear_current_user


def reset_state():
    FAVOURITES.clear()
    clear_current_user()


def test_symbolic_path_user_none():
    reset_state()
    ok, result = view_favourite_schools(input_func=lambda _: "", print_func=lambda _: None)
    assert ok is False
    assert "logged in" in str(result).lower()


def test_symbolic_path_choice_cancel():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    inputs = iter(["0"])
    ok, result = view_favourite_schools(input_func=lambda _: next(inputs, ""), print_func=lambda _: None)
    assert ok is False
    assert "cancelled" in str(result).lower()


def test_symbolic_path_empty_favourites():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    ok, result = view_favourite_schools(input_func=lambda _: "", print_func=lambda _: None)
    assert ok is True
    assert result == []


def test_symbolic_path_has_favourites():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    FAVOURITES.append({"user_id": 1, "school_id": "1"})
    ok, result = view_favourite_schools(input_func=lambda _: "", print_func=lambda _: None)
    assert ok is True
    assert len(result) == 1
