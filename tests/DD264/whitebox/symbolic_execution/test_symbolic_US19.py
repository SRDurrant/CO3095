"""
White-box tests for US19 - Average Rating (Symbolic Execution Style)

Path conditions for get_average_rating_for_school():
- matching ratings list is empty -> returns None
- matching ratings list is non-empty -> returns average
"""

from app.reviews import RATINGS, get_average_rating_for_school


def reset_ratings(seed):
    RATINGS.clear()
    RATINGS.extend(seed)


def test_symbolic_path_no_matching_ratings_returns_none():
    reset_ratings([
        {"user_id": 1, "school_id": "OTHER", "value": 5},
    ])

    out = get_average_rating_for_school("SCH-1")
    assert out is None


def test_symbolic_path_matching_ratings_returns_average():
    reset_ratings([
        {"user_id": 1, "school_id": "SCH-2", "value": 2},
        {"user_id": 2, "school_id": "SCH-2", "value": 4},
    ])

    out = get_average_rating_for_school("SCH-2")
    assert abs(out - 3.0) < 1e-9
