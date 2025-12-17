"""
Black-box tests for US29 - Save System Data to File (Random-Based)

These tests use seeded randomized inputs to verify the persistence function can
handle varied system states while still producing valid JSON output.
"""

import json
import random
import string
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


def rand_text(n: int) -> str:
    """
    Generates random text for comment bodies.

    Inputs:
        n (int): length of string

    Outputs:
        str: random string (non-empty)
    """
    text = "".join(random.choice(string.ascii_letters + string.digits + " ") for _ in range(n)).strip()
    return text if text else "x"


def test_randomized_snapshot_saves_valid_json(tmp_path):
    """
    Tests that a randomized (but seeded) system state can be saved successfully,
    and the saved JSON preserves counts for users, schools, ratings, and comments.
    """
    reset_state()
    random.seed(42)

    user_count = random.randint(1, 5)
    school_count = random.randint(1, 5)
    rating_count = random.randint(1, 5)
    comment_count = random.randint(1, 5)

    for i in range(user_count):
        USERS.append(
            {
                "user_id": i + 1,
                "username": f"user{i + 1}",
                "password": "password123",
                "role": "student",
            }
        )

    for i in range(school_count):
        SCHOOLS.append(
            {
                "school_id": i + 1,
                "name": f"School {i + 1}",
                "level": random.choice(["primary", "secondary", "combined"]),
                "location": random.choice(["Edinburgh", "Glasgow", "Dundee"]),
            }
        )

    for _ in range(rating_count):
        RATINGS.append(
            {
                "user_id": random.randint(1, user_count),
                "school_id": str(random.randint(1, max(1, school_count))),
                "value": random.randint(1, 5),
            }
        )

    for _ in range(comment_count):
        COMMENTS.append(
            {
                "user_id": random.randint(1, user_count),
                "school_id": str(random.randint(1, max(1, school_count))),
                "text": rand_text(random.randint(5, 50)),
                "created_at": datetime(2025, 12, 17, 12, 0, 0, tzinfo=timezone.utc),
            }
        )

    out_file = tmp_path / "system_data.json"

    success = save_system_data(str(out_file), print_func=lambda _: None)

    assert success is True

    payload = json.loads(out_file.read_text(encoding="utf-8"))
    assert len(payload["users"]) == user_count
    assert len(payload["schools"]) == school_count
    assert len(payload["ratings"]) == rating_count
    assert len(payload["comments"]) == comment_count
