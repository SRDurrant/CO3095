"""
Black-box tests for US16 - Edit My Comment

These tests treat edit_my_comment() as a black-box feature and validate observable behaviour:
- Requires login
- Cancel at prompts using '0'
- Handles empty school ID
- Handles no comments for the user on that school
- Successful edit updates the comment text
"""

from datetime import datetime, timezone

from app.reviews import (
    clear_comments,
    add_comment_record,
    edit_my_comment,
    COMMENTS,
)
from app.data_store import set_current_user, clear_current_user


def run_edit_with_inputs(example_user, seed_comments, inputs):
    """
    Helper to run edit_my_comment with fake inputs and captured output
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

    success, result = edit_my_comment(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_edit_requires_login():
    """
    If no user is logged in, editing should fail early with an appropriate message
    """
    success, result, outputs = run_edit_with_inputs(
        example_user=None,
        seed_comments=[],
        inputs=[],
    )

    assert success is False
    assert "edit a comment" in str(result).lower()
    assert any("edit a comment" in line.lower() for line in outputs)


def test_edit_cancel_at_school_prompt():
    """
    Entering '0' at the school prompt cancels the edit flow
    """
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=[],
        inputs=["0"],
    )

    assert success is False
    assert "cancelled" in str(result).lower()
    assert any("cancelled" in line.lower() for line in outputs)


def test_edit_empty_school_id_fails():
    """
    Empty school ID should be rejected
    """
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=[],
        inputs=[""],
    )

    assert success is False
    assert "cannot be empty" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)


def test_edit_no_comments_for_user_returns_empty_list():
    """
    If the user has no comments on that school, return success with an empty list
    """
    user = {"user_id": 3, "username": "charlie", "password": "pw", "role": "student"}

    seed = [
        {"user_id": 999, "school_id": "SCH-1", "text": "Not yours"},
    ]

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=["SCH-1"],
    )

    assert success is True
    assert result == []
    assert any("no comments found for you" in line.lower() for line in outputs)


def test_edit_success_updates_comment_text():
    """
    A logged-in user can edit one of their comments successfully
    """
    user = {"user_id": 4, "username": "dave", "password": "pw", "role": "student"}

    seed = [
        {"user_id": 4, "school_id": "SCH-9", "text": "Old comment"},
    ]

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=[
            "SCH-9",
            "1",
            "New text",
        ],
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["text"] == "New text"
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "New text"
    assert any("updated successfully" in line.lower() for line in outputs)
