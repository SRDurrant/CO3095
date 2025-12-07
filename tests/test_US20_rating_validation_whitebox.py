"""
White-box tests for US20 - Validate Rating Input.

These tests aim to cover the different internal branches of the
validate_rating_input function.
"""

from app.validation import validate_rating_input


def test_branch_none_input():
    """
    Branch: rating_value is None.
    """
    is_valid, msg = validate_rating_input(None)
    assert is_valid is False
    assert "empty" in msg


def test_branch_empty_after_strip():
    """
    Branch: rating_value becomes empty after stripping whitespace.
    """
    is_valid, msg = validate_rating_input("   ")
    assert is_valid is False
    assert "empty" in msg


def test_branch_negative_number_path():
    """
    Branch: input looks like a negative number (starts with '-'
    and the rest are digits).
    """
    is_valid, msg = validate_rating_input("-3")
    assert is_valid is False
    assert "negative" in msg


def test_branch_non_digit_path():
    """
    Branch: non-digit input that is not a valid negative integer.
    """
    is_valid, msg = validate_rating_input("3.5")
    assert is_valid is False
    assert "whole number" in msg


def test_branch_below_min_rating():
    """
    Branch: parsed integer is below min_rating.
    """
    is_valid, msg = validate_rating_input("0", min_rating=1, max_rating=5)
    assert is_valid is False
    assert "at least 1" in msg


def test_branch_above_max_rating():
    """
    Branch: parsed integer is above max_rating.
    """
    is_valid, msg = validate_rating_input("10", min_rating=1, max_rating=5)
    assert is_valid is False
    assert "at most 5" in msg


def test_branch_valid_path():
    """
    Branch: valid integer within [min_rating, max_rating].
    """
    is_valid, msg = validate_rating_input("4")
    assert is_valid is True
    assert msg == "OK"
