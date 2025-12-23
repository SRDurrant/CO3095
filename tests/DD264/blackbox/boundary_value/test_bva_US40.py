"""
Black-box boundary value testing for US40 - Auto-load and Auto-save

These tests target edge/boundary cases:
- Saving into nested directories
- Comments with boundary created_at values
"""

import json

from app.persistence import save_system_data, load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS


def reset_system_state():
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()


def run_save(file_path: str):
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = save_system_data(file_path=file_path, print_func=fake_print)
    return success, outputs


def run_load(file_path: str):
    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = load_system_data(file_path=file_path, print_func=fake_print)
    return success, outputs


def test_boundary_save_to_nested_directory(tmp_path):
    """
    Boundary: file_path includes nested parent directories
    save_system_data should create directories and succeed
    """
    reset_system_state()
    fp = tmp_path / "a" / "b" / "system_data.json"

    success, outputs = run_save(str(fp))

    assert success is True
    assert fp.exists()
    assert any("System data saved successfully" in line for line in outputs)


def test_boundary_comment_created_at_none_roundtrip(tmp_path):
    """
    Boundary: COMMENTS entry has created_at = None
    Save + load should not crash, and created_at should remain None
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    USERS.append({"user_id": 1, "username": "u", "password": "x" * 8, "role": "student"})
    COMMENTS.append({"user_id": 1, "school_id": "1", "text": "Edge", "created_at": None})

    save_ok, _ = run_save(str(fp))
    assert save_ok is True

    reset_system_state()

    load_ok, _ = run_load(str(fp))
    assert load_ok is True

    assert len(COMMENTS) == 1
    assert COMMENTS[0]["created_at"] is None


def test_boundary_comment_created_at_invalid_string_sets_none(tmp_path):
    """
    Boundary: snapshot contains invalid created_at string
    load_system_data should set created_at to None
    """
    reset_system_state()
    fp = tmp_path / "system_data.json"

    snapshot = {
        "users": [],
        "schools": [],
        "ratings": [],
        "comments": [{"user_id": 1, "school_id": "1", "text": "Bad date", "created_at": "not-a-date"}],
    }
    fp.write_text(json.dumps(snapshot), encoding="utf-8")

    load_ok, outputs = run_load(str(fp))

    assert load_ok is True
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["created_at"] is None
    assert any("System data loaded successfully" in line for line in outputs)
