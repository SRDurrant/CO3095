"""
White-box tests for US29 - Save System Data to File (Concolic Testing Style)

These tests use concrete executions designed to drive multiple distinct paths in serialize_comment().
"""

from datetime import datetime, timezone

from app.persistence import serialize_comment


def test_concolic_run_drives_datetime_then_other_path():
    """
    Drives two different paths in serialize_comment using concrete inputs:
    - datetime branch
    - fallback stringification branch
    """
    comment_1 = {
        "user_id": 1,
        "school_id": "1",
        "text": "x",
        "created_at": datetime(2025, 12, 17, 10, 0, 0, tzinfo=timezone.utc),
    }
    out_1 = serialize_comment(comment_1)
    assert out_1["created_at"].startswith("2025-12-17T10:00:00")

    comment_2 = {"user_id": 1, "school_id": "1", "text": "x", "created_at": 999}
    out_2 = serialize_comment(comment_2)
    assert out_2["created_at"] == "999"


def test_concolic_run_drives_none_path():
    """
    Drives the created_at == None path in serialize_comment using a concrete input.
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": None}

    out = serialize_comment(comment)

    assert out["created_at"] is None
