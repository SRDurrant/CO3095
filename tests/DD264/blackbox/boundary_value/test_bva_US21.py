from app.auth import register_user
from app.data_store import get_users


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def test_register_username_length_min_boundary():
    # username length 3 is allowed (boundary)
    input_func = make_input(["abc", "password1", "password1"])
    ok, user = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is True
    assert user["username"] == "abc"
    assert len(get_users()) == 1


def test_register_username_length_just_below_min_boundary():
    # username length 2 is rejected
    input_func = make_input(["ab", "password1", "password1"])
    ok, msg = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert "at least 3" in str(msg).lower()
    assert len(get_users()) == 0


def test_register_password_length_min_boundary():
    # password length 8 is allowed (boundary)
    input_func = make_input(["validuser", "12345678", "12345678"])
    ok, user = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is True
    assert user["password"] == "12345678"


def test_register_password_length_just_below_min_boundary():
    # password length 7 is rejected
    input_func = make_input(["validuser", "1234567", "1234567"])
    ok, msg = register_user(input_func=input_func, print_func=lambda *_: None)
    assert ok is False
    assert "at least 8" in str(msg).lower()
