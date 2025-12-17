"""
Black-box tests for US24 - Password Reset

These tests treat reset_password() as a black-box feature and validate observable behaviour:
- Success updates the correct user's password
- Unknown usernames are rejected (loop continues)
- Invalid password formats are rejected (loop continues)
- Mismatched confirmation is rejected (loop continues)
- User can cancel at multiple prompts using '0'
- Function fails gracefully when there are no registered users
"""

from app.auth import reset_password
from app.data_store import USERS, add_user


def setup_users(seed):
    """
    Reset and preload the global USERS list.

    Inputs:
        seed (list[dict]): users to preload

    Outputs:
        None
    """
    USERS.clear()
    for u in seed:
        add_user(u)


def run_reset_with_inputs(seed_users, inputs):
    """
    Helper to run reset_password with fake inputs and captured output

    Inputs:
        seed_users (list[dict]): users to preload
        inputs (list[str]): sequence of inputs fed into reset_password()

    Returns:
        tuple:
            - success (bool)
            - result (dict | str)
            - outputs (list[str])
    """
    setup_users(seed_users)
    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = reset_password(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_reset_fails_when_no_users_registered():
    """
    Tests that password reset fails early when there are no users in the system
    """
    success, result, outputs = run_reset_with_inputs([], ["alice"])

    assert success is False
    assert result == "\nNo registered users. Please register first"
    assert any("No registered users" in line for line in outputs)


def test_reset_cancel_immediately_at_username():
    """
    Tests that entering '0' at the username prompt cancels the reset flow
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Password reset cancelled" in line for line in outputs)


def test_reset_unknown_username_then_cancel():
    """
    Tests that an unknown username is rejected and user can cancel afterward
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["bob", "0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Username not found" in line for line in outputs)


def test_reset_unknown_username_then_success():
    """
    Tests that after entering an unknown username, user can retry with a valid username and succeed
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]

    success, result, outputs = run_reset_with_inputs(
        seed,
        ["bob", "alice", "newpassword123", "newpassword123"]
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["username"] == "alice"
    assert result["password"] == "newpassword123"
    assert any("Username not found" in line for line in outputs)
    assert any("Password reset successful" in line for line in outputs)


def test_reset_cancel_at_new_password_prompt():
    """
    Tests that entering '0' at the new password prompt cancels the reset flow
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["alice", "0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Password reset cancelled" in line for line in outputs)


def test_reset_cancel_at_confirm_password_prompt():
    """
    Tests that entering '0' at the confirm password prompt cancels the reset flow
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["alice", "newpassword123", "0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Password reset cancelled" in line for line in outputs)


def test_reset_rejects_short_password_then_cancel():
    """
    Tests that a short password is rejected and user can cancel after validation failure
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["alice", "123", "123", "0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Invalid Password" in line for line in outputs)
    assert any("at least 8 characters" in line for line in outputs)


def test_reset_rejects_mismatched_passwords_then_cancel():
    """
    Tests that mismatched passwords are rejected and user can cancel afterwards
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, outputs = run_reset_with_inputs(seed, ["alice", "newpassword123", "wrongpass", "0"])

    assert success is False
    assert result == "\nPassword reset cancelled"
    assert any("Passwords must match" in line for line in outputs)


def test_reset_rejects_mismatch_then_succeeds_on_retry():
    """
    Tests that after mismatch failure, user can retry the entire flow and succeed
    """
    seed = [{"user_id": 1, "username": "alice", "password": "oldpassword", "role": "student"}]

    success, result, outputs = run_reset_with_inputs(
        seed,
        [
            "alice",
            "newpassword123", "wrongpass",     # mismatch
            "alice",
            "finalpassword999", "finalpassword999"
        ]
    )

    assert success is True
    assert result["password"] == "finalpassword999"
    assert any("Passwords must match" in line for line in outputs)
    assert any("Password reset successful" in line for line in outputs)


def test_reset_updates_only_target_user_when_multiple_users_exist():
    """
    Tests that only the matching user's password is changed when multiple users exist
    """
    seed = [
        {"user_id": 1, "username": "alice", "password": "oldA", "role": "student"},
        {"user_id": 2, "username": "bob", "password": "oldB", "role": "student"},
    ]

    success, result, outputs = run_reset_with_inputs(seed, ["bob", "newpassword123", "newpassword123"])

    assert success is True
    assert result["username"] == "bob"
    assert result["password"] == "newpassword123"
    assert USERS[0]["password"] == "oldA"
    assert USERS[1]["password"] == "newpassword123"
    assert any("Password reset successful" in line for line in outputs)


def test_reset_preserves_non_password_fields():
    """
    Tests that user_id/role/username are preserved when password changes
    """
    seed = [{"user_id": 10, "username": "alice", "password": "oldpassword", "role": "student"}]
    success, result, _ = run_reset_with_inputs(seed, ["alice", "newpassword123", "newpassword123"])

    assert success is True
    assert result["user_id"] == 10
    assert result["role"] == "student"
    assert result["username"] == "alice"
