from app.school_actions import view_trending_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_trending_multiple_entries_loop():

    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    for i in range(3):
        SCHOOLS.append({"school_id": i, "name": f"S{i}"})
        RATINGS.append({"school_id": i})
        COMMENTS.append({"school_id": i})

    outputs = []
    view_trending_schools(print_func=lambda x: outputs.append(x))

    assert len([o for o in outputs if "Activity Score" in o]) == 3
