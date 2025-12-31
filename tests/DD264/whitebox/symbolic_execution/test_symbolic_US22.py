from app.auth import register_user
from app.data_store import get_users


def make_input(seq):
    it = iter(seq)
    return lambda _prompt="": next(it)


def test_register_symbolic_small_domain_exhaustive():
    # small domain: usernames of lengths 0..3, password lengths 7..8, confirm match/mismatch
    usernames = ["", "a", "ab", "abc"]
    passwords = ["1234567", "12345678"]
    confirms = ["1234567", "12345678", "mismatch"]

    for u in usernames:
        for p in passwords:
            for c in confirms:
                # reset state each attempt
                get_users().clear()

                input_func = make_input([u, p, c])
                ok, _ = register_user(input_func=input_func, print_func=lambda *_: None)

                # expected constraints:
                # username must be >=3 and password >=8 and confirm must match
                expect = (len(u.strip()) >= 3) and (len(p.strip()) >= 8) and (p == c)
                assert ok is expect
