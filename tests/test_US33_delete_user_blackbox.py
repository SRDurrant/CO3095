from app.data_store import USERS, add_user
from app.admin_actions import delete_user_by_id

def setup_function():
    USERS.clear()
    add_user({"user_id": 1, "username": "admin-user", "password": "x", "role": "admin"})
    add_user({"user_id": 2, "username": "student-user", "password": "x", "role": "student"})


def test_delete_student_user_blackbox():
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    # student-user has ID = 2
    result = delete_user_by_id(2, mock_print)

    assert result is True
    assert outputs[0] == "User 'student-user' (ID 2) has been deleted."


def test_delete_nonexistent_user_blackbox():
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_user_by_id(99, mock_print)

    assert result is False
    assert outputs[0] == "Error: User does not exist."
    assert len(USERS) == 2


def test_delete_admin_user_blackbox():
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    # Try to delete admin (ID = 1)
    result = delete_user_by_id(1, mock_print)

    assert result is False
    assert outputs[0] == "Error: Admin accounts cannot be deleted."


def test_delete_from_empty_list_blackbox():
    USERS.clear()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_user_by_id(1, mock_print)

    assert result is False
    assert outputs[0] == "Error: User does not exist."