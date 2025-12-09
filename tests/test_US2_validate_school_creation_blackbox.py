"""
Black-box tests for US2 - Validate School Creation Input

These tests simulate administrator interactions with the system
and confrim that validation errors are properly caught and reported
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS, get_schools, add_school

def run_add_school_with_inputs(inputs):
    """
    Helps to run add_new_school with predefined inputs

    Inputs:
        inputs (list[str]): list of user inputs

    Returns:
        tuple:
            - success (bool): True if successful, False otherwise
            - outputs (list[str]): printed messages
    """

    SCHOOLS.clear()

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = add_new_school(input_func=fake_input, print_func=fake_print)
    return success, outputs


def test_validation_empty_school_name_retry():
    """
    Tests that empty school name shows error but allows retry
    """

    success, outputs = run_add_school_with_inputs(
        ["", "Test School", "1", "London"]
    )

    assert success is True
    assert any("cannot be empty" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_validation_short_school_name_retry():
    """
    Tests that school names < 5 characters show error but allow retry
    """

    success, outputs = run_add_school_with_inputs(
        ["A", "Test School", "1", "London"]
    )

    assert success is True
    assert any("must be at least 5 characters long" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_validation_invalid_level_retry():
    """
    Tests that invalid level input show error but allows retry
    """

    success, outputs = run_add_school_with_inputs(
        ["Test School", "5", "2", "London"]
    )

    assert success is True
    assert any("Invalid input" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_validation_empty_location_retry():
    """
    Tests that empty location shows error but allows retry
    """

    success, outputs = run_add_school_with_inputs(
        ["Test School", "1", "", "London"]
    )

    assert success is True
    assert any("cannot be empty" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_validation_short_location_retry():
    """
    Tests that locations shorter than 3 characters show error but allow retry
    """

    success, outputs = run_add_school_with_inputs(
        ["Valid School", "1", "L", "London"]
    )

    assert success is True
    assert any("must be at least 3 characters long" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_validation_duplicate_school_retry_different_location():
    """
    Test that duplicate school names and locations show error but allow retry with different location
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    success, outputs = run_add_school_with_inputs(
        ["Test School", "2", "London", "Manchester"]
    )

    assert success is True
    assert any("already exists" in line for line in outputs)
    assert any("successfully added" in line for line in outputs)


def test_cancel_at_name_prompt():
    """
    Tests that entering 0 at name prompt cancels school creation
    """

    success, outputs = run_add_school_with_inputs(
        ["0"]
    )

    assert success is False
    assert any("cancelled" in line for line in outputs)


def test_cancel_at_level_prompt():
    """
    Tests that entering 0 at level prompt cancels school creation
    """

    success, outputs = run_add_school_with_inputs(
        ["Valid School", "0"]
    )

    assert success is False
    assert any("cancelled" in line for line in outputs)


def test_cancel_at_location_prompt():
    """
    Tests that entering 0 at location prompt cancels school creation
    """

    success, outputs = run_add_school_with_inputs(
        ["Valid School", "1", "0"]
    )

    assert success is False
    assert any("cancelled" in line for line in outputs)
