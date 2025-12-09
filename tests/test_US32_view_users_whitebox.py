"""
White-box testing for US32 - Admin View All Registered Users

These tests explicitly target internal logic branches within list_all_users().
"""

from app.admin_actions import list_all_users
from app.data_store import USERS


def test_branch_no_users():
    """
    Branch test: users list is empty → should trigger the 'no users' branch.
    """

    USERS.clear()
    out = []

    def fake_print(msg): out.append(msg)

    list_all_users(print_func=fake_print)

    assert len(out) == 1
    assert "No users found" in out[0]


def test_branch_users_exist_header_printed():
    """
    Branch test: users exist → header must be printed before listing users.
    """

    USERS.clear()
    USERS.append({
        "user_id": 1,
        "username": "test-user",
        "role": "student"
    })

    out = []
    list_all_users(print_func=out.append)

    assert "=== Registered Users ===" in out[0]


def test_loop_single_iteration():
    """
    Loop test: exactly one user in USERS triggers loop exactly once.
    """

    USERS.clear()
    USERS.append({
        "user_id": 1,
        "username": "single-user",
        "role": "student"
    })

    out = []
    list_all_users(print_func=out.append)

    assert len(out) == 2    # header + one printed user line
    assert "single-user" in out[1]


def test_loop_multiple_iterations():
    """
    Loop test: multiple users → multiple loop iterations.
    """

    USERS.clear()
    USERS.extend([
        {"user_id": 1, "username": "u1", "role": "admin"},
        {"user_id": 2, "username": "u2", "role": "student"},
        {"user_id": 3, "username": "u3", "role": "student"},
    ])

    out = []
    list_all_users(print_func=out.append)

    # header + 3 user lines
    assert len(out) == 4
    assert "u3" in out[3]


def test_missing_keys_defaults_are_used():
    """
    White-box test: user dict missing keys should use '?' fallback via .get()
    """

    USERS.clear()
    USERS.append({"username": "ghost"})

    out = []
    list_all_users(print_func=out.append)

    assert "ID: ?" in out[1]
    assert "ghost" in out[1]