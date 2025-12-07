"""
Black-box tests for US15 - Add a Comment to a School.
"""

from app.reviews import add_comment, COMMENTS, clear_comments
from app.data_store import set_current_user, clear_current_user

def run_add_comment_with_inputs(example_user, inputs):
    """
    Helper to run add_comment with controlled input/print functions.
    """
    clear_comments()
    clear_current_user()

    if example_user is not None:
        set_current_user(example_user)

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")
    outputs = []
    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = add_comment(input_func=fake_input, print_func=fake_print)
    return success, result, outputs

def test_add_comment_requires_login():
    success, result, outputs = run_add_comment_with_inputs(
        example_user=None,
        inputs=[],
    )
    assert success is False
    assert "logged in" in result
    assert len(COMMENTS) == 0

def test_add_comment_successful():
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}

    success, result, outputs = run_add_comment_with_inputs(
        example_user=user,
        inputs=[
            "SCH-123",
            "This is my comment.",
        ],
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["user_id"] == 1
    assert result["school_id"] == "SCH-123"
    assert result["text"] == "This is my comment."
    assert "created_at" in result
    assert len(COMMENTS) == 1

def test_add_comment_cancel_from_school_prompt():
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}

    success, result, outputs = run_add_comment_with_inputs(
        example_user=user,
        inputs=["0"],
    )
    assert success is False
    assert "cancelled" in result
    assert len(COMMENTS) == 0

def test_add_comment_empty_text_then_valid():
    user = {"user_id": 3, "username": "charlie", "password": "pw", "role": "student"}

    success, result, outputs = run_add_comment_with_inputs(
        example_user=user,
        inputs=[
            "SCH-999",
            "   ",
            "A real comment!",
        ],
    )

    assert success is True
    assert result["text"] == "A real comment!"
    assert len(COMMENTS) == 1
