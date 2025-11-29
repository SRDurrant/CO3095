"""
Black-box testing for US31 - Global Input Validation.

These tests treat the validation functions as black-box utilities
and assert on observable behaviour.
"""

from app.validation import (
    validate_username_format,
    validate_password_format,
    validate_menu_option_format,
)


def test_username_empty_fails():
    is_valid, msg = validate_username_format("")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_username_too_short_fails():
    is_valid, msg = validate_username_format("ab")
    assert is_valid is False
    assert "at least 3 characters" in msg


def test_username_valid_passes():
    is_valid, msg = validate_username_format("alice")
    assert is_valid is True
    assert msg == "OK"


def test_password_empty_fails():
    is_valid, msg = validate_password_format("")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_password_too_short_fails():
    is_valid, msg = validate_password_format("123")
    assert is_valid is False
    assert "at least 8 characters" in msg


def test_password_valid_passes():
    is_valid, msg = validate_password_format("password123")
    assert is_valid is True
    assert msg == "OK"


def test_menu_option_valid():
    is_valid, msg = validate_menu_option_format("1", ["1", "2", "9", "0"])
    assert is_valid is True
    assert msg == "OK"


def test_menu_option_invalid():
    is_valid, msg = validate_menu_option_format("5", ["1", "2", "9", "0"])
    assert is_valid is False
    assert "Invalid option, please try again" in msg