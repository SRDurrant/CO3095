"""
White-box tests for US24 - Password Reset

These tests force the key branches inside reset_password():
- no users -> fail early
- cancel at username
- username not found -> loop continues
- cancel at new password
- cancel at confirm
- invalid password -> validation fail -> loop continues
- success path -> updates password and returns
"""

from app.auth import reset_password
from app.data_store import USERS, add_user


def setup_users(seed):
    """
    Reset and preload USERS list

    Inputs:
        seed (list[dict]): users to preload

    Outputs:
        None
    """
    USERS.clear()
    for u in seed:
        add_user(u)


def test_branch_no_users_registered():
    """
    Tests the branch where there are no users and the function fails before entering the loop
    """
    setup_users([])
    inputs_iter = iter(["alice"])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = reset_password(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert result == "\nNo registered users. Please register first"
    assert any("No registered users" in line for line in outputs)


def test_branch_cancel_at_username():
    """
    Tests cancel branch where user enters 0 at username prompt
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"


def test_branch_username_not_found_then_success():
    """
    Tests username-not-found branch followed by a successful retry
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["bob", "alice", "newpassword123", "newpassword123"])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = reset_password(input_func=fake_input, print_func=fake_print)

    assert success is True
    assert result["password"] == "newpassword123"
    assert any("Username not found" in line for line in outputs)


def test_branch_cancel_at_new_password():
    """
    Tests cancel branch where user enters 0 at new password prompt
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"


def test_branch_cancel_at_confirm_password():
    """
    Tests cancel branch where user enters 0 at confirm password prompt
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "newpassword123", "0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"


def test_branch_invalid_password_then_cancel():
    """
    Tests invalid-password branch (fails validation) then user cancels by entering 0 at username prompt next
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "123", "123", "0"])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = reset_password(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Invalid Password" in line for line in outputs)


def test_branch_successful_reset():
    """
    Tests the success branch where username exists and password validation passes
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "newpassword123", "newpassword123"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is True
    assert result["password"] == "newpassword123"
    assert USERS[0]["password"] == "newpassword123"
