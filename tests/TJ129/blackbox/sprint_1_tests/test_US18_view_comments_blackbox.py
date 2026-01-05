"""
Black-box tests for US18 - View Comments for a School.
"""
from datetime import datetime, timezone
from app.reviews import (
    COMMENTS,
    clear_comments,
    add_comment_record,
    view_comments_for_school,
)

def run_view_comments(inputs):
    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = view_comments_for_school(
        input_func=fake_input,
        print_func=fake_print,
    )
    return success, result, outputs

def test_view_comments_cancel():
    success, result, outputs = run_view_comments(["0"])
    assert success is False
    assert "cancelled" in result.lower()

def test_view_comments_empty_school_id():
    success, result, outputs = run_view_comments([""])
    assert success is False
    assert "cannot be empty" in result.lower()
def test_view_comments_no_comments():
    clear_comments()
    success, result, outputs = run_view_comments(["SCH-1"])
    assert success is True
    assert result == []
    assert "no comments" in "\n".join(outputs).lower()

def test_view_comments_existing_comments():
    clear_comments()
    add_comment_record(1, "SCH-1", "First", datetime.now(timezone.utc))
    add_comment_record(2, "SCH-1", "Second", datetime.now(timezone.utc))
    success, result, outputs = run_view_comments(["SCH-1"])
    assert success is True
    assert len(result) == 2
    joined = "\n".join(outputs).lower()
    assert "first" in joined
    assert "second" in joined
