import random
import string

from app.auth import login_user
from app.data_store import add_user, clear_current_user, get_current_user


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def rand_password():
    n = random.randint(8, 16)
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def test_login_random_passwords_success():
    pw = rand_password()
    add_user({"user_id": 1, "username": "userA", "password": pw, "role": "student"})
    clear_current_user()

    input_func = make_input(["userA", pw])
    ok, user = login_user(input_func=input_func, print_func=lambda *_: None)

    assert ok is True
    assert user["username"] == "userA"
    assert get_current_user()["username"] == "userA"
