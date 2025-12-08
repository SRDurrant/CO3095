"""
White-box tests for US1 - Create the Schools

These tests will target the internal functions used by add_new_schools
to make sure all the branches and conditions are exercised
"""

from app.data_store import SCHOOLS, add_school, get_schools, get_next_school_id

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


def test_add_school():
    """
    Tests that add_school correctly adds a school to the global list SCHOOLS
    """

    setup_schools([])

    new_school = {
        "school_id": 1,
        "name": "Test School",
        "level": "combined",
        "location": "London"
    }

    add_school(new_school)
    schools = get_schools()

    assert len(schools) == 1
    assert schools[0]["name"] == "Test School"
    assert schools[0]["level"] == "combined"
    assert schools[0]["location"] == "London"


def test_get_next_school_id_empty():
    """
    Tests that get_next_school_id returns 1 for an empty list
    """

    schools = []
    assert get_next_school_id(schools) == 1


def test_get_next_school_id_non_empty():
    """
    Tests that get_next_school_id returns highest active id + 1
    """

    schools = [
        {"school_id": 1, "name": "School 1", "level": "primary", "location": "London"},
        {"school_id": 2, "name": "School 2", "level": "secondary", "location": "London"}
    ]

    assert get_next_school_id(schools) == 3
