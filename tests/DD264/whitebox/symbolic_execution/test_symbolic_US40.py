from app.validation import validate_username_format, validate_password_format, validate_rating_input


def test_validation_symbolic_small_domain():
    usernames = ["", "  ", "ab", "abc", "abcd"]
    passwords = ["", "1234567", "12345678", " 12345678 "]
    ratings = [None, "", " ", "abc", "-1", "0", "1", "5", "6"]

    for u in usernames:
        ok, _ = validate_username_format(u)
        assert ok is (len(u.strip()) >= 3)

    for p in passwords:
        ok, _ = validate_password_format(p)
        assert ok is (len(p.strip()) >= 8)

    for r in ratings:
        ok, _ = validate_rating_input(r)
        if r is None:
            assert ok is False
        else:
            s = r.strip()
            if s == "":
                assert ok is False
            elif s.startswith("-") and s[1:].isdigit():
                assert ok is False
            elif not s.isdigit():
                assert ok is False
            else:
                v = int(s)
                assert ok is (1 <= v <= 5)
