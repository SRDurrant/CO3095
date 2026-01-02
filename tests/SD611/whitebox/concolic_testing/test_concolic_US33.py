from app.admin_actions import delete_user_by_id
from app.data_store import USERS, add_user

def test_delete_user_concolic_student_path():
    """
    Forces path:
    - user exists
    - role != admin
    """

    USERS.clear()
    add_user({"user_id": 1, "username": "admin", "password": "x", "role": "admin"})
    add_user({"user_id": 2, "username": "student", "password": "x", "role": "student"})

    outputs = []
    result = delete_user_by_id(2, lambda m: outputs.append(m))

    # Concrete execution
    assert result is True

    # Symbolic condition validation
    assert all(u["user_id"] != 2 for u in USERS)