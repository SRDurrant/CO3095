"""
Black-box tests for US19 - View Average Rating for a School

These tests treat view_average_rating_for_school() as a black-box feature:
- Cancel with '0'
- Empty school ID rejected
- No ratings returns success with None
- Ratings exist returns correct average
"""

from app.reviews import (
    RATINGS,
    view_average_rating_for_school,
)


def reset_ratings(seed):
    """
    Reset and preload RATINGS list

    Inputs:
        seed (list[dict]): ratings to preload

    Outputs:
        None
    """
    RATINGS.clear()
    RATINGS.extend(seed)


def run_view_avg_with_inputs(seed_ratings, inputs):
    """
    Helper to run view_average_rating_for_school with fake inputs and captured output
    """
    reset_ratings(seed_ratings)
    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = view_average_rating_for_school(
        input_func=fake_input,
        print_func=fake_print,
    )
    return success, result, outputs


def test_view_avg_cancel():
    success, result, outputs = run_view_avg_with_inputs([], ["0"])
    assert success is False
    assert "cancelled" in str(result).lower()
    assert any("cancelled" in line.lower() for line in outputs)


def test_view_avg_empty_school_id_fails():
    success, result, outputs = run_view_avg_with_inputs([], [""])
    assert success is False
    assert "cannot be empty" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_view_avg_no_ratings_returns_none():
    success, result, outputs = run_view_avg_with_inputs([], ["SCH-1"])
    assert success is True
    assert result is None
    assert any("no ratings found" in line.lower() for line in outputs)


def test_view_avg_returns_average_when_ratings_exist():
    seed = [
        {"user_id": 1, "school_id": "SCH-9", "value": 4},
        {"user_id": 2, "school_id": "SCH-9", "value": 2},
    ]

    success, result, outputs = run_view_avg_with_inputs(seed, ["SCH-9"])
    assert success is True
    assert isinstance(result, float)
    assert abs(result - 3.0) < 1e-9
    assert any("average rating" in line.lower() for line in outputs)
