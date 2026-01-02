from app.school_actions import _calculate_average_ratings
from app.reviews import RATINGS

def test_average_rating_empty_list():

    RATINGS.clear()

    avgs = _calculate_average_ratings()
    assert avgs == {}

def test_average_rating_single_entry():

    RATINGS.clear()
    RATINGS.append(
        {"user_id": 1, "school_id": "1", "value": 5}
    )

    avgs = _calculate_average_ratings()
    assert avgs["1"] == 5.0