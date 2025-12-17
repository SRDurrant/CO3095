"""
White-box tests for US24 - Password Reset

These tests select inputs satisfying path conditions:
- users empty -> early failure
- username exists AND password valid -> success
- username exists AND password invalid -> validation failure path
- username exists AND mismatch -> mismatch path
- username not found -> loop continues until cancel
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


def test_symbolic_path_no_users():
    """
    Path condition: users list is empty -> return False with message
    """
    setup_users([])
    inputs_iter = iter(["alice"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nNo registered users. Please register first"


def test_symbolic_path_username_exists_password_valid():
    """
    Path condition: user exists AND validate_new_password returns True -> success
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "newpassword123", "newpassword123"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is True
    assert result["password"] == "newpassword123"


def test_symbolic_path_username_exists_password_invalid_then_cancel():
    """
    Path condition: user exists AND validate_new_password returns False -> loop continues, then cancel
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "123", "123", "0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"


def test_symbolic_path_username_exists_password_mismatch_then_cancel():
    """
    Path condition: user exists AND password != confirm -> loop continues, then cancel
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "newpassword123", "wrongpass", "0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"


def test_symbolic_path_username_not_found_then_cancel():
    """
    Path condition: username not found -> loop continues until user cancels
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["bob", "0"])

    success, result = reset_password(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert result == "\nPassword reset cancelled"
