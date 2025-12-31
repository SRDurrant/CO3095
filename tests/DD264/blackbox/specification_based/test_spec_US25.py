"""
Black-box tests for US25 - Role-Based Access Control

These tests treat the access control helpers as black-box utilities
and assert on their observable behaviour and messages
"""

from app.access_control import (
    user_has_role,
    check_access,
    ROLE_ADMIN,
    ROLE_STUDENT,
)


def test_user_has_role_admin_true():
    """
    user_has_role should return True when the user has the required role
    """
    user = {"username": "admin-user", "role": ROLE_ADMIN}

    result = user_has_role(user, [ROLE_ADMIN])

    assert result is True


def test_user_has_role_student_false_for_admin_action():
    """
    user_has_role should return False when the user does not have
    any of the required roles
    """
    user = {"username": "student-user", "role": ROLE_STUDENT}

    result = user_has_role(user, [ROLE_ADMIN])

    assert result is False


def test_user_has_role_none_user_returns_false():
    """
    user_has_role should return False when there is no user
    """
    result = user_has_role(None, [ROLE_ADMIN])

    assert result is False


def test_check_access_denies_when_not_logged_in():
    """
    check_access should deny access and print appropriate messages
    when no user is logged in
    """
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(None, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is False
    assert any("must be logged in" in m for m in messages)
    assert not any("do not have permission" in m for m in messages)


def test_check_access_denies_when_role_insufficient():
    """
    check_access should deny access and print a permission error when the
    user does not have any of the required roles
    """
    user = {"username": "student-user", "role": ROLE_STUDENT}
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(user, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is False
    assert any("do not have permission" in m for m in messages)


def test_check_access_allows_when_role_sufficient():
    """
    check_access should allow access when the user has at least one of the
    required roles and should not print any error messages
    """
    user = {"username": "admin-user", "role": ROLE_ADMIN}
    messages = []

    def fake_print(msg: str) -> None:
        messages.append(msg)

    allowed = check_access(user, [ROLE_ADMIN], print_func=fake_print)

    assert allowed is True
    assert messages == []
