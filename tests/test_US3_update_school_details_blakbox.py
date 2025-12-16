"""
Black-box tests for US3 - Update School Details

These tests simulate administrator interactions with the school update feature
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS, add_school


def test_update_no_schools():
    """
    Tests message when no schools exist to update
    """

    SCHOOLS.clear()

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("No schools found in the system" in line for line in outputs)


def test_update_school_all_fields_successfully():
    """
    Tests successful update of all school fields
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "Updated School", "2", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert SCHOOLS[0]["name"] == "Updated School"
    assert SCHOOLS[0]["level"] == "secondary"
    assert SCHOOLS[0]["location"] == "Manchester"
    assert any("successfully updated" in line for line in outputs)


def test_update_shows_current_values():
    """
    Tests that current values are displayed to the user
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["5", "", "", ""])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    update_school_by_id(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "Test School" in output_text
    assert "Primary" in output_text
    assert "London" in output_text


def test_update_cancel():
    """
    Tests that entering '0' cancels update and returns to menu
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

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("cancelled" in line for line in outputs)


def test_update_invalid_school_id():
    """
    Tests that invalid school ID shows error and prompts again
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["999", "1", "", "", ""])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("does not exist" in line for line in outputs)


def test_update_partial_fields():
    """
    Tests updating only some fields while keeping others
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "New School", "", ""])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    # Changed field
    assert SCHOOLS[0]["name"] == "New School"
    # Unchanged fields
    assert SCHOOLS[0]["level"] == "primary"
    assert SCHOOLS[0]["location"] == "London"


def test_update_with_validation_errors():
    """
    Tests that validation errors are shown and user is prompted again to retry
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "AB", "New School", "5", "2", "XY", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("must be at least 5 characters" in line or "must be at least 3 characters" in line for line in outputs)
    assert SCHOOLS[0]["name"] == "New School"
    assert SCHOOLS[0]["location"] == "Manchester"


def test_update_prevents_duplicate():
    """
    Tests that update function prevents duplicate schools
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })
    add_school({
        "school_id": 2,
        "name": "School Two",
        "level": "secondary",
        "location": "Manchester"
    })

    inputs_iter = iter(["2", "Test School", "1", "London", "Birmingham"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("already exists" in line for line in outputs)
    assert SCHOOLS[1]["location"] == "Birmingham"
