import random
import string

from app.validation import validate_username_format, validate_password_format


def test_username_validation_randomized():
    for _ in range(50):
        length = random.randint(0, 10)
        s = "".join(random.choice(string.ascii_letters) for _ in range(length))
        ok, _ = validate_username_format(s)

        if length >= 3:
            assert ok is True
        else:
            assert ok is False


def test_password_validation_randomized():
    for _ in range(50):
        length = random.randint(0, 12)
        s = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        ok, _ = validate_password_format(s)

        if length >= 8:
            assert ok is True
        else:
            assert ok is False
