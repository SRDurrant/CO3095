"""
Black-box testing for US40 - Auto-load and Auto-save

These tests validate US40 behaviour via the persistence interface:
- load_system_data() should safely handle missing/invalid files
- save_system_data() should create/update the JSON file
- failures should not crash the system and should print appropriate messages
"""

import json
import builtins

from app.persistence import load_system_data, save_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def reset_system_state():
    """
    Resets the global in-memory state for isolation between tests
    """

    USERS.clear()
    SCHOOLS.clear()
    COMMENTS.clear()
    RATINGS.clear()


def run_load(file_path: str):
    """
    Simulates a load flow for US40

    Inputs:
    file_path: path to load the system state from

    Returns:
        tuple:
            - Success (bool): True if load is successful, False otherwise
            - Outputs (list[str]): List of printed messages during load
    """

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(file_path = file_path, print_func = fake_print)
    return success, outputs


def run_save(file_path: str):
    """Simulates a save flow for US40

    Inputs:
        file_path: path to save the system state to

    Returns:
        tuple:
        - Success (bool): True if save is successful, False otherwise
        - Outputs (list[str]): List of printed messages during save
        """

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = save_system_data(file_path = file_path, print_func = fake_print)
    return success, outputs

def test_autoload_missing_file_no_crash(tmp_path):
    """
    Auto-load should handle missing file safely
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("No saved system data found" in line for line in outputs)

def test_autoload_invalid_json_no_crash(tmp_path):
    """
    Auto-load should handle invalid JSON safely
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"
    fp.write_text("{invalid json", encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)

def test_autoload_missing_keys_no_crash(tmp_path):
    """
    Auto-load should reject snapshots missing required keys
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"
    fp.write_text(json.dumps({"users": []}), encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)

def test_autoload_valid_snapshot_restores_state(tmp_path):
    """
    Auto-load should restore state from a valid snapshot
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    snapshot = {
        "users": [{"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"}],
        "schools": [{"school_id": 1, "name": "Alpha School", "level": "primary", "location": "Town"}],
        "ratings": [{"user_id": 1, "school_id": "1", "value": 5}],
        "comments": [{"user_id": 1, "school_id": "1", "text": "Good", "created_at": "2025-01-01T00:00:00+00:00"}],
    }
    fp.write_text(json.dumps(snapshot), encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is True
    assert len(USERS) == 1
    assert len(SCHOOLS) == 1
    assert len(RATINGS) == 1
    assert len(COMMENTS) == 1
    assert any("System data loaded successfully" in line for line in outputs)

def test_autosave_creates_file(tmp_path):
    """
    Auto-save should create the JSON file and return True
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    USERS.append({"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"})

    success, outputs = run_save(str(fp))

    assert success is True
    assert fp.exists()
    assert any("System data saved successfully" in line for line in outputs)

def test_autosave_failure_returns_false(monkeypatch, tmp_path):
    """
    Auto-save should fail safely if writing fails
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    real_open = builtins.open

    def bad_open(*args, **kwargs):
        raise OSError("cannot write")

    monkeypatch.setattr(builtins, "open", bad_open)
    try:
        success, outputs = run_save(str(fp))
        assert success is False
        assert any("Failed to save system state" in line for line in outputs)
    finally:
        monkeypatch.setattr(builtins, "open", real_open)