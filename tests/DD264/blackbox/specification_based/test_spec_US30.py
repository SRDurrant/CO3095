"""
Blackbox tests for US30 - Load System Data on Startup

These tests treat load_system_data as a black-box function and validate the behaviour
- Correct return values
- Correct messaging via print_func
- Correct restoration of global in-memory state
- Correct handling of missing files and invalid snapshot formats
"""

import json
from datetime import datetime, timezone
from app.persistence import load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def reset_state():
    """
    Resets all the global in-memory stores used by persistence
    """

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

def write_snapshot(file_path, snapshot):
    """
    Writes a snapshot dictionary to a JSON file

    Inputs:
        file_path: Path to the JSON file
        snapshot: Snapshot dictionary

    Outputs:
        None
    """

    with open(file_path, 'w', encoding = "utf-8") as f:
        json.dump(snapshot, f, indent = 2, ensure_ascii = False)


def test_load_returns_false_when_file_missing(tmp_path):
    """
    Tests that load_system_data returns False and prints a message when the target file does not exist.
    """
    reset_state()

    missing = tmp_path / "does_not_exist.json"
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(str(missing), print_func=fake_print)

    assert success is False
    assert any("No saved system data found" in line for line in outputs)


def test_load_returns_false_when_json_invalid(tmp_path):
    """
    Tests that load_system_data returns False when the file exists but contains invalid JSON.
    """
    reset_state()

    bad_file = tmp_path / "system_data.json"
    bad_file.write_text("{not valid json", encoding="utf-8")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(str(bad_file), print_func=fake_print)

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)


def test_load_returns_false_when_snapshot_missing_keys(tmp_path):
    """
    Tests that load_system_data returns False when JSON is valid but missing required snapshot keys.
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


def test_load_restores_all_collections_on_success(tmp_path):
    """
    Tests that load_system_data returns True and restores USERS, SCHOOLS, RATINGS, COMMENTS on success.
    """
    reset_state()

    file_path = tmp_path / "system_data.json"
    snapshot = {
        "users": [{"user_id": 1, "username": "u1", "password": "password123", "role": "student"}],
        "schools": [{"school_id": 1, "name": "School A", "level": "primary", "location": "Edinburgh"}],
        "ratings": [{"user_id": 1, "school_id": "1", "value": 5}],
        "comments": [
            {
                "user_id": 1,
                "school_id": "1",
                "text": "Nice",
                "created_at": "2025-12-17T12:00:00+00:00"
            }
        ],
    }
    write_snapshot(str(file_path), snapshot)

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(str(file_path), print_func=fake_print)

    assert success is True
    assert any("System data loaded successfully" in line for line in outputs)

    assert len(USERS) == 1
    assert len(SCHOOLS) == 1
    assert len(RATINGS) == 1
    assert len(COMMENTS) == 1


def test_load_restores_comment_created_at_as_datetime(tmp_path):
    """
    Tests that a valid ISO created_at string is restored into a datetime object in COMMENTS.
    """
    reset_state()

    file_path = tmp_path / "system_data.json"
    snapshot = {
        "users": [],
        "schools": [],
        "ratings": [],
        "comments": [
            {
                "user_id": 2,
                "school_id": "7",
                "text": "Test comment",
                "created_at": "2025-12-17T12:30:00+00:00",
            }
        ],
    }
    write_snapshot(str(file_path), snapshot)

    success = load_system_data(str(file_path), print_func=lambda _: None)

    assert success is True
    assert isinstance(COMMENTS[0]["created_at"], datetime)
    assert COMMENTS[0]["created_at"].isoformat().startswith("2025-12-17T12:30:00")


def test_load_invalid_created_at_results_in_none(tmp_path):
    """
    Tests that an invalid created_at string results in created_at being set to None after loading.
    """
    reset_state()

    file_path = tmp_path / "system_data.json"
    snapshot = {
        "users": [],
        "schools": [],
        "ratings": [],
        "comments": [
            {
                "user_id": 3,
                "school_id": "9",
                "text": "Bad timestamp",
                "created_at": "not-an-iso-datetime",
            }
        ],
    }
    write_snapshot(str(file_path), snapshot)

    success = load_system_data(str(file_path), print_func=lambda _: None)

    assert success is True
    assert COMMENTS[0]["created_at"] is None


def test_load_does_not_require_non_empty_lists(tmp_path):
    """
    Tests that load_system_data succeeds even when all collections are empty lists.
    """
    reset_state()

    file_path = tmp_path / "system_data.json"
    snapshot = {"users": [], "schools": [], "ratings": [], "comments": []}
    write_snapshot(str(file_path), snapshot)

    success = load_system_data(str(file_path), print_func=lambda _: None)

    assert success is True
    assert USERS == []
    assert SCHOOLS == []
    assert RATINGS == []
    assert COMMENTS == []