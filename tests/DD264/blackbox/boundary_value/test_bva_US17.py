"""
Black-box tests for US17 - Delete My Comment (Boundary Value)

Boundary focus:
- Selecting the first comment (1) should succeed
- Selecting the last comment (n) should succeed
"""

from datetime import datetime, timezone

from app.reviews import clear_comments, add_comment_record, delete_my_comment, COMMENTS
from app.data_store import set_current_user, clear_current_user


def run_delete_with_inputs(example_user, seed_comments, inputs):
    clear_comments()
    clear_current_user()

    if example_user is not None:
        set_current_user(example_user)

    for c in seed_comments:
        add_comment_record(
            user_id=c["user_id"],
            school_id=c["school_id"],
            text=c["text"],
            created_at=c.get("created_at", datetime.now(timezone.utc)),
        )

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    success, result = delete_my_comment(input_func=fake_input, print_func=lambda _: None)
    return success, result


def test_delete_select_first_comment_boundary():
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}
    seed = [
        {"user_id": 1, "school_id": "SCH-BVA", "text": "First"},
        {"user_id": 1, "school_id": "SCH-BVA", "text": "Second"},
    ]

    success, result = run_delete_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=["SCH-BVA", "1"],
    )

    assert success is True
    assert result["text"] == "First"
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "Second"


def test_delete_select_last_comment_boundary():
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}
    seed = [
        {"user_id": 2, "school_id": "SCH-BVA2", "text": "First"},
        {"user_id": 2, "school_id": "SCH-BVA2", "text": "Last"},
    ]

    success, result = run_delete_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=["SCH-BVA2", "2"],
    )

    assert success is True
    assert result["text"] == "Last"
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "First"
