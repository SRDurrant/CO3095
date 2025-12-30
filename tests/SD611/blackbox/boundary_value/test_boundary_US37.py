from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_limit_exceeds_users_blackbox(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({"user_id": 1, "username": "alice", "role": "student"})
    USERS.append({"user_id": 2, "username": "bob", "role": "student"})

    view_top_contributors(limit=10)
    out = capsys.readouterr().out
    assert "alice" in out
    assert "bob" in out