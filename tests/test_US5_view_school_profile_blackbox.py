"""
Black-box tests for US5 - View School Profile

These tests simulate user interactions with the school profile viewing feature
through the view schools interface
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS, add_school


def test_view_profile_page():
    """
    Tests that the view school profile page appears when selected
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test Primary School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "0", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "View School Profile" in output_text


def test_school_profile_display_details():
    """
    Tests that school profile display details(correctly) appears when valid ID input
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

    assert "School ID: 1" in output_text
    assert "Test School" in output_text
    assert "Primary" in output_text
    assert "London" in output_text


def test_invalid_school_id_shows_error():
    """
    Tests that invalid school ID shows error
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "999", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("does not exist" in line for line in outputs)


def test_non_numeric_input_shows_error():
    """
    Tests that non-numeric input shows error
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "abc", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("must be a number" in line for line in outputs)


def test_empty_input_shows_error():
    """
    Tests that empty input shows error
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    inputs_iter = iter(["1", "", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    assert any("cannot be empty" in line for line in outputs)


def test_view_multiple_schools():
    """
    Tests viewing one school profile after another
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
        "name": "Other School",
        "level": "secondary",
        "location": "Manchester"
    })

    inputs_iter = iter(["1", "1", "0", "2", "0", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    list_all_schools(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "Test School" in output_text
    assert "Other School" in output_text
