"""
White-box tests for US23 - Session Handling

These tests directly target the session management helpers:
- set_current_user()
- get_current_user()
- clear_current_user()

They verify that the global CURRENT_USER state behaves correctly
in all branches
"""

from app.data_store import (
    set_current_user,
    get_current_user,
    clear_current_user,
)


def test_set_current_user():
    """
    set_current_user should store the given user dictionary as
    currently logged-in user.
    """

    clear_current_user()
    user = {"username": "any-user", "role": "student"}

    set_current_user(user)

    current = get_current_user()
    assert current is user
    assert current["username"] == "any-user"
    assert current["role"] == "student"


def test_clear_current_user():
    """
    clear_current_user should set the current user to None
    """

    user = {"username": "any-user", "role": "student"}
    set_current_user(user)

    assert get_current_user() is user

    clear_current_user()

    assert get_current_user() is None


def test_get_current_user_none_when_not_set():
    """
    get_current_user should return None if no current user is set.
    """

    clear_current_user()
    current = get_current_user()
    assert current is None