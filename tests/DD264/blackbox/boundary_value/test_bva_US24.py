"""
Black-box tests for US24 - Password Reset

These tests target boundary conditions of password validation:
- Length exactly 8 should pass
- Length 7 should fail
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


def test_password_length_exactly_8_passes():
    """
    Tests boundary: password length == 8 should be accepted
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "12345678", "12345678"])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    success, result = reset_password(input_func=fake_input, print_func=lambda _: None)

    assert success is True
    assert result["password"] == "12345678"


def test_password_length_7_fails_then_cancel():
    """
    Tests boundary: password length == 7 should be rejected, then user cancels
    """
    setup_users([{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}])
    inputs_iter = iter(["alice", "1234567", "1234567", "0"])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = reset_password(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("at least 8 characters" in line for line in outputs)
