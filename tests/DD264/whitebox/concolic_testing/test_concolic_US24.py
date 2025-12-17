"""
White-box tests for US24 - Password Reset

These tests execute reset_password multiple times with concrete inputs to traverse
distinct internal paths:
- success path
- cancel path
- username not found path
- invalid password path
- mismatch path
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


def test_concolic_runs_drive_multiple_paths():
    """
    Executes reset_password multiple times with different concrete inputs to drive distinct paths
    """

    # Path 1: success path
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter_1 = iter(["alice", "newpassword123", "newpassword123"])
    success_1, result_1 = reset_password(
        input_func=lambda _: next(inputs_iter_1, ""),
        print_func=lambda _: None
    )
    assert success_1 is True
    assert result_1["password"] == "newpassword123"

    # Path 2: cancel at username
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter_2 = iter(["0"])
    success_2, result_2 = reset_password(
        input_func=lambda _: next(inputs_iter_2, ""),
        print_func=lambda _: None
    )
    assert success_2 is False
    assert result_2 == "\nPassword reset cancelled"

    # Path 3: username not found then cancel
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter_3 = iter(["bob", "0"])
    success_3, result_3 = reset_password(
        input_func=lambda _: next(inputs_iter_3, ""),
        print_func=lambda _: None
    )
    assert success_3 is False
    assert result_3 == "\nPassword reset cancelled"

    # Path 4: invalid password then cancel
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter_4 = iter(["alice", "123", "123", "0"])
    success_4, result_4 = reset_password(
        input_func=lambda _: next(inputs_iter_4, ""),
        print_func=lambda _: None
    )
    assert success_4 is False
    assert result_4 == "\nPassword reset cancelled"

    # Path 5: mismatch then cancel
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter_5 = iter(["alice", "newpassword123", "wrongpass", "0"])
    success_5, result_5 = reset_password(
        input_func=lambda _: next(inputs_iter_5, ""),
        print_func=lambda _: None
    )
    assert success_5 is False
    assert result_5 == "\nPassword reset cancelled"
