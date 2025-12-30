from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_limit_exceeds_users_blackbox():
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({"user_id": 1, "username": "alice", "role": "student"})
    USERS.append({"user_id": 2, "username": "bob", "role": "student"})

    COMMENTS.append({"user_id": 1, "school_id": "1", "text": "Hi", "created_at": None})
    RATINGS.append({"user_id": 2, "school_id": "1", "value": 5})

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    view_top_contributors(limit=10, print_func=fake_print)

    combined = "\n".join(outputs)
    assert "alice" in combined
    assert "bob" in combined
