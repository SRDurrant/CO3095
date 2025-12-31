from app.validation import (
    validate_username_format,
    validate_password_format,
    validate_rating_input,
)


def test_validate_username_min_length_boundary():
    ok, _ = validate_username_format("abc")
    assert ok is True


def test_validate_username_below_min_length_boundary():
    ok, msg = validate_username_format("ab")
    assert ok is False
    assert "at least 3" in msg.lower()


def test_validate_password_min_length_boundary():
    ok, _ = validate_password_format("12345678")
    assert ok is True


def test_validate_password_below_min_length_boundary():
    ok, msg = validate_password_format("1234567")
    assert ok is False
    assert "at least 8" in msg.lower()


def test_validate_rating_input_boundaries():
    assert validate_rating_input("1")[0] is True
    assert validate_rating_input("5")[0] is True
    assert validate_rating_input("0")[0] is False
    assert validate_rating_input("6")[0] is False
