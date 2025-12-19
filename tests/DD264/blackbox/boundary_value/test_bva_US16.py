"""
Black-box tests for US16 - Edit My Comment (Boundary Value)

These tests target boundary conditions of the edited comment text:
- Length exactly 500 should pass
- Length 501 should fail (then user cancels)
"""

from datetime import datetime, timezone

from app.reviews import clear_comments, add_comment_record, edit_my_comment, COMMENTS
from app.data_store import set_current_user, clear_current_user


def run_edit_with_inputs(example_user, seed_comments, inputs):
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
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = edit_my_comment(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_edit_comment_length_exactly_500_passes():
    """
    Boundary: edited comment length == 500 should be accepted
    """
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}

    seed = [{"user_id": 1, "school_id": "SCH-BVA", "text": "original"}]
    new_text = "x" * 500

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=[
            "SCH-BVA",
            "1",
            new_text,
        ],
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["text"] == new_text
    assert COMMENTS[0]["text"] == new_text


def test_edit_comment_length_501_fails_then_cancel():
    """
    Boundary: edited comment length == 501 should be rejected, then user cancels
    """
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}

    seed = [{"user_id": 2, "school_id": "SCH-BVA2", "text": "original"}]
    too_long = "x" * 501

    success, result, outputs = run_edit_with_inputs(
        example_user=user,
        seed_comments=seed,
        inputs=[
            "SCH-BVA2",
            "1",
            too_long,  # should fail
            "0",       # cancel at "enter updated comment text"
        ],
    )

    assert success is False
    assert "cancelled" in str(result).lower()
    assert COMMENTS[0]["text"] == "original"
    assert any("at most 500 characters" in line.lower() for line in outputs)
