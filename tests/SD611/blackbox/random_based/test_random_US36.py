import random
from app.school_actions import view_trending_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_trending_random_activity(capsys):

    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    for i in range(5):
        SCHOOLS.append({"school_id": i, "name": f"S{i}"})
        for _ in range(random.randint(0, 10)):
            RATINGS.append({"school_id": i})

    view_trending_schools()