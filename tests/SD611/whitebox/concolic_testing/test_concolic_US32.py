from app.admin_actions import list_all_users
from app.data_store import USERS

def test_view_users_concolic_whitebox():

    USERS.clear()
    USERS.append({"user_id": 0, "username": "", "role": ""})

    outputs = []
    list_all_users(print_func=lambda x: outputs.append(x))

    assert outputs[0] == "\n=== Registered Users ==="