from app.reviews import RATINGS
from app.school_actions import _calculate_average_ratings


def test_average_rating_uneven_counts():

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "1", "value": 1},
        {"user_id": 3, "school_id": "2", "value": 4},
    ])

    avgs = _calculate_average_ratings()

    assert avgs["1"] == 3.0
    assert avgs["2"] == 4.0
