"""
Black-box tests for US14 - Rate a School.
"""

from app.reviews import rate_school, RATINGS, clear_ratings
from app.data_store import set_current_user, clear_current_user


def run_rate_school_with_inputs(example_user, inputs):
    """
    Helper to run rate_school with controlled input/print functions.

    Inputs:
        example_user (dict | None): user dict to set as current user,
                                    or None if no one should be logged in.
        inputs (list[str]): list of strings that fake user input.

    Returns:
        tuple:
            - success (bool)
            - result (dict | str)
            - outputs (list[str]): printed messages
    """
    clear_ratings()
    clear_current_user()

    if example_user is not None:
        set_current_user(example_user)

    inputs_iter = iter(inputs)
    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = rate_school(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_rate_school_requires_login():
    """
    If no user is logged in, rating should fail with an appropriate message.
    """
    success, result, outputs = run_rate_school_with_inputs(
        example_user=None,
        inputs=[],
    )

    assert success is False
    assert "logged in" in result
    assert any("logged in" in line for line in outputs)


def test_rate_school_success_new_rating():
    """
    A logged-in user can rate a school successfully with valid input.
    """
    user = {"user_id": 1, "username": "alice", "password": "pw", "role": "student"}

    success, result, outputs = run_rate_school_with_inputs(
        example_user=user,
        inputs=[
            "SCH-123",  
            "4",        
        ],
    )

    assert success is True
    assert isinstance(result, dict)
    assert result["user_id"] == 1
    assert result["school_id"] == "SCH-123"
    assert result["value"] == 4

    
    assert len(RATINGS) == 1
    assert any("Successfully rated" in line for line in outputs)


def test_rate_school_cancel_from_school_prompt():
    """
    User can cancel rating from the school ID prompt by entering '0'.
    """
    user = {"user_id": 2, "username": "bob", "password": "pw", "role": "student"}

    success, result, outputs = run_rate_school_with_inputs(
        example_user=user,
        inputs=[
            "0",  
        ],
    )

    assert success is False
    assert "cancelled" in result
    assert len(RATINGS) == 0
    assert any("cancelled" in line for line in outputs)


def test_rate_school_invalid_rating_then_cancel():
    """
    If the user enters an invalid rating then chooses '0', the rating is cancelled.
    """
    user = {"user_id": 3, "username": "charlie", "password": "pw", "role": "student"}

    success, result, outputs = run_rate_school_with_inputs(
        example_user=user,
        inputs=[
            "SCH-999", 
            "abc",      
            "0",        
        ],
    )

    assert success is False
    assert "cancelled" in result
    assert len(RATINGS) == 0
    assert any("cancelled" in line for line in outputs)
