"""
Black-box tests for US1 - Add a New School

These tests simulate administrator interactions with the system
using a fake input function and capture the output via fake print function.
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS, get_schools


def run_add_school_with_inputs(inputs):
    """
    Helps to run add_new_school with predefined inputs

    Inputs:
        inputs (list[str]): list of user inputs:
                           [name, level, location]

    Returns:
        tuple:
            - success (bool): True if successful, False otherwise
            - outputs (list[str]): printed messages
    """

    SCHOOLS.clear()

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    success = add_new_school(input_func=fake_input, print_func=fake_print)
    return success, outputs


def test_add_school_success_primary():
    """
    Tests successful addition of a primary school
    """

    success, outputs = run_add_school_with_inputs(
        ["St Joseph's", "1", "Dudley"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["name"] == "St Joseph's"
    assert schools[0]["level"] == "primary"
    assert schools[0]["location"] == "Dudley"
    assert schools[0]["school_id"] == 1
    assert any("successfully added" in line for line in outputs)


def test_add_school_success_secondary():
    """
    Tests successful addition of a secondary school
    """

    success, outputs = run_add_school_with_inputs(
        ["Bishop Milner", "2", "Dudley"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["name"] == "Bishop Milner"
    assert schools[0]["level"] == "secondary"
    assert schools[0]["location"] == "Dudley"
    assert schools[0]["school_id"] == 1


def test_add_school_success_combined():
    """
    Tests successful addition of a combined school
    """

    success, outputs = run_add_school_with_inputs(
        ["Royal School Wolverhampton", "3", "Wolverhampton"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["name"] == "Royal School Wolverhampton"
    assert schools[0]["level"] == "combined"
    assert schools[0]["location"] == "Wolverhampton"


def test_add_school_empty_name():
    """
    Tests adding a school with empty name (currently no validation, should be accepted)
    """

    success, outputs = run_add_school_with_inputs(
        ["", "1", "London"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["name"] == ""


def test_add_school_empty_level_choice():
    """
    Tests adding a school with empty level choice (currently no validation, should be accepted)
    """

    success, outputs = run_add_school_with_inputs(
        ["Fancy School", "", "London"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["level"] == "5"


def test_add_school_empty_location():
    """
    Tests adding a school with empty location (currently no validation, should be accepted)
    """

    success, outputs = run_add_school_with_inputs(
        ["Test School", "1", ""]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["location"] == ""


def test_add_school_invalid_level_choice():
    """
    Tests adding a school with invalid level choice (currently no validation, should be accepted)
    """

    success, outputs = run_add_school_with_inputs(
        ["Test School", "5", "London"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["level"] == "5"


def test_add_school_special_characters_name():
    """
    Tests adding a school with special characters in name (should be accepted)
    """

    success, outputs = run_add_school_with_inputs(
        ["Test & School", "1", "Oxford"]
    )

    assert success is True
    schools = get_schools()
    assert len(schools) == 1
    assert schools[0]["name"] == "Test & School"
