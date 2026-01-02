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

def test_view_users_multiple_users():
    """
        Case: Multiple users exist.
        Expected: Should print all users.
    """
    USERS.clear()
    USERS.extend([
        {"user_id": 1, "username": "admin-user", "role": "admin"},
        {"user_id": 2, "username": "student1", "role": "student"},
    ])

    outputs = run_list_users()

    assert "=== Registered Users ===" in outputs[0]
    assert "admin-user" in outputs[1]
    assert "student1" in outputs[2]