"""
White-box Branch-Based tests for US26 - Favourite a School

Targets internal branches:
- Not logged in
- Wrong role
- Cancel path
- Empty input re-prompt path
- Already favourited path
- Success path
"""

from app.reviews import (
    favourite_school,
    clear_favourites,
    add_favourite_record,
    FAVOURITES,
)
from app.data_store import set_current_user, clear_current_user


def test_branch_not_logged_in():
    clear_favourites()
    clear_current_user()

    success, result = favourite_school(input_func=lambda _: "SCH-1", print_func=lambda _: None)
    assert success is False
    assert "logged in" in str(result).lower()


def test_branch_wrong_role_admin():
    clear_favourites()
    clear_current_user()
    set_current_user({"user_id": 1, "username": "admin", "password": "pw", "role": "admin"})

    success, result = favourite_school(input_func=lambda _: "SCH-1", print_func=lambda _: None)
    assert success is False
    assert "only students" in str(result).lower()


def test_branch_cancel_at_prompt():
    clear_favourites()
    clear_current_user()
    set_current_user({"user_id": 2, "username": "stud", "password": "pw", "role": "student"})

    inputs_iter = iter(["0"])
    success, result = favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None,
    )
    assert success is False
    assert "cancelled" in str(result).lower()
    assert len(FAVOURITES) == 0


def test_branch_empty_then_success():
    clear_favourites()
    clear_current_user()
    set_current_user({"user_id": 3, "username": "stud2", "password": "pw", "role": "student"})

    inputs_iter = iter(["", "SCH-X"])
    outputs = []

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=fake_print,
    )
    assert success is True
    assert result["school_id"] == "SCH-X"
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_branch_already_favourited_path():
    clear_favourites()
    clear_current_user()
    user = {"user_id": 4, "username": "stud3", "password": "pw", "role": "student"}
    set_current_user(user)

    add_favourite_record(user["user_id"], "SCH-9")

    inputs_iter = iter(["SCH-9"])
    outputs = []

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=fake_print,
    )
    assert success is True
    assert len(FAVOURITES) == 1
    assert any("already" in line.lower() for line in outputs)


def test_branch_success_path_adds_new():
    clear_favourites()
    clear_current_user()
    user = {"user_id": 5, "username": "stud4", "password": "pw", "role": "student"}
    set_current_user(user)

    inputs_iter = iter(["SCH-NEW"])
    success, result = favourite_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None,
    )
    assert success is True
    assert result["school_id"] == "SCH-NEW"
    assert len(FAVOURITES) == 1
