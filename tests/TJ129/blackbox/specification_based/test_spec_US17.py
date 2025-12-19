"""
Black-box tests for US17 - Delete My Comment

These tests treat delete_my_comment() as a black-box feature and validate observable behaviour:
- Requires login
- Cancel at prompts using '0'
- Empty school ID rejected
- No comments for the user returns empty list
- Successful delete removes exactly one comment
"""

from datetime import datetime, timezone

from app.reviews import (
    clear_comments,
    add_comment_record,
    delete_my_comment,
    COMMENTS,
)
from app.data_store import set_current_user, clear_current_user


def run_delete_with_inputs(example_user, seed_comments, inputs):
    """
    Helper to run delete_my_comment with fake inputs and captured output
    """
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

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = delete_my_comment(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_delete_requires_login():
    success, result, outputs = run_delete_with_inputs(
        example_user=None,
        seed_comments=[],
        inputs=[],
    )
    assert success is False
    assert "delete a comment" in str(result).lower()
    assert any("delete a comment" in line.lower() for line in outputs)


def test_delete_cancel_at_school_prompt():
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}

    success, result, outputs = run_delete_with_inputs(
        example_user=user,
        seed_comments=[],
        inputs=["0"],
    )

    assert success is False
    assert "cancelled" in str(result).lower()
    assert any("cancelled" in line.lower() for line in outputs)


def test_delete_empty_school_id_fails():
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}

    success, result, outputs = run_delete_with_inputs(
        example_user=user,
        seed_comments=[],
        inputs=[""],
    )

    assert success is False
    assert "cannot be empty" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_delete_no_comments_for_user_returns_empty_list():
    user = {"user_id": 3, "username": "charlie", "password": "pw", "role": "student"}

    seed = [{"user_id": 999, "school_id": "SCH-1", "text": "Not yours"}]

    success, result, outputs = run_delete_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=["SCH-1"],
    )

    assert success is True
    assert result == []
    assert any("no comments found for you" in line.lower() for line in outputs)


def test_delete_success_removes_comment():
    user = {"user_id": 4, "username": "dave", "password": "pw", "role": "student"}

    seed = [
        {"user_id": 4, "school_id": "SCH-9", "text": "Delete me"},
        {"user_id": 4, "school_id": "SCH-9", "text": "Keep me"},
    ]

    success, result, outputs = run_delete_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=[
            "SCH-9",
            "1",
        ],
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["text"] == "Delete me"
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "Keep me"
    assert any("deleted successfully" in line.lower() for line in outputs)
