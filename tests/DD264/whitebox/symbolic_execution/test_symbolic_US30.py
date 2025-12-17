"""
White-box tests for US30 - Load System Data on Startup

These tests intentionally select inputs that satisfy key path conditions in deserialize_comment:
- created_at is str AND parseable -> datetime branch
- created_at is str AND not parseable -> ValueError branch -> None
- created_at is not str -> None branch
"""

from app.persistence import deserialize_comment


def test_symbolic_path_created_at_str_parseable():
    """
    Path condition: isinstance(created_at, str) == True AND datetime.fromisoformat succeeds
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "2025-12-17T12:00:00+00:00"}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is not None


def test_symbolic_path_created_at_str_not_parseable():
    """
    Path condition: isinstance(created_at, str) == True AND datetime.fromisoformat raises ValueError
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "not-iso"}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is None


def test_symbolic_path_created_at_not_str():
    """
    Path condition: isinstance(created_at, str) == False -> created_at set to None
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": 123}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is None
