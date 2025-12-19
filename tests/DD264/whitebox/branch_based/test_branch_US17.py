"""
White-box tests for US17 - Delete My Comment (Branch-Based)

These tests force key branches inside delete_my_comment():
- invalid selection branches (non-digit / out-of-range)
- cancel branch at selection prompt
- success branch removes the correct comment
"""

from datetime import datetime, timezone

from app.reviews import clear_comments, add_comment_record, delete_my_comment, COMMENTS
from app.data_store import set_current_user, clear_current_user


def test_branch_invalid_selection_then_success():
    clear_comments()
    clear_current_user()

    user = {"user_id": 10, "username": "tester", "password": "pw", "role": "student"}
    set_current_user(user)

    add_comment_record(10, "SCH-1", "Delete me", datetime.now(timezone.utc))
    add_comment_record(10, "SCH-1", "Keep me", datetime.now(timezone.utc))

    inputs_iter = iter([
        "SCH-1",
        "abc",   # non-digit
        "9",     # out-of-range
        "1",     # valid
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = delete_my_comment(input_func=fake_input, print_func=fake_print)

    assert success is True
    assert result["text"] == "Delete me"
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "Keep me"
    assert any("invalid option" in line.lower() for line in outputs)


def test_branch_cancel_at_selection_prompt():
    clear_comments()
    clear_current_user()

    user = {"user_id": 11, "username": "tester2", "password": "pw", "role": "student"}
    set_current_user(user)

    add_comment_record(11, "SCH-2", "Do not delete", datetime.now(timezone.utc))

    inputs_iter = iter([
        "SCH-2",
        "0",  # cancel at selection
    ])

    success, result = delete_my_comment(
        input_func=lambda _: next(inputs_iter, ""),
        print_func=lambda _: None
    )

    assert success is False
    assert "cancelled" in str(result).lower()
    assert len(COMMENTS) == 1
    assert COMMENTS[0]["text"] == "Do not delete"
