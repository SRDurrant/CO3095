"""
White-box testing for US21 - User Registration

These tests will target the internal functions used by the registration logic
to make sure all the branches and conditions are exercised
"""

from app.auth import (
    validate_new_username,
    validate_new_password,
    find_user_by_username,
    get_next_user_id
)


def test_find_user_by_username():
    """
    This test will make sure that find_user_by_username finds the correct user
    """

    users = [
        {"user_id": 1, "username": "new-user1", "password": "password123", "role": "student"},
        {"user_id": 2, "username": "new-user2", "password": "password123", "role": "student"}
    ]
    user = find_user_by_username(users, "new-user2")
    assert user is not None
    assert user["user_id"] == 2


def test_find_user_by_username_not_found():
    """
    This test will make sure that find_user_by_username will return None when the user is not found
    """

    users = [
        {"user_id": 1, "username": "new-user1", "password": "password123", "role": "student"}
    ]
    user = find_user_by_username(users, "new-user2")
    assert user is None


def test_get_next_user_id_empty():
    """
    This test will make sure that get_next_user_id returns 1 for an empty list
    """

    users = []
    assert get_next_user_id(users) == 1


def test_get_next_user_id_non_empty_list():
    """
    This test will make sure that get_next_user_id returns max(existing IDs) + 1
    """

    users = [
        {"user_id": 1, "username": "new-user1", "password": "password123", "role": "student"},
        {"user_id": 2, "username": "new-user2", "password": "password123", "role": "student"}
    ]
    assert get_next_user_id(users) == 3


def test_validate_new_username_empty():
    """
    This test will make sure that validate_new_username fails if the password is empty
    """

    users = []
    is_valid, msg = validate_new_username(users, "")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_validate_new_username_short():
    """
    This test will make sure that validate_new_username fails if the username is too short
    """

    users = []
    is_valid, msg = validate_new_username(users, "us")
    assert is_valid is False
    assert "Username must be at least 3 characters long" in msg


def test_validate_new_username_duplicates():
    """
    This test will make sure that validate_new_username fails if there is more than one user
    with the same username
    """

    users = [
        {"user_id": 1, "username": "new-user1", "password": "password123", "role": "student"},
    ]
    is_valid, msg = validate_new_username(users, "new-user1")
    assert is_valid is False
    assert "Username already exists" in msg


def test_validate_new_username_valid():
    """
    This test will make sure that validate_new_username passes if the username is valid
    """

    users = [
        {"user_id": 1, "username": "new-user1", "password": "password123", "role": "student"},
    ]
    is_valid, msg = validate_new_username(users, "new-user2")
    assert is_valid is True
    assert "Username valid" in msg


def test_validate_new_password_empty():
    """
    This test will make sure that validate_new_password fails if the password is empty
    """

    is_valid, msg = validate_new_password("", "")
    assert is_valid is False
    assert "Password cannot be empty" in msg


def test_validate_new_password_short():
    """
    This test will make sure that validate_new_password fails if the password is too short
    """

    is_valid, msg = validate_new_password("123", "123")
    assert is_valid is False
    assert "Password must be at least 8 characters long" in msg


def test_validate_new_password_mismatch():
    """
    This test will make sure that validate_new_password fails if the password doesn't match the confirmation password
    """

    is_valid, msg = validate_new_password("password123", "password456")
    assert is_valid is False
    assert "Passwords must match" in msg


def test_validate_new_password_valid():
    """
    This test will make sure that validate_new_password passes if the password and confirmation is valid
    """

    is_valid, msg = validate_new_password("password123", "password123")
    assert is_valid is True
    assert "Password valid" in msg