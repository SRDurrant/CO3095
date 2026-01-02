def test_average_rating_symbolic_bounds_whitebox():
    from app.school_actions import _calculate_average_ratings
    from app.reviews import RATINGS

    RATINGS.clear()
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 1},
        {"user_id": 2, "school_id": "1", "value": 5},
        {"user_id": 3, "school_id": "1", "value": 3},
    ])

    avgs = _calculate_average_ratings()

    # Symbolic invariant: average must be between min and max rating
    assert 1 <= avgs["1"] <= 5