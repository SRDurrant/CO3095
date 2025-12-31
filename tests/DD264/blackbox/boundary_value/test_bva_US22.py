from app.auth import login_user
from app.data_store import add_user, set_current_user, clear_current_user, get_current_user


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def seed_user():
    add_user({"user_id": 1, "username": "u", "password": "password1", "role": "student"})


def test_login_empty_username_then_cancel():
    seed_user()
    clear_current_user()

    # empty username -> "not found" loop, then user cancels with "0"
    input_func = make_input(["", "0"])
    ok, msg = login_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert get_current_user() is None
    assert "cancel" in str(msg).lower()


def test_login_password_cancel_boundary():
    seed_user()
    clear_current_user()

    # username ok, then user enters "0" at password prompt to cancel
    input_func = make_input(["u", "0"])
    ok, msg = login_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert get_current_user() is None
    assert "cancel" in str(msg).lower()
