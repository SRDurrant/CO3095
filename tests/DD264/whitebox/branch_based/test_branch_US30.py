"""
White-box tests for US30 - Load System Data on Startup

These tests directly exercise internal branches within:
- deserialize_comment()
- load_system_data()

They ensure all key path behaviours are covered:
- datetime parsing success
- datetime parsing failure
- non-string created_at
- file missing branch
- invalid snapshot keys branch
"""

import json

from app.persistence import deserialize_comment, load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS


def reset_state():
    """
    Reset all global in-memory stores used by persistence
    """
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()


def write_snapshot(file_path, snapshot):
    """
    Writes a snapshot dictionary to a JSON file

    Inputs:
        file_path (str): Path where the JSON should be written
        snapshot (dict): Snapshot dictionary to write

    Outputs:
        None
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)


def test_deserialize_comment_branch_valid_iso_datetime():
    """
    Tests the deserialize_comment branch where created_at is a valid ISO string and is parsed successfully
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "2025-12-17T12:00:00+00:00"}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is not None
    assert restored["created_at"].isoformat().startswith("2025-12-17T12:00:00")


def test_deserialize_comment_branch_invalid_iso_datetime_sets_none():
    """
    Tests the deserialize_comment branch where created_at is a string but not ISO parseable, resulting in None
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": "invalid-date"}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is None


def test_deserialize_comment_branch_non_string_sets_none():
    """
    Tests the deserialize_comment branch where created_at is not a string, resulting in None
    """
    comment = {"user_id": 1, "school_id": "1", "text": "x", "created_at": 12345}

    restored = deserialize_comment(comment)

    assert restored["created_at"] is None


def test_load_system_data_branch_missing_file(tmp_path):
    """
    Tests the load_system_data branch where the file does not exist and load fails early
    """
    reset_state()

    missing = tmp_path / "missing.json"
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(str(missing), print_func=fake_print)

    assert success is False
    assert any("No saved system data found" in line for line in outputs)


def test_load_system_data_branch_invalid_snapshot_keys(tmp_path):
    """
    Tests the load_system_data branch where the snapshot is missing required keys and triggers failure
    """
    reset_state()

    file_path = tmp_path / "system_data.json"
    write_snapshot(str(file_path), {"users": [], "schools": []})

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(str(file_path), print_func=fake_print)

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)


def test_load_system_data_branch_success_restores_in_place(tmp_path):
    """
    Tests the successful branch of load_system_data restores data by clearing and extending globals
    """
    reset_state()

    # Pre-load junk data to confirm overwrite
    USERS.append({"user_id": 999, "username": "junk", "password": "password123", "role": "student"})

    file_path = tmp_path / "system_data.json"
    snapshot = {
        "users": [{"user_id": 1, "username": "u1", "password": "password123", "role": "student"}],
        "schools": [{"school_id": 1, "name": "S1", "level": "primary", "location": "Edinburgh"}],
        "ratings": [{"user_id": 1, "school_id": "1", "value": 4}],
        "comments": [{"user_id": 1, "school_id": "1", "text": "ok", "created_at": "2025-12-17T12:00:00+00:00"}],
    }
    write_snapshot(str(file_path), snapshot)

    success = load_system_data(str(file_path), print_func=lambda _: None)

    assert success is True
    assert len(USERS) == 1
    assert USERS[0]["user_id"] == 1
    assert len(SCHOOLS) == 1
    assert len(RATINGS) == 1
    assert len(COMMENTS) == 1
