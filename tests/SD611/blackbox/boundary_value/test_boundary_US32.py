from app.admin_actions import list_all_users
from app.data_store import USERS

def run_list_users():
    """
    Helper that calls list_all_users with a fake print function.

    Returns:
        list[str]: Captured printed output
    """

    outputs = []

    def fake_print(message: str):
        outputs.append(message)

    list_all_users(print_func=fake_print)
    return outputs

def test_view_users_no_users():
    """
        Case: No registered users exist.
        Expected: Should print 'No users found'.
    """
    USERS.clear()
    outputs = run_list_users()

    assert len(outputs) > 0
    assert "No users found" in outputs[0]

def test_view_users_single_user():
    """
        Case: Exactly one user exists.
        Expected: Should list the user correctly.
    """
    USERS.clear()
    USERS.append({
        "user_id": 1,
        "username": "admin-user",
        "role": "admin"
    })

    outputs = run_list_users()

    assert "=== Registered Users ===" in outputs[0]
    assert "admin-user" in outputs[1]
    assert "admin" in outputs[1]