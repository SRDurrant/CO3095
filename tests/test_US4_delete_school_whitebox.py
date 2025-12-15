"""
White-box tests for US4 - Delete School

These tests verify the functions: delete_school_by_id, validate_school_id_exits behavior
and exhausts all possible branches
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS, add_school
from app.validation import validate_school_id_exists

def setup_schools(seed):
    """
    Clears and the adds example schools into the global SCHOOLS list

    Inputs:
        seed (list[dict]): a list of schools to preload the system

    Outputs:
        None
    """

    SCHOOLS.clear()
    for s in seed:
        add_school(s)


def test_validate_school_id_exists_found():
    """
    Tests that validate_school_id_exists returns True when school exists
    """

    schools = [
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ]

    exists, msg = validate_school_id_exists(schools, 1)
    assert exists is True
    assert msg == "Accepted"


def test_validate_school_id_exists_not_found():
    """
    Tests that validate_school_id_exists returns False when school doesn't exist
    """

    schools = [
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ]

    exists, msg = validate_school_id_exists(schools, 999)
    assert exists is False
    assert "does not exist" in msg
    assert "999" in msg


def test_delete_school_empty_input():
    """
    Test that empty input shows error and prompts again
    """

    setup_schools([
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ])

    inputs_iter = iter(["", "1"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("cannot be empty" in line for line in outputs)


def test_delete_school_successful():
    """
    Tests successful deletion of a school
    """

    setup_schools([
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "1"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert len(SCHOOLS) == 0
    assert any("has been deleted" in line for line in outputs)


def test_delete_school_cancel():
    """
    Tests that entering '0' cancels deletion
    """

    setup_schools([
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("cancelled" in line for line in outputs)


def test_delete_school_invalid_id_then_valid():
    """
    Tests that invalid ID shows error then accepts valid ID
    """

    setup_schools([
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ])

    inputs_iter = iter(["999", "1"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert len(SCHOOLS) == 0
    assert any("does not exist" in line for line in outputs)
    assert any("has been deleted" in line for line in outputs)


def test_delete_shows_school_info():
    """
    Tests that ID, name, level, and location are all displayed
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = []

    def fake_input(prompt: str) -> str:
        return "1"

    def fake_print(message: str) -> None:
        outputs.append(message)

    delete_school_by_id(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "ID: 1" in output_text
    assert "Test School" in output_text
    assert "Primary" in output_text
    assert "London" in output_text
