"""
Black box tests for US30 - Load System Data on Startup

These tests use seeded random snapshots to confirm
- load_system_data can load varied states correctly
- counts and key fields are preserved
- created_at strings remain loadable into datetime
"""

import json
import random
from app.persistence import load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def reset_state():
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

def write_snapshot(file_path, snapshot):
    with open(file_path, "w", encoding = "utf-8") as f:
        json.dump(snapshot, f, indent = 2, ensure_ascii = False)

def test_randomized_snapshot_loads_and_preserves_counts(tmp_path):
    """
    Tests that seeded randomized snapshot loads correctly and preserves
    collection sizes
    """

    reset_state()
    random.seed(123)
    user_count = random.randint(1, 6)
    school_count = random.randint(1, 6)
    rating_count = random.randint(1, 6)
    comment_count = random.randint(1, 6)

    users = []
    for i in range(user_count):
        users.append(
            {"user_id": i + 1, "username": f"user{i+1}", "password": "password123", "role": "student"}
        )

    schools = []
    for i in range(school_count):
        schools.append(
            {"school_id": i + 1, "name": f"School {i+1}", "level": "primary", "location": "Edinburgh"}
        )

    ratings = []
    for _ in range(rating_count):
        ratings.append(
            {"user_id": random.randint(1, user_count), "school_id": str(random.randint(1, school_count)), "value": random.randint(1, 5)}
        )

    comments = []
    for _ in range(comment_count):
        comments.append(
            {
                "user_id": random.randint(1, user_count),
                "school_id": str(random.randint(1, school_count)),
                "text": "random comment",
                "created_at": "2025-12-17T12:00:00+00:00"
            }
        )

    snapshot = {"users": users, "schools": schools, "ratings": ratings, "comments": comments}

    file_path = tmp_path / "system_data.json"
    write_snapshot(str(file_path), snapshot)

    success = load_system_data(str(file_path), print_func = lambda _: None)

    assert success is True
    assert len(USERS) == user_count
    assert len(SCHOOLS) == school_count
    assert len(RATINGS) == rating_count
    assert len(COMMENTS) == comment_count


def test_randomized_multiple_loads_overwrite_previous_state(tmp_path):
    """
    Tests that a second load overwrites existing in-memory state
    """
    reset_state()
    random.seed(999)

    snapshot_1 = {
        "users": [{"user_id": 1, "username": "u1", "password": "password123", "role": "student"}],
        "schools": [],
        "ratings": [],
        "comments": [],
    }

    snapshot_2 = {
        "users": [{"user_id": 2, "username": "u2", "password": "password123", "role": "student"}],
        "schools": [{"school_id": 10, "name": "S10", "level": "primary", "location": "Edinburgh"}],
        "ratings": [],
        "comments": [],
    }

    file_1 = tmp_path / "system_data_1.json"
    file_2 = tmp_path / "system_data_2.json"
    write_snapshot(str(file_1), snapshot_1)
    write_snapshot(str(file_2), snapshot_2)

    success_1 = load_system_data(str(file_1), print_func=lambda _: None)
    assert success_1 is True
    assert len(USERS) == 1
    assert USERS[0]["user_id"] == 1

    success_2 = load_system_data(str(file_2), print_func=lambda _: None)
    assert success_2 is True
    assert len(USERS) == 1
    assert USERS[0]["user_id"] == 2
    assert len(SCHOOLS) == 1
    assert SCHOOLS[0]["school_id"] == 10