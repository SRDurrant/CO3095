from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_no_users_blackbox(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    view_top_contributors(limit=5)
    out = capsys.readouterr().out
    assert "No registered users found." in out

def test_top_contributors_no_activity_blackbox(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({"user_id": 1, "username": "alice", "role": "student"})
    USERS.append({"user_id": 2, "username": "bob", "role": "student"})

    view_top_contributors(limit=5)
    out = capsys.readouterr().out
    assert "No contributions yet." in out