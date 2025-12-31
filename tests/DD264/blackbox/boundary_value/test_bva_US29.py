import os
import json
from datetime import datetime, timezone

from app.persistence import save_system_data, build_system_snapshot, serialize_comment
from app.reviews import COMMENTS


def test_save_system_data_creates_parent_dir_boundary(tmp_path):
    target_dir = tmp_path / "nested" / "dir"
    target_file = target_dir / "system_data.json"

    ok = save_system_data(file_path=str(target_file), print_func=lambda *_: None)
    assert ok is True
    assert target_file.exists()

    data = json.loads(target_file.read_text(encoding="utf-8"))
    assert "users" in data and "schools" in data


def test_serialize_comment_created_at_none_boundary():
    c = {"user_id": 1, "school_id": "1", "text": "x", "created_at": None}
    out = serialize_comment(c)
    assert "created_at" in out
    assert out["created_at"] is None


def test_serialize_comment_created_at_datetime_boundary():
    dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
    c = {"user_id": 1, "school_id": "1", "text": "x", "created_at": dt}
    out = serialize_comment(c)
    assert out["created_at"].startswith("2025-01-01")
