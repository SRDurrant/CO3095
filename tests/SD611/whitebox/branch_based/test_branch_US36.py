from app.school_actions import view_trending_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_trending_no_activity():

    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Idle"})

    outputs = []
    view_trending_schools(print_func=lambda x: outputs.append(x))

    assert "No recent activity" in outputs[-1]