"""
White-box tests for US31 - Global Input Validation.

These tests directly exercise branches inside:
- validate_username_format
- validate_password_format
- validate_menu_option_format
"""

from app.validation import (
    validate_username_format,
    validate_password_format,
    validate_menu_option_format,
)


def test_username_branch_empty():
    is_valid, msg = validate_username_format("   ")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_username_branch_min_length():
    is_valid, msg = validate_username_format("ab")
    assert is_valid is False
    assert "at least 3 characters" in msg


def test_username_branch_ok():
    is_valid, msg = validate_username_format("bob")
    assert is_valid is True
    assert msg == "OK"


def test_password_branch_empty():
    is_valid, msg = validate_password_format("")
    assert is_valid is False
    assert "cannot be empty" in msg


def test_password_branch_too_short():
    is_valid, msg = validate_password_format("12345")
    assert is_valid is False
    assert "at least 8 characters" in msg


def test_password_branch_ok():
    is_valid, msg = validate_password_format("securepwd")
    assert is_valid is True
    assert msg == "OK"


def test_menu_branch_valid():
    is_valid, msg = validate_menu_option_format("9", ["1", "2", "9", "0"])
    assert is_valid is True
    assert msg == "OK"


def test_menu_branch_invalid():
    is_valid, msg = validate_menu_option_format("x", ["1", "2", "9", "0"])
    assert is_valid is False
    assert "Invalid option, please try again" in msg