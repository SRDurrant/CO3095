"""
White-box tests for US8 - Search Schools by Name

These tests will target the internal logic and branches within search_schools_by_name()
to ensure all branches and conditions are exercised
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS

def setup_schools(seed):
    """
    Clears SCHOOLS list and adds example schools

    Inputs:
        seed (list[dict]): a list of schools to preload the system

    Outputs:
        None
    """

    SCHOOLS.clear()
    for s in seed:
        SCHOOLS.append(s)


def test_branch_keyword_is_zero():
    """
    Tests the branch where user enters '0' at search prompt
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("Returning to main menu" in line for line in outputs)


def test_branch_empty_keyword():
    """
    Tests the branch where keyword is empty
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("Error: Search cannot be empty" in line for line in outputs)


def test_branch_no_matching_schools():
    """
    Tests the branch where no schools match the keyword
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["Nothing", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("No schools found matching 'Nothing'" in line for line in outputs)


def test_branch_matching_schools_found():
    """
    Tests the branch where matching schools are found
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["Test School", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("Found 1 school(s)" in line for line in outputs)
    assert any("Test School" in line for line in outputs)


def test_branch_choice_zero_after_results():
    """
    Tests the branch where user chooses 0 after viewing results
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["Test Schools", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("Test School" in line for line in outputs)
    assert any("Returning to main menu" in line for line in outputs)


def test_branch_choice_one_view_profile():
    """
    Tests the branch where user chooses 1 to view profile
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["Test", "1", "", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("ID: 1" in line for line in outputs)
    assert any("Name: Test School" in line for line in outputs)
    assert any("Level: Primary" in line for line in outputs)
    assert any("Location: London" in line for line in outputs)


def test_branch_choice_two_search_again():
    """
    Tests the branch where user chooses 2 to search again
    """

    setup_schools([
        {"school_id": 1,
         "name": "First School",
         "level": "primary",
         "location": "London"},

        {"school_id": 2,
         "name": "Second School",
         "level": "secondary",
         "location": "Manchester"}
    ])

    inputs = ["First", "2", "Second", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("First School" in line for line in outputs)
    assert any("Second School" in line for line in outputs)


def test_branch_invalid_choice():
    """
    Tests the branch where user enters invalid option
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs = ["Test", "99", "0"]
    input_index = [0]

    def fake_input(prompt):
        result = inputs[input_index[0]]
        input_index[0] += 1
        return result

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    search_schools_by_name(input_func=fake_input, print_func=fake_print)

    assert any("Invalid option, please try again" in line for line in outputs)
