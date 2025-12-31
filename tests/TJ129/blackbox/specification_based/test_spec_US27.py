"""
Black-box tests for US27 - Remove Favourite School (Specification Based)

Checks observable behaviour:
- login required
- cancel works
- removing existing favourite works
- removing non-existing favourite returns a friendly message
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


def run_remove_fav(example_user, inputs):
    reset_state()

    if example_user is not None:
        set_current_user(example_user)

    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = remove_favourite_school(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_remove_favourite_requires_login():
    success, result, outputs = run_remove_fav(None, [])
    assert success is False
    assert "logged in" in str(result).lower()


def test_remove_favourite_cancel():
    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    success, result, outputs = run_remove_fav(user, ["0"])
    assert success is False
    assert "cancelled" in str(result).lower()


def test_remove_existing_favourite_success():
    user = {"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}
    reset_state()
    set_current_user(user)
    add_favourite_record(1, "SCH-1")
    assert len(FAVOURITES) == 1

    inputs_iter = iter(["SCH-1"])
    outputs = []

    success, result = remove_favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda m: outputs.append(m),
    )

    assert success is True
    assert result is True
    assert len(FAVOURITES) == 0
    assert any("removed" in line.lower() for line in outputs)


def test_remove_non_existing_favourite_returns_true_false():
    user = {"user_id": 2, "username": "u2", "password": "x" * 8, "role": "student"}
    success, result, outputs = run_remove_fav(user, ["SCH-X"])
    assert success is True
    assert result is False
    assert any("not in your favourites" in line.lower() for line in outputs)
