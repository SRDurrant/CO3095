"""
White-box tests for US16 - Edit My Comment (Branch-Based)

These tests force key branches inside edit_my_comment():
- invalid selection branches (non-digit / out-of-range)
- invalid new text branch then cancel
"""

from datetime import datetime, timezone

from app.reviews import clear_comments, add_comment_record, edit_my_comment, COMMENTS
from app.data_store import set_current_user, clear_current_user


def test_branch_invalid_selection_then_success():
    """
    Forces:
    - non-digit selection branch
    - out-of-range branch
    - then valid selection + success update
    """
    clear_comments()
    clear_current_user()

    user = {"user_id": 10, "username": "tester", "password": "pw", "role": "student"}
    set_current_user(user)

    add_comment_record(10, "SCH-1", "Original", datetime.now(timezone.utc))

    inputs_iter = iter([
        "SCH-1",
        "abc",     # non-digit selection branch
        "2",       # out-of-range branch
        "1",       # valid
        "Updated text",
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = edit_my_comment(input_func=fake_input, print_func=fake_print)

    assert success is True
    assert result["text"] == "Updated text"
    assert COMMENTS[0]["text"] == "Updated text"
    assert any("invalid option" in line.lower() for line in outputs)


def test_branch_invalid_new_text_then_cancel():
    """
    Forces:
    - invalid new text branch (empty after strip)
    - then cancel branch at the updated text prompt
    """
    clear_comments()
    clear_current_user()

    user = {"user_id": 11, "username": "tester2", "password": "pw", "role": "student"}
    set_current_user(user)

    add_comment_record(11, "SCH-2", "Keep this", datetime.now(timezone.utc))

    inputs_iter = iter([
        "SCH-2",
        "1",
        "   ",  # invalid new text branch
        "0",    # cancel at updated text prompt
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = edit_my_comment(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert "cancelled" in str(result).lower()
    assert COMMENTS[0]["text"] == "Keep this"
    assert any("cannot be empty" in line.lower() for line in outputs)
