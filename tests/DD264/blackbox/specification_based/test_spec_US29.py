"""
Black-box tests for US29 - Save System Data to File

These tests treat save_system_data as a black-box persistence function and
verify observable behaviour:
- Returns True/False correctly
- Writes a JSON file on success
- Produces expected top-level structure
- Serializes datetime into a JSON-safe format
"""

import json
from datetime import datetime, timezone

from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS
from app.persistence import save_system_data


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


def test_save_creates_file_and_returns_true(tmp_path):
    """
    Tests that save_system_data returns True and creates the output file when the
    system contains valid data.
    """
    reset_state()

    USERS.append({"user_id": 1, "username": "admin-user", "password": "admin123", "role": "admin"})
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "Edinburgh"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 5})
    COMMENTS.append(
        {
            "user_id": 1,
            "school_id": "1",
            "text": "Great school",
            "created_at": datetime(2025, 12, 17, 12, 0, 0, tzinfo=timezone.utc),
        }
    )

    out_file = tmp_path / "system_data.json"
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = save_system_data(str(out_file), print_func=fake_print)

    assert success is True
    assert out_file.exists()
    assert any("System data saved successfully" in line for line in outputs)


def test_saved_json_contains_required_top_level_keys(tmp_path):
    """
    Tests that the output file contains the required top-level keys:
    users, schools, ratings, comments.
    """
    reset_state()

    USERS.append({"user_id": 2, "username": "student-user", "password": "student456", "role": "student"})

    out_file = tmp_path / "system_data.json"

    success = save_system_data(str(out_file), print_func=lambda _: None)

    assert success is True

    payload = json.loads(out_file.read_text(encoding="utf-8"))
    assert "users" in payload
    assert "schools" in payload
    assert "ratings" in payload
    assert "comments" in payload


def test_comment_created_at_is_serialized_to_string(tmp_path):
    """
    Tests that when a comment contains a datetime created_at field, it is persisted as
    a JSON-safe string (ISO format).
    """
    reset_state()

    COMMENTS.append(
        {
            "user_id": 3,
            "school_id": "99",
            "text": "Test comment",
            "created_at": datetime(2025, 12, 17, 12, 30, 0, tzinfo=timezone.utc),
        }
    )

    out_file = tmp_path / "system_data.json"

    success = save_system_data(str(out_file), print_func=lambda _: None)

    assert success is True

    payload = json.loads(out_file.read_text(encoding="utf-8"))
    assert len(payload["comments"]) == 1
    assert isinstance(payload["comments"][0]["created_at"], str)
    assert payload["comments"][0]["created_at"].startswith("2025-12-17T12:30:00")
