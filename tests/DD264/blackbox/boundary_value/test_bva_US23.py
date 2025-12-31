from app.data_store import set_current_user, get_current_user, clear_current_user


def test_session_set_and_clear_user_boundary_minimal_dict():
    # boundary: minimal valid dict (only keys used elsewhere are optional here)
    user = {"user_id": 1}
    set_current_user(user)
    assert get_current_user() == user

    clear_current_user()
    assert get_current_user() is None
