from app.admin_actions import list_all_users
from app.data_store import USERS

def test_view_users_symbolic_whitebox():

    USERS.clear()
    USERS.append({})  # symbolic "unknown user"

    outputs = []
    list_all_users(print_func=lambda x: outputs.append(x))

    assert "ID: ?" in outputs[1]