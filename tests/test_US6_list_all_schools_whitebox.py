"""
White-box tests for US6 - List All Schools

These tests verify the list_all_schools function behavior
with different data store states
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS, add_school


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


def test_list_schools_empty():
    """
    Tests that listing schools with empty list shows correct message
    """

    setup_schools([])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("No schools found" in line for line in outputs)
    assert any("Press '0' to return" in line for line in outputs)


def test_list_schools_display_correctly():
    """
    Tests that listing schools displays it correctly
    """

    setup_schools([
        {"school_id": 1, "name": "Test School", "level": "primary", "location": "London"}
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("Schools" in line for line in outputs)
    assert any("Test School" in line for line in outputs)
    assert any("ID: 1" in line for line in outputs)


def test_list_schools_multiple_schools():
    """
    Tests that listing schools with multiple schools displays all of them
    """

    setup_schools([
        {"school_id": 1, "name": "First School", "level": "primary", "location": "London"},
        {"school_id": 2, "name": "Second School", "level": "secondary", "location": "Manchester"},
        {"school_id": 3, "name": "Third School", "level": "combined", "location": "Birmingham"}
    ])

    outputs = []

    def fake_input(prompt: str) -> str:
        return "0"

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = " ".join(outputs)

    assert "First School" in output_text
    assert "Second School" in output_text
    assert "Third School" in output_text


def test_list_shows_options():
    """
    Tests that sub-menu options are displayed
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

    assert any("1. View School Profile" in line for line in outputs)
    assert any("0. Return to Main Menu" in line for line in outputs)


def test_list_invalid_option_input():
    """
    Test that invalid option input shows error and loops back
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["5", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("Invalid option" in line for line in outputs)
