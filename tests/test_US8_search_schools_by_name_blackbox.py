"""
Black-box tests for US8 - Search Schools by Name

These tests simulate user interactions with the search system
using a fake input function and capture the output via fake print function.
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS, add_school

def run_search_with_inputs(inputs):
    """
    Helper to run search_schools_by_name with predefined inputs

    Inputs:
        inputs (list[str]): list of user inputs

    Returns:
        tuple:
            - outputs (list[str]): printed messages
    """

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)
    return outputs


def test_search_success_single_result():
    """
    Tests successful search with a single matching school
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["Test School", "0"]
    )

    assert any("Found 1 school(s)" in line for line in outputs)
    assert any("Test School" in line for line in outputs)


def test_search_success_multiple_results():
    """
    Tests successful search with multiple matching schools
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

    outputs = run_search_with_inputs(
        ["School", "0"]
    )

    assert any("Found 2 school(s)" in line for line in outputs)
    assert any("Test School" in line for line in outputs)
    assert any("ABC School" in line for line in outputs)


def test_search_case_insensitive():
    """
    Tests that search is case-insensitive
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["TEST SCHOOL", "0"]
    )

    assert any("Found 1 school(s)" in line for line in outputs)
    assert any("Test School" in line for line in outputs)


def test_search_partial_match():
    """
    Tests that search matches partial keywords
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

    outputs = run_search_with_inputs(
        ["sch", "0"]
    )

    assert any("Found 2 school(s)" in line for line in outputs)
    assert any("Test School" in line for line in outputs)
    assert any("ABC School" in line for line in outputs)


def test_search_empty_keyword():
    """
    Tests searching with empty keyword (should bring up error, then retry)
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["", "Test", "0"]
    )

    assert any("Error: Search cannot be empty" in line for line in outputs)
    assert any("Test School" in line for line in outputs)


def test_search_no_results():
    """
    Tests searching with keyword that has no matches
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["Nothing", "0"]
    )

    assert any("No schools found matching 'Nothing'" in line for line in outputs)
    assert any("Try a different search" in line for line in outputs)


def test_search_and_view_profile():
    """
    Tests searching and then viewing a school profile
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["Test School", "1", "", "0"]
    )

    assert any("Test School" in line for line in outputs)
    assert any("ID: 1" in line for line in outputs)
    assert any("Name: Test School" in line for line in outputs)
    assert any("Level: Primary" in line for line in outputs)
    assert any("Location: London" in line for line in outputs)


def test_search_and_search_again():
    """
    Tests performing multiple searches using option 2
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "First School",
        "level": "primary",
        "location": "London"
    })
    add_school({
        "school_id": 2,
        "name": "Second School",
        "level": "secondary",
        "location": "Manchester"
    })

    outputs = run_search_with_inputs(
        ["First", "2", "Second", "0"]
    )

    assert any("First School" in line for line in outputs)
    assert any("Second School" in line for line in outputs)


def test_search_invalid_menu_option():
    """
    Tests entering invalid option after search results (should bring up error, then retry)
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["Test", "99", "0"]
    )

    assert any("Invalid option, please try again" in line for line in outputs)


def test_cancel_at_search_prompt():
    """
    Tests that entering 0 at search prompt cancels and returns to main menu
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["0"]
    )

    assert any("Returning to main menu" in line for line in outputs)


def test_cancel_after_search_results():
    """
    Tests that entering 0 after viewing results cancels and returns to main menu
    """

    SCHOOLS.clear()
    add_school({
        "school_id": 1,
        "name": "Test School",
        "level": "primary",
        "location": "London"
    })

    outputs = run_search_with_inputs(
        ["Test", "0"]
    )

    assert any("Test School" in line for line in outputs)
    assert any("Returning to main menu" in line for line in outputs)
