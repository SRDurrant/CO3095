"""
Black-box testing for US23 - Session Handling

These tests will verify that a successful login sets the current user,
logging out clears the current session and the session is empty before any login attempt
"""

from app.auth import login_user
from app.data_store import (
    set_current_user,
    get_current_user,
    clear_current_user,
    USERS,
    add_user
)


def run_login_with_inputs(example_users, inputs):
    """
    Helper function for run_login_with_inputs

    Inputs:
    example_users (list[dict]): list of users to log in with
    inputs (list[str]): dictionary of inputs

    Returns:
        tuple:
            - success (bool): True is successful, False otherwise
            - results (dict | str): User dict on success, error message on failure
            - outputs (list[str]): list of output strings
    """

    USERS.clear()
    for u in example_users:
        add_user(u)

    clear_current_user()

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message:str) -> None:
        outputs.append(message)

    success, result = login_user(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_session_is_none_before_any_login():
    """
    Before any log in attempt, the current session should be empty
    """

    clear_current_user()
    assert get_current_user() is None


def test_successful_login_sets_current_user():
    """
    After a successful login attempt, the current user should be set
    """

    example_users = [
        {"user_id": 1, "username": "any-user", "password": "any-password", "role": "student"}
    ]

    success, result, outputs = run_login_with_inputs(
        example_users,
        ["any-user", "any-password"]
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["username"] == "any-user"
    assert any("Login successful" in line for line in outputs)

    current = get_current_user()
    assert current is result
    assert current["username"] == "any-user"


def test_logout_clears_session():
    """
    After a logout attempt, the current user should be cleared
    """

    example_user = {"username": "any-user", "role": "student"}
    set_current_user(example_user)

    assert get_current_user() == example_user

    clear_current_user()

    assert clear_current_user() is None