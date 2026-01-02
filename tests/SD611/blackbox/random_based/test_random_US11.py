import random
from app.school_actions import view_school_rankings
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_view_school_rankings_random_ratings_blackbox(capsys):

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(5):
        SCHOOLS.append({
            "school_id": i,
            "name": f"School{i}",
            "level": "primary",
        })
        RATINGS.append({
            "user_id": i,
            "school_id": str(i),
            "value": random.randint(1, 5),
        })

    view_school_rankings()
    out = capsys.readouterr().out

    # We don't assert exact order, only that all schools appear
    for i in range(5):
        assert f"School{i}" in out