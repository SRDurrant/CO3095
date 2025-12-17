"""
White-box tests for US29 - Save System Data to File (Branch-Based)

These tests directly exercise internal helpers and branches inside:
- serialize_comment()
- build_system_snapshot()
- save_system_data() error handling paths
"""

import os
from datetime import datetime, timezone

from app.persistence import serialize_comment, build_system_snapshot, save_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS


def reset_state():
    """
    Reset all global in-memory stores used by persistence.

    Inputs:
        None

    Outputs:
        None
    """
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()


def test_serialize_comment_branch_datetime_to_iso():
    """
    Tests the serialize_comment branch where created_at is a datetime and should be converted to ISO format.
    """
    comment = {
        "user_id": 1,
        "school_id": "1",
        "text": "hello",
        "created_at": datetime(2025, 12, 17, 12, 0, 0, tzinfo=timezone.utc),
    }

    out = serialize_comment(comment)

    assert isinstance(out["created_at"], str)
    assert out["created_at"].startswith("2025-12-17T12:00:00")


def test_serialize_comment_branch_none_preserved():
    """
    Tests the serialize_comment branch where created_at is None and should remain None.
    """
    comment = {"user_id": 1, "school_id": "1", "text": "hello", "created_at": None}

    out = serialize_comment(comment)

    assert "created_at" in out
    assert out["created_at"] is None


def test_serialize_comment_branch_other_type_stringified():
    """
    Tests the serialize_comment fallback branch where created_at is not datetime and not None, and should be stringified.
    """
    comment = {"user_id": 1, "school_id": "1", "text": "hello", "created_at": 12345}

    out = serialize_comment(comment)

    assert out["created_at"] == "12345"


def test_build_system_snapshot_includes_all_sections_and_serializes_comments():
    """
    Tests that build_system_snapshot collects users/schools/ratings/comments and serializes comment created_at values.
    """
    reset_state()

    USERS.append({"user_id": 1, "username": "u", "password": "password123", "role": "student"})
    SCHOOLS.append({"school_id": 1, "name": "S", "level": "primary", "location": "Edinburgh"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 5})
    COMMENTS.append(
        {
            "user_id": 1,
            "school_id": "1",
            "text": "hi",
            "created_at": datetime(2025, 12, 17, 12, 0, 0, tzinfo=timezone.utc),
        }
    )

    snap = build_system_snapshot()

    assert "users" in snap
    assert "schools" in snap
    assert "ratings" in snap
    assert "comments" in snap
    assert isinstance(snap["comments"][0]["created_at"], str)


def test_save_system_data_failure_branch_when_target_is_directory(tmp_path):
    """
    Tests the save_system_data exception branch by passing a directory path (open() should fail).
    """
    reset_state()

    bad_target = tmp_path / "not_a_file"
    os.makedirs(bad_target, exist_ok=True)

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = save_system_data(str(bad_target), print_func=fake_print)

    assert success is False
    assert any("Failed to save system state" in line for line in outputs)
