"""
Black-box tests for US4 - Delete School

These tests exhaust administrator interactions with the school deletion feature
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS, add_school


def test_delete_no_schools():
    """
    Tests error message when no schools exist to delete
    """

    SCHOOLS.clear()

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("No schools found in the system" in line for line in outputs)


def test_delete_school_successfully():
    """
    Tests successful deletion of a school by valid ID
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

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert len(SCHOOLS) == 0
    assert any("Test School" in line and "deleted" in line for line in outputs)


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


def test_delete_school_cancel():
    """
    Tests that entering '0' cancels deletion and returns to menu
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
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("cancelled" in line for line in outputs)


def test_delete_empty_input():
    """
    Tests that empty input shows error and prompts again
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["", "1"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("cannot be empty" in line for line in outputs)
    assert any("deleted" in line for line in outputs)


def test_delete_non_numeric_input():
    """
    Tests that non-numeric input shows error and prompts again
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["abc", "xyz", "1"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    # Should see error messages for both invalid inputs
    error_count = sum(1 for line in outputs if "must be a number" in line)
    assert error_count == 2


def test_delete_id_not_exist():
    """
    Tests that school ID that doesn't exist shows error and prompts again
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["999", "1"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = delete_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("does not exist" in line for line in outputs)
