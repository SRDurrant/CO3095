import random
import string

from app.auth import register_user
from app.data_store import get_users


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def rand_username():
    n = random.randint(3, 12)
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


def rand_password():
    n = random.randint(8, 16)
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def test_register_multiple_random_users():
    created = set()

    for _ in range(20):
        u = rand_username()
        while u in created:
            u = rand_username()
        created.add(u)

        p = rand_password()
        input_func = make_input([u, p, p])
        ok, user = register_user(input_func=input_func, print_func=lambda *_: None)
        assert ok is True
        assert user["username"] == u

    assert len(get_users()) == 20
