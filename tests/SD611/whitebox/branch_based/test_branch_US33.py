from app.admin_actions import delete_user_by_id, list_all_users
from app.data_store import USERS, add_user

def setup_users_multiple():
    USERS.clear()
    add_user({"user_id": 1, "username": "admin-user", "password": "x", "role": "admin"})
    add_user({"user_id": 2, "username": "john", "password": "x", "role": "student"})
    add_user({"user_id": 3, "username": "mark", "password": "x", "role": "student"})

def test_whitebox_admin_cannot_be_deleted():
    setup_users_multiple()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_user_by_id(1, mock_print)

    assert result is False
    assert outputs[0] == "Error: Admin accounts cannot be deleted."
    assert len(USERS) == 3  # unchanged

def test_whitebox_empty_list_no_users():
    USERS.clear()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_user_by_id(5, mock_print)

    assert result is False
    assert outputs[0] == "Error: User does not exist."
    assert USERS == []