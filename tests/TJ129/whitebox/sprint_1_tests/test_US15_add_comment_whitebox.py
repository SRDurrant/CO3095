"""
White-box tests for US15 - Add a Comment to a School.
"""
from app.reviews import add_comment, clear_comments, COMMENTS
from app.data_store import set_current_user, clear_current_user

def test_branch_comment_too_long_then_cancel():
    clear_comments()
    clear_current_user()

    user = {"user_id": 5, "username": "longtext", "password": "pw", "role": "student"}
    set_current_user(user)

    long_text = "x" * 600  

    inputs = iter([
        "SCH-LONG",
        long_text,
        "0",
    ])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs, "")

    def fake_print(message: str) -> None:
        outputs.append(message)
    success, result = add_comment(input_func=fake_input, print_func=fake_print)

    assert success is False
    assert "cancelled" in result
    assert len(COMMENTS) == 0
    assert any("500 characters" in line for line in outputs)

def test_branch_valid_comment_direct():
    clear_comments()
    clear_current_user()
    user = {"user_id": 6, "username": "simple", "password": "pw", "role": "student"}
    set_current_user(user)

    inputs = iter([
        "SCH-SIMPLE",
        "Nice school here!",
    ])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs, "")
    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = add_comment(input_func=fake_input, print_func=fake_print)

    assert success is True
    assert len(COMMENTS) == 1
    assert result["text"] == "Nice school here!"
    assert any("successfully" in line.lower() for line in outputs)
