from app.school_actions import _calculate_average_ratings
from app.reviews import RATINGS

def test_average_rating_concolic():

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "1", "value": 3},
        {"user_id": 3, "school_id": "2", "value": 4},
    ])

    avgs = _calculate_average_ratings()

    # Path 1: aggregation
    assert avgs["1"] == 4.0
    # Path 2: single entry
    assert avgs["2"] == 4.0