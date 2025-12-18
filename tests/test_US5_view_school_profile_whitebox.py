"""
White-box tests for US5 - View School Profile

These tests verify the view_school_profile function behavior
with different data store states
"""

from app.school_actions import view_school_profile
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


def test_view_profile_school_exists():
    """
    Tests viewing profile of an existing school
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["1", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    view_school_profile(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "School Profile" in output_text
    assert "School ID: 1" in output_text
    assert "Test School" in output_text
    assert "Primary" in output_text
    assert "London" in output_text


def test_view_profile_cancel():
    """
    Tests "0" opts out of View School Profile
    """

    setup_schools([
        {"school_id": 1,
         "name": "Test School",
         "level": "primary",
         "location": "London"}
    ])

    inputs_iter = iter(["0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    view_school_profile(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "Returning to schools list" in output_text


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

    inputs_iter = iter(["1", "0", "2", "0"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "0")

    def fake_print(message: str) -> None:
        outputs.append(message)

    view_school_profile(input_func=fake_input, print_func=fake_print)

    output_text = "\n".join(outputs)

    assert "Test School" in output_text
    assert "Other School" in output_text
