"""
Black-box testing for US21 - User Registration

These tests simulate the user interactions with the system by fake input functions and
capture printed output via a fake print function.
"""

from app.auth import register_user
from app.data_store import USERS, add_user


def run_reg_with_inputs(inputs):
    """
    This function simulates a registration flow for US21

    Inputs:
        inputs (list[str]): list of user inputs: [username, password, confirm_password]

    Returns:
        tuple:
            - Success (bool): True if successful, False otherwise
            - Result (dict | str): New user dict on success, Error message on failure
            - Outputs (list[str]): List of printed messages from registration
    """

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        try:
            return next(inputs_iter)
        except StopIteration:
            return ""

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    # Resets the user before each simulation
    USERS.clear()

    success, result = register_user(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_reg_success():
    """
    Users enters all valid inputs
    """
    success, result, outputs = run_reg_with_inputs(
        ["new-user", "password123", "password123"]
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["username"] == "new-user"
    assert any("Registration Successful" in line for line in outputs)


def test_reg_fail_username():
    """
    Registration fails when the username is invalid
    """

    success, results, outputs = run_reg_with_inputs(
        ["", "password123", "password123"]
    )

    assert success is False
    assert "Username cannot be empty" in results


def test_reg_fail_short_username():
    """
    Registration fails when the username is too short
    """

    success, results, outputs = run_reg_with_inputs(
        ["new", "password123", "password123"]
    )

    assert success is False
    assert "Username must be at least 5 characters long" in results


def test_reg_fail_duplicate_username():
    """
    Registration fails when the username is already taken
    """
    USERS.clear()
    add_user(
        {
            "user_id": 1,
            "username": "existing",
            "password": "password123",
            "role": "student"
        }
    )

    inputs_iter = iter(["existing", "password123", "password123"])

    def fake_input(prompt: str) -> str:
        try:
            return next(inputs_iter)
        except StopIteration:
            return ""

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = register_user(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert "Username already exists" in result


def test_reg_fail_short_password():
    """
    Registration fails when the password is too short
    """

    success, results, outputs = run_reg_with_inputs(
        ["new-user", "123", "123"]
    )

    assert success is False
    assert "Password must be at least 8 characters long" in results


def test_reg_fail_mismatched_password():
    """
    Registration fails when the password and confirm_password are different
    """

    success, results, outputs = run_reg_with_inputs(
        ["new-user", "password123", "password456"]
    )

    assert success is False
    assert "Passwords must match" in results