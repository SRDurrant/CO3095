"""
Black-box tests for US19 - View Average Rating (Boundary Value)

Boundary focus (rating scale):
- Single rating at minimum (1) => average is 1.0
- Single rating at maximum (5) => average is 5.0
"""

from app.reviews import RATINGS, view_average_rating_for_school


def reset_ratings(seed):
    RATINGS.clear()
    RATINGS.extend(seed)


def run_view_avg(seed_ratings, inputs):
    reset_ratings(seed_ratings)
    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    success, result = view_average_rating_for_school(
        input_func=fake_input,
        print_func=lambda _: None,
    )
    return success, result


def test_avg_boundary_min_rating_single():
    seed = [{"user_id": 1, "school_id": "SCH-BVA", "value": 1}]

    success, result = run_view_avg(seed, ["SCH-BVA"])
    assert success is True
    assert abs(result - 1.0) < 1e-9


def test_avg_boundary_max_rating_single():
    seed = [{"user_id": 2, "school_id": "SCH-BVA2", "value": 5}]

    success, result = run_view_avg(seed, ["SCH-BVA2"])
    assert success is True
    assert abs(result - 5.0) < 1e-9
