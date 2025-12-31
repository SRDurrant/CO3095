import json

from app.persistence import load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS, FAVOURITES


def test_load_system_data_missing_file_boundary(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    ok = load_system_data(file_path=str(missing), print_func=lambda *_: None)
    assert ok is False


def test_load_system_data_invalid_snapshot_keys_boundary(tmp_path):
    bad = tmp_path / "system.json"
    bad.write_text(json.dumps({"users": [], "schools": []}), encoding="utf-8")  # missing ratings/comments

    ok = load_system_data(file_path=str(bad), print_func=lambda *_: None)
    assert ok is False


def test_load_system_data_invalid_json_boundary(tmp_path):
    bad = tmp_path / "system.json"
    bad.write_text("{not valid json", encoding="utf-8")

    ok = load_system_data(file_path=str(bad), print_func=lambda *_: None)
    assert ok is False


def test_load_system_data_restores_favourites_optional_boundary(tmp_path):
    snap = {
        "users": [],
        "schools": [],
        "ratings": [],
        "comments": [],
        "favourites": [{"user_id": 1, "school_id": "2"}],
    }

    f = tmp_path / "system.json"
    f.write_text(json.dumps(snap), encoding="utf-8")

    ok = load_system_data(file_path=str(f), print_func=lambda *_: None)
    assert ok is True
    assert isinstance(FAVOURITES, list)
    assert len(FAVOURITES) == 1
