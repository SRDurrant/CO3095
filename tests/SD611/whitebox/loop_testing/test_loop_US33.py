from app.admin_actions import delete_user_by_id, list_all_users
from app.data_store import USERS, add_user

def setup_users_multiple():
    USERS.clear()
    add_user({"user_id": 1, "username": "admin-user", "password": "x", "role": "admin"})
    add_user({"user_id": 2, "username": "john", "password": "x", "role": "student"})
    add_user({"user_id": 3, "username": "mark", "password": "x", "role": "student"})


# Loop order + branch: delete user NOT first in list
def test_whitebox_delete_second_student_user():
    setup_users_multiple()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    # user_id 3 is NOT the first entry → tests branch inside the loop
    result = delete_user_by_id(3, mock_print)

    assert result is True
    assert outputs[0] == "User 'mark' (ID 3) has been deleted."
    assert len(USERS) == 2
    assert USERS[1]["username"] == "john"  # ensures correct element deleted

# Verify list_all_users prints correct order (loop sequencing)
def test_whitebox_list_all_users_order():
    setup_users_multiple()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    list_all_users(mock_print)

    # Check ordering
    assert "admin-user" in outputs[1]
    assert "john" in outputs[2]
    assert "mark" in outputs[3]

    # The order must match insertion order
    assert outputs[1].endswith("admin")
    assert outputs[2].endswith("student")
    assert outputs[3].endswith("student")