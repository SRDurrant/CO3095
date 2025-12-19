"""
White-box tests for US19 - View Average Rating (Branch-Based)

Branches targeted:
- empty school id -> immediate failure
- no ratings branch -> returns True, None
- ratings exist branch -> returns computed average
"""

from app.reviews import RATINGS, view_average_rating_for_school


def reset_ratings(seed):
    RATINGS.clear()
    RATINGS.extend(seed)


def test_branch_empty_school_id():
    reset_ratings([])

    inputs_iter = iter([""])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    success, result = view_average_rating_for_school(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert "cannot be empty" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_branch_no_ratings_path():
    reset_ratings([])

    inputs_iter = iter(["SCH-X"])

    success, result = view_average_rating_for_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None,
    )

    assert success is True
    assert result is None


def test_branch_ratings_exist_path():
    reset_ratings([
        {"user_id": 1, "school_id": "SCH-Y", "value": 5},
        {"user_id": 2, "school_id": "SCH-Y", "value": 3},
        {"user_id": 3, "school_id": "SCH-Y", "value": 4},
    ])

    inputs_iter = iter(["SCH-Y"])

    success, result = view_average_rating_for_school(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None,
    )

    assert success is True
    assert abs(result - 4.0) < 1e-9
