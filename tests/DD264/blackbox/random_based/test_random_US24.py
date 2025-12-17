"""
Black-box tests for US24 - Password Reset

These tests use seeded random generation to validate reset_password over varied data:
- Random valid password resets succeed
- Repeated resets overwrite previous password (latest wins)
"""

import random
import string

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


def rand_text(n: int) -> str:
    """
    Generates random alphanumeric text

    Inputs:
        n (int): desired length

    Outputs:
        str: random string
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def test_random_valid_password_reset_succeeds():
    """
    Tests that a randomized valid password (>= 8 chars) resets successfully for an existing user
    """
    random.seed(101)
    username = f"user_{rand_text(6)}"
    new_pw = rand_text(12)

    setup_users([{"user_id": 1, "username": username, "password": "oldpassword", "role": "student"}])

    inputs_iter = iter([username, new_pw, new_pw])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    success, result = reset_password(input_func=fake_input, print_func=lambda _: None)

    assert success is True
    assert result["password"] == new_pw


def test_random_two_resets_latest_password_wins():
    """
    Tests that performing reset twice results in the second password being stored
    """
    random.seed(202)
    username = f"user_{rand_text(6)}"
    pw1 = rand_text(10)
    pw2 = rand_text(11)

    setup_users([{"user_id": 1, "username": username, "password": "oldpassword", "role": "student"}])

    inputs_iter_1 = iter([username, pw1, pw1])

    def fake_input_1(prompt: str) -> str:
        return next(inputs_iter_1, "")

    success1, result1 = reset_password(input_func=fake_input_1, print_func=lambda _: None)
    assert success1 is True
    assert result1["password"] == pw1

    inputs_iter_2 = iter([username, pw2, pw2])

    def fake_input_2(prompt: str) -> str:
        return next(inputs_iter_2, "")

    success2, result2 = reset_password(input_func=fake_input_2, print_func=lambda _: None)
    assert success2 is True
    assert result2["password"] == pw2
