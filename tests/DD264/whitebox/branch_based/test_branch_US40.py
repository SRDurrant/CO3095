"""
White-box branch-based testing for US40 - Auto-load and Auto-save

These tests are designed to hit key branches in persistence.py:
- load: file missing / invalid JSON / missing keys / success
- save: success / exception path
"""

import json
import builtins

from app.persistence import load_system_data, save_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS


def reset_system_state():
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()


def run_load(file_path: str):
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(file_path=file_path, print_func=fake_print)
    return success, outputs


def run_save(file_path: str):
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = save_system_data(file_path=file_path, print_func=fake_print)
    return success, outputs


def test_branch_load_missing_file(tmp_path):
    """
    Branch: load -> file does not exist
    """
    reset_system_state()
    fp = tmp_path / "missing.json"

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("No saved system data found" in line for line in outputs)


def test_branch_load_invalid_json(tmp_path):
    """
    Branch: load -> json.load throws exception
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"
    fp.write_text("{invalid json", encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)


def test_branch_load_missing_keys(tmp_path):
    """
    Branch: load -> missing required keys triggers ValueError
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"
    fp.write_text(json.dumps({"users": []}), encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is False
    assert any("Failed to load system data" in line for line in outputs)


def test_branch_load_success(tmp_path):
    """
    Branch: load -> success path
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"
    fp.write_text(json.dumps({"users": [], "schools": [], "ratings": [], "comments": []}), encoding="utf-8")

    success, outputs = run_load(str(fp))

    assert success is True
    assert any("System data loaded successfully" in line for line in outputs)


def test_branch_save_success(tmp_path):
    """
    Branch: save -> success path
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    success, outputs = run_save(str(fp))

    assert success is True
    assert fp.exists()
    assert any("System data saved successfully" in line for line in outputs)


def test_branch_save_failure(monkeypatch, tmp_path):
    """
    Branch: save -> exception path (open fails)
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
