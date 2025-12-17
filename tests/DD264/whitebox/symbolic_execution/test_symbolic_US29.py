"""
White-box tests for US29 - Save System Data to File (Symbolic Execution Style)

These tests select inputs that satisfy specific path conditions in serialize_comment():
- created_at is datetime
- created_at is None
- created_at is neither datetime nor None
"""

from datetime import datetime, timezone

from app.persistence import serialize_comment


def test_symbolic_path_created_at_is_datetime():
    """
    Path condition: isinstance(created_at, datetime) == True
    """
    comment = {
        "user_id": 1,
        "school_id": "1",
        "text": "x",
        "created_at": datetime(2025, 12, 17, 1, 2, 3, tzinfo=timezone.utc),
    }

    out = serialize_comment(comment)

    assert out["created_at"].startswith("2025-12-17T01:02:03")


def test_symbolic_path_created_at_is_none():
    """
    Path condition: created_at is None
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": None}

    out = serialize_comment(comment)

    assert out["created_at"] is None


def test_symbolic_path_created_at_is_other_type():
    """
    Path condition: created_at is not datetime AND created_at is not None
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": {"a": 1}}

    out = serialize_comment(comment)

    assert out["created_at"] == "{'a': 1}"
