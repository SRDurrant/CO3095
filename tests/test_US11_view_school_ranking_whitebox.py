from app.school_actions import _calculate_average_ratings
from app.reviews import RATINGS

def test_average_rating_empty_list_whitebox():

    RATINGS.clear()

    avgs = _calculate_average_ratings()
    assert avgs == {}

def test_average_rating_single_entry_whitebox():

    RATINGS.clear()
    RATINGS.append(
        {"user_id": 1, "school_id": "1", "value": 5}
    )

    avgs = _calculate_average_ratings()
    assert avgs["1"] == 5.0

def test_average_rating_multiple_schools_whitebox():

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "2", "value": 3},
    ])

    avgs = _calculate_average_ratings()

    assert avgs["1"] == 5.0
    assert avgs["2"] == 3.0

def test_average_rating_uneven_counts_whitebox():

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "1", "value": 1},
        {"user_id": 3, "school_id": "2", "value": 4},
    ])

    avgs = _calculate_average_ratings()

    assert avgs["1"] == 3.0
    assert avgs["2"] == 4.0

