from app.auth import login_user
from app.data_store import add_user, clear_current_user, get_current_user


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def test_login_path_username_not_found_then_cancel():
    add_user({"user_id": 1, "username": "known", "password": "password1", "role": "student"})
    clear_current_user()

    # not found -> loop -> cancel with "0"
    input_func = make_input(["unknown", "0"])
    ok, msg = login_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert get_current_user() is None
    assert "cancel" in str(msg).lower()


def test_login_path_wrong_password_then_success():
    add_user({"user_id": 1, "username": "known", "password": "password1", "role": "student"})
    clear_current_user()

    # wrong pw -> loop -> correct pw
    input_func = make_input(["known", "wrongpass", "known", "password1"])
    ok, user = login_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is True
    assert user["username"] == "known"
    assert get_current_user()["username"] == "known"
