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


def test_list_view_profile_option():
    """
    Tests selecting View School Profile option
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "1", "0", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    # Should show View School Profile section
    assert "View School Profile" in output_text
    # Should show school details when valid ID entered
    assert "School Details" in output_text
    assert "Primary" in output_text
    assert "London" in output_text


def test_list_loops_after_viewing_profile():
    """
    Tests that after viewing a profile, user returns to schools list
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
        "name": "ABC School",
        "level": "secondary",
        "location": "Manchester"
    })

    inputs_iter = iter(["1", "1", "0", "1", "2", "0", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert output_text.count("School Details") == 2
    assert "Test School" in output_text
    assert "ABC School" in output_text
