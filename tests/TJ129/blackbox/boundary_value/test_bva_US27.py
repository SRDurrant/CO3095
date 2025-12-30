"""
Black-box boundary value tests for US27 - Remove Favourite School

Boundaries:
- empty school id
- whitespace school id
"""

from app.data_store import set_current_user, clear_current_user
from app.reviews import clear_favourites, remove_favourite_school


def reset_state():
    clear_current_user()
    clear_favourites()


def test_boundary_empty_school_id_fails():
    reset_state()
    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    inputs_iter = iter([""])
    outputs = []

    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda m: outputs.append(m),
    )

    assert success is False
    assert "cannot be empty" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_boundary_whitespace_school_id_fails():
    reset_state()
    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    set_current_user(user)

    inputs_iter = iter(["   "])
    outputs = []

    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda m: outputs.append(m),
    )

    assert success is False
    assert "cannot be empty" in str(result).lower()
