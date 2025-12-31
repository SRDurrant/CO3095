"""
White-box tests for US25 - Role-Based Access Control

These tests explicitly exercise the different branches inside
user_has_role and check_access
"""

from app.access_control import (
    user_has_role,
    check_access,
    ROLE_ADMIN,
    ROLE_STUDENT,
)


def test_user_has_role_branch_missing_role_key():
    """
    Branch: user dictionary exists but has no 'role' key, it should return False
    """
    user = {"username": "no-role-user"}

    result = user_has_role(user, [ROLE_ADMIN])

    assert result is False


def test_user_has_role_branch_required_roles_multiple_match():
    """
    Branch: required_roles contains multiple roles and the user has one of them
    """
    user = {"username": "student-user", "role": ROLE_STUDENT}

    result = user_has_role(user, [ROLE_ADMIN, ROLE_STUDENT])

    assert result is True


def test_check_access_branch_not_logged_in_both_messages():
    """
    Branch: current_user is None it should print login message and
    permission message, and deny access
    """
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(None, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is False
    assert any("must be logged in" in m for m in messages)
    assert not any("do not have permission" in m for m in messages)


def test_check_access_branch_insufficient_role():
    """
    Branch: user is logged in but does not have required role
    """
    user = {"username": "student-user", "role": ROLE_STUDENT}
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(user, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is False
    assert any("do not have permission" in m for m in messages)


def test_check_access_branch_allowed():
    """
    Branch: user is logged in and has required role
    """
    user = {"username": "admin-user", "role": ROLE_ADMIN}
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(user, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is True
    assert messages == []
