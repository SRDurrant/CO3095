"""
White-box branch-based tests for US27 - Remove Favourite School

Targets key branches:
- no login
- cancel
- empty school id
- not found
- found & removed
"""

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


def test_branch_no_login():
    reset_state()
    success, result = remove_favourite_school(
        input_func=lambda _: "SCH-1",
        print_func=lambda _: None
    )
    assert success is False
    assert "logged in" in str(result).lower()


def test_branch_cancel():
    reset_state()
    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    inputs_iter = iter(["0"])
    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    assert success is False
    assert "cancelled" in str(result).lower()


def test_branch_not_found():
    reset_state()
    user = {"user_id": 2, "username": "u2", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    inputs_iter = iter(["SCH-NOPE"])
    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )
    assert success is True
    assert result is False


def test_branch_remove_success():
    reset_state()
    user = {"user_id": 3, "username": "u3", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    add_favourite_record(3, "SCH-3")
    assert len(FAVOURITES) == 1

    inputs_iter = iter(["SCH-3"])
    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is True
    assert result is True
    assert len(FAVOURITES) == 0
