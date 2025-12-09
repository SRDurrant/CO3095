"""
Black-box tests for US6 - List All Schools

These tests simulate user interactions with the list_all_schools feature
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS, add_school


def test_list_no_schools_message():
    """
    Tests that correct message is shown when no schools exist
    """

    SCHOOLS.clear()

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert len(outputs) > 0
    assert any("No schools found in the system" in line for line in outputs)


def test_list_shows_id_and_name_only():
    """
    Tests that only school ID and name are shown
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

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "Test School" in output_text
    assert "ID: 1" in output_text
    # Verifies level and location aren't shown
    assert not any("primary" in line.lower() and "Test" in line for line in outputs)
    assert not any("London" in line and "Test" in line for line in outputs)


def test_list_schools_header_displayed():
    """
    Tests that the header is displayed when schools exist
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

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("Schools" in line for line in outputs)


def test_list_schools_return_prompt_shown():
    """
    Test that the return to main menu prompt is always shown
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

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("Press '0' to return to the main menu" in line for line in outputs)


def test_user_return_to_menu_input():
    """
    Tests that user input is captured for returning to menu
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    input_captured = []

    def fake_input(prompt: str) -> str:
        input_captured.append(True)
        return "0"

    def fake_print(message: str) -> None:
        pass

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert len(input_captured) == 1
