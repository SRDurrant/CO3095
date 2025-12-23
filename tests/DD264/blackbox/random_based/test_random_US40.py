"""
Black-box random-based testing for US40 - Auto-load and Auto-save

These tests randomly generate in-memory system state, then verify:
- save_system_data() succeeds
- load_system_data() restores the same counts after a clear
"""

import random
import string
from datetime import datetime, timezone, timedelta

from app.persistence import save_system_data, load_system_data
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS


def reset_system_state():
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()


def _rand_word(n=8):
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


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


def test_random_roundtrip_state_counts_preserved(tmp_path):
    """
    Random-based: generate random state -> save -> clear -> load -> compare counts
    """
    random.seed(123)
    reset_system_state()
    fp = tmp_path / "system_data.json"

    num_users = random.randint(1, 5)
    for i in range(1, num_users + 1):
        USERS.append(
            {
                "user_id": i,
                "username": _rand_word(6),
                "password": "x" * 8,
                "role": random.choice(["student", "admin"]),
            }
        )

    num_schools = random.randint(1, 5)
    for sid in range(1, num_schools + 1):
        SCHOOLS.append(
            {
                "school_id": sid,
                "name": f"{_rand_word(5)} School",
                "level": random.choice(["primary", "secondary", "combined"]),
                "location": _rand_word(4),
            }
        )

    for _ in range(random.randint(0, 10)):
        RATINGS.append(
            {
                "user_id": random.randint(1, num_users),
                "school_id": str(random.randint(1, num_schools)),
                "value": random.randint(1, 5),
            }
        )

    for _ in range(random.randint(0, 10)):
        dt = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365))
        COMMENTS.append(
            {
                "user_id": random.randint(1, num_users),
                "school_id": str(random.randint(1, num_schools)),
                "text": _rand_word(20),
                "created_at": dt,
            }
        )

    before_counts = (len(USERS), len(SCHOOLS), len(RATINGS), len(COMMENTS))

    save_ok, _ = run_save(str(fp))
    assert save_ok is True

    reset_system_state()

    load_ok, _ = run_load(str(fp))
    assert load_ok is True

    after_counts = (len(USERS), len(SCHOOLS), len(RATINGS), len(COMMENTS))
    assert after_counts == before_counts
