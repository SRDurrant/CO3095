"""
White-box tests for US30 - Load System Data on Startup

These tests use concrete executions designed to traverse multiple paths in deserialize_comment:
- Valid ISO string -> datetime path
- Invalid ISO string -> error handling path -> None
- Non-string -> None path
"""

from app.persistence import deserialize_comment


def test_concolic_drives_valid_then_invalid_then_non_string_paths():
    """
    Executes deserialize_comment three times with different concrete inputs to traverse distinct paths
    """

    # Path 1: valid ISO string
    c1 = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "2025-12-17T12:00:00+00:00"}
    out1 = deserialize_comment(c1)
    assert out1["created_at"] is not None

    # Path 2: invalid ISO string
    c2 = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "invalid"}
    out2 = deserialize_comment(c2)
    assert out2["created_at"] is None

    # Path 3: non-string created_at
    c3 = {"user_id": 1, "school_id": "1", "text": "x", "created_at": 999}
    out3 = deserialize_comment(c3)
    assert out3["created_at"] is None
