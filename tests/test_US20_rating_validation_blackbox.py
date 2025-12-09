"""
Black-box tests for US20 - Validate Rating Input.

These tests treat validate_rating_input as a black-box function and
check observable behaviour only.
"""

from app.validation import validate_rating_input


def test_rating_valid_middle_of_range():
    """
    A typical valid rating within the allowed range passes.
    """
    is_valid, msg = validate_rating_input("3")
    assert is_valid is True
    assert msg == "OK"


def test_rating_valid_minimum_boundary():
    """
    Boundary: minimum allowed rating (1) should be accepted.
    """
    is_valid, msg = validate_rating_input("1")
    assert is_valid is True
    assert msg == "OK"


def test_rating_valid_maximum_boundary():
    """
    Boundary: maximum allowed rating (5) should be accepted.
    """
    is_valid, msg = validate_rating_input("5")
    assert is_valid is True
    assert msg == "OK"


def test_rating_empty_string_fails():
    """
    Empty string should be rejected.
    """
    is_valid, msg = validate_rating_input("")
    assert is_valid is False
    assert "empty" in msg


def test_rating_whitespace_only_fails():
    """
    Whitespace-only input should be rejected.
    """
    is_valid, msg = validate_rating_input("   ")
    assert is_valid is False
    assert "empty" in msg


def test_rating_non_numeric_fails():
    """
    Completely non-numeric input should be rejected.
    """
    is_valid, msg = validate_rating_input("abc")
    assert is_valid is False
    assert "whole number" in msg


def test_rating_negative_number_fails():
    """
    Negative numbers should be rejected with a specific message.
    """
    is_valid, msg = validate_rating_input("-1")
    assert is_valid is False
    assert "negative" in msg


def test_rating_below_minimum_fails():
    """
    0 is below the allowed minimum (1) and should fail.
    """
    is_valid, msg = validate_rating_input("0")
    assert is_valid is False
    assert "at least 1" in msg


def test_rating_above_maximum_fails():
    """
    Ratings above the maximum (5) should fail.
    """
    is_valid, msg = validate_rating_input("6")
    assert is_valid is False
    assert "at most 5" in msg
