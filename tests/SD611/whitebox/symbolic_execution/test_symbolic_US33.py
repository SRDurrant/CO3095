def test_delete_user_symbolic_conditions():
    """
    Symbolic reasoning:
    IF user exists AND role == admin → deletion must fail
    """
    from app.admin_actions import delete_user_by_id
    from app.data_store import USERS, add_user

    USERS.clear()
    add_user({"user_id": 1, "username": "admin", "password": "x", "role": "admin"})

    outputs = []
    result = delete_user_by_id(1, lambda m: outputs.append(m))

    # Symbolic constraint: role == admin
    assert result is False
    assert "cannot be deleted" in outputs[0]