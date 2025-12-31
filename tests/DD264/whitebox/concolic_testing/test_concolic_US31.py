from app.validation import validate_rating_input


def test_rating_input_paths():
    # non-digit branch
    ok, msg = validate_rating_input("abc")
    assert ok is False
    assert "whole number" in msg.lower()

    # negative branch
    ok, msg = validate_rating_input("-1")
    assert ok is False
    assert "negative" in msg.lower()

    # below min branch
    ok, msg = validate_rating_input("0")
    assert ok is False
    assert "at least" in msg.lower()

    # above max branch
    ok, msg = validate_rating_input("6")
    assert ok is False
    assert "at most" in msg.lower()

    # ok branch
    ok, msg = validate_rating_input("5")
    assert ok is True
    assert msg == "OK"
