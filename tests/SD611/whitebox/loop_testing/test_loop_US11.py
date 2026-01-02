from app.reviews import RATINGS
from app.school_actions import _calculate_average_ratings


def test_average_rating_multiple_schools():

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "2", "value": 3},
    ])

    avgs = _calculate_average_ratings()

    assert avgs["1"] == 5.0
    assert avgs["2"] == 3.0