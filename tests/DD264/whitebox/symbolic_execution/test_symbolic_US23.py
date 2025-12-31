import builtins
from app.auth import login_user
from app.data_store import add_user, clear_current_user, get_current_user


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def test_login_symbolic_cases():
    add_user({"user_id": 1, "username": "u", "password": "password1", "role": "student"})
    clear_current_user()

    cases = [
        (["0"], False),                       # cancel at username
        (["unknown", "0"], False),            # not found then cancel
        (["u", "0"], False),                  # cancel at password
        (["u", "wrong", "0"], False),         # wrong pw then cancel at username on next loop
        (["u", "password1"], True),           # success
    ]

    for seq, expected_ok in cases:
        clear_current_user()
        input_func = make_input(seq)
        ok, _ = login_user(input_func=input_func, print_func=lambda *_: None)
        assert ok is expected_ok
        if expected_ok:
            assert get_current_user() is not None
        else:
            assert get_current_user() is None
