from app.data_store import set_current_user, get_current_user, clear_current_user


def test_session_paths_none_and_user():
    # Path: clear when already None
    clear_current_user()
    assert get_current_user() is None

    # Path: set then clear
    set_current_user({"user_id": 99, "username": "x", "role": "student"})
    assert get_current_user()["user_id"] == 99

    clear_current_user()
    assert get_current_user() is None
