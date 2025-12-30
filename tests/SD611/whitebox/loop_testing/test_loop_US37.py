from app.admin_actions import view_top_contributors
from app.data_store import USERS
from app.reviews import RATINGS, COMMENTS


def test_top_contributors_looping(capsys):
    USERS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    for i in range(3):
        USERS.append({"user_id": i, "username": f"user{i}", "role": "student"})
        RATINGS.append({"user_id": i, "school_id": str(i), "value": 5})
        COMMENTS.append({"user_id": i, "school_id": str(i), "text": "Nice"})

    view_top_contributors(limit=5)
    out = capsys.readouterr().out
    assert "user0" in out and "user1" in out and "user2" in out