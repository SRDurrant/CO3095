import random

from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_random_activity_blackbox(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    for i in range(10):
        USERS.append({"user_id": i, "username": f"user{i}", "role": "student"})
        RATINGS.append({"user_id": i, "school_id": str(i), "value": random.randint(1, 5)})
        COMMENTS.append({"user_id": i, "school_id": str(i), "text": "Good"})

    view_top_contributors(limit=5)
    out = capsys.readouterr().out
    assert "user" in out  # At least one user printed