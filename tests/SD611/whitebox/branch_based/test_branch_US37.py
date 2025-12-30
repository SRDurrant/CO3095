from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_branch_coverage(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    # Branch 1: no users
    view_top_contributors()
    out = capsys.readouterr().out
    assert "No registered users found." in out

    # Branch 2: users exist, no activity
    USERS.append({"user_id": 1, "username": "alice", "role": "student"})
    USERS.append({"user_id": 2, "username": "bob", "role": "student"})
    view_top_contributors()
    out = capsys.readouterr().out
    assert "No contributions yet." in out

    # Branch 3: users exist with activity
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 5})
    COMMENTS.append({"user_id": 2, "school_id": "1", "text": "Great"})
    view_top_contributors()
    out = capsys.readouterr().out
    assert "alice" in out
    assert "bob" in out