"""
White-box tests for US3 - Update School Details

These tests verify the update_school_by_id function behavior
with different data store states and input sequences
"""

from app.admin_actions import update_school_by_id
from app.data_store import SCHOOLS, add_school


def setup_schools(seed):
    """
    Clears  out list and adds example schools to the global list SCHOOLS

    Inputs:
        seed (list[dict]): a list of schools to preload the system

    Outputs:
        None
    """

    SCHOOLS.clear()
    for s in seed:
        add_school(s)


def test_update_school_empty_list():
    """
    Tests that attempting to update from empty list shows appropriate message
    """

    setup_schools([])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    assert any("No schools found" in line for line in outputs)


def test_update_school_successful_all_fields():
    """
    Tests successful update of all school fields
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "New School", "2", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert SCHOOLS[0]["name"] == "New School"
    assert SCHOOLS[0]["level"] == "secondary"
    assert SCHOOLS[0]["location"] == "Manchester"
    assert any("successfully updated" in line for line in outputs)


def test_update_school_keep_current_name():
    """
    Tests keeping current name by pressing Enter
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "", "2", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    # Unchanged
    assert SCHOOLS[0]["name"] == "Test School"
    # Changed
    assert SCHOOLS[0]["level"] == "secondary"
    assert SCHOOLS[0]["location"] == "Manchester"

def test_update_school_keep_current_level():
    """
    Tests keeping current level by pressing Enter
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "New School", "", "Birmingham"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert SCHOOLS[0]["name"] == "New School"
    # Unchanged level field
    assert SCHOOLS[0]["level"] == "primary"
    assert SCHOOLS[0]["location"] == "Birmingham"


def test_update_school_keep_current_location():
    """
    Tests keeping current location by pressing Enter
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "New School", "3", ""])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert SCHOOLS[0]["name"] == "New School"
    assert SCHOOLS[0]["level"] == "combined"
    # Unchanged location field
    assert SCHOOLS[0]["location"] == "London"


def test_update_school_cancel():
    """
    Tests that entering '0' cancels update
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is False
    # Unchanged school
    assert SCHOOLS[0]["name"] == "Test School"
    assert any("cancelled" in line for line in outputs)


def test_update_school_invalid_id_then_valid():
    """
    Tests that invalid ID shows error then accepts valid ID
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["999", "1", "New School", "2", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("does not exist" in line for line in outputs)
    assert SCHOOLS[0]["name"] == "New School"


def test_update_school_invalid_name_then_valid():
    """
    Tests that invalid name shows error and prompts again
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "AB", "New School", "1", "London"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("must be at least 5 characters long" in line for line in outputs)
    assert SCHOOLS[0]["name"] == "New School"


def test_update_school_invalid_level_then_valid():
    """
    Tests that invalid level shows error and prompts again
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "New School", "4", "2", "London"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("Invalid input" in line for line in outputs)
    assert SCHOOLS[0]["level"] == "secondary"


def test_update_school_invalid_location_then_valid():
    """
    Tests that invalid location shows error and prompts again
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "New School", "2", "AS", "Manchester"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    result = update_school_by_id(input_func=fake_input, print_func=fake_print)

    assert result is True
    assert any("must be at least 3 characters long" in line for line in outputs)
    assert SCHOOLS[0]["location"] == "Manchester"
