"""
White-box tests for US22 - User Login

These tests will test the specific branches within the login_user by controller
the USERS list and the sequence of provided inputs
"""

from app.auth import login_user
from app.data_store import USERS, add_user

def setup_users(seed):
    """
    Reset and place example users into the global USERS list

    Inputs:
        seed (list [dict]): a list of users to preload the system

    Outputs:
        None
    """

    USERS.clear()
    for u in seed:
        add_user(u)


def test_branch_no_users():
    """
    Test the branch with no users which should result in failure before the loop begins
    """

    setup_users([])
    inputs_iter = iter(["any-user", "any-password"])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_prints(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func = fake_input, print_func = fake_prints)

    assert success is False
    assert result == "No registered users"
    assert any("No registered users" in line for line in outputs)


def test_branch_cancel_at_username():
    """
    Test the branch with cancel at username by immediately inputting 0
    """

    setup_users(
        [{"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}]
    )

    inputs_iter = iter(["0"])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_prints(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func = fake_input, print_func = fake_prints)

    assert success is False
    assert result == "Login cancelled"
    assert any("Returning to the main menu" in line for line in outputs)


def test_branch_username_not_found_then_cancel():
    """
    This branch is testing that when the username is not found, the user stays in the loop
    and then the user inputs 0 to cancel is returned to the main menu
    """

    setup_users([
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ])

    inputs_iter = iter([
        "any-user1", # username that is not in the system
        "0" # cancels on the next username prompt
    ])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_prints(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func = fake_input, print_func = fake_prints)

    assert success is False
    assert result == "Login cancelled"
    assert any("Username not found" in line for line in outputs)


def test_branch_invalid_password_then_cancel():
    """
    This branch is testing that when the password is invalid, the user stays in the loop
    and then the user inputs 0 to cancel is returned to the main menu
    """
    setup_users([
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ])

    inputs_iter = iter([
        "any-user",  # correct username
        "any-password1", # incorrect Password
        "0"  # cancels on the password prompt
    ])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_prints(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func=fake_input, print_func=fake_prints)

    assert success is False
    assert result == "Login cancelled"
    assert any("Incorrect password" in line for line in outputs)


def test_branch_successful_login():
    """
    This branch is testing that when the username and password is successful,
    the user exists the loop and is returned to the main menu
    :return:
    """

    setup_users([
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ])

    inputs_iter = iter([
        "any-user",  # correct username
        "any-password", # correct Password
    ])

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_prints(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func=fake_input, print_func=fake_prints)

    assert success is True
    assert isinstance(result, dict)
    assert result["username"] == "any-user"
    assert any("Login successful" in line for line in outputs)