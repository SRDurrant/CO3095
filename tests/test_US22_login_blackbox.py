"""
Black-box tests for US22 - User Login

These tests will simulate the ser interactions with they system using a fake input function
and capture the output via the fake print function.
"""

from app.auth import login_user
from app.data_store import USERS, add_user

def run_login_with_inputs(example_users, inputs):
    """
    Helper to run the user login with inputs

    Inputs:
        example_users (list[dict]): list of users to login
        inputs (list[str]): list of users to login

    Returns:
        Tuple:
            - success(bool): True if successful, False otherwise
            - result (dict | str): User dict on success, None on failure
            - outputs (list[str]): printed messages
    """

    USERS.clear()
    for u in example_users:
        add_user(u)

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = login_user(input_func = fake_input, print_func = fake_print)
    return success, result, outputs


def test_login_no_users_registered():
    """
    Tests the user login with no users registered into the system
    """

    success, result, outputs = run_login_with_inputs([], ["any-user", "any-password"])

    assert success is False
    assert result == "No registered users"
    assert any("No registered users" in line for line in outputs)


def test_login_unknown_username_then_cancel():
    """
    The test should show that when the username doesn't exist, it should fail and allow the user to cancel
    and go back to the main menu
    """
    user_example = [
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "user"}
    ]

    # First attempt is the user typing in an unknown username
    # Second attempt is the user inserting '0' and returning to the menu
    success, result, outputs = run_login_with_inputs(
        user_example,
        ["any-user1", "any_password", "0"]
    )

    assert success is False
    assert result == "Login cancelled"
    assert any("Username not found" in line for line in outputs)
    assert any("Returning to the main menu" in line for line in outputs)


def test_login_wrong_password_then_cancel():
    """
    The test should fail when the user inputs the incorrect password and then allow the
    user to cancel and go back to the main menu
    """

    user_example = [
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ]

    success, result, outputs = run_login_with_inputs(
        user_example,
        ["any-user", "any-password2", "0"]
    )

    assert success is False
    assert result == "Login cancelled"
    assert any("Incorrect password" in line for line in outputs)
    assert any("Returning to the main menu" in line for line in outputs)


def test_login_success_first_attempt():
    """
    The test should succeed when the user inputs the correct username and password
    and should then return to the main menu
    """

    example_users = [
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ]

    success, result, outputs = run_login_with_inputs(
        example_users,
        ["any-user", "any-password", "0"]
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["username"] == "any-user"
    assert any("Login successful" in line for line in outputs)


def test_login_user_cancels_immediately():
    """
    The test shows that when the user inputs '0' as the username
    they will not be logged in and go back to main menu
    """

    example_users = [
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ]

    success, result, outputs = run_login_with_inputs(
        example_users,
        ["0"]
    )

    assert success is False
    assert result == "Login cancelled"
    assert any("Returning to the main menu" in line for line in outputs)