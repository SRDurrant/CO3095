from app.auth import register_user
from app.data_store import add_user, get_users


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def test_register_paths_invalid_username_then_success():
    # Path 1: invalid username (<3) -> fail
    input_func = make_input(["ab", "password1", "password1"])
    ok, _ = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert len(get_users()) == 0

    # Path 2: valid username/password -> success
    input_func = make_input(["abc", "password1", "password1"])
    ok, user = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is True
    assert user["username"] == "abc"
    assert len(get_users()) == 1


def test_register_paths_duplicate_username():
    add_user({"user_id": 1, "username": "dup", "password": "password1", "role": "student"})
    input_func = make_input(["dup", "password1", "password1"])
    ok, msg = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert "already exists" in str(msg).lower()
