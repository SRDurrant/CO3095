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