"""
Specification-based (black-box) tests for US1 - Add New School

Tests based on the functional requirements
"""

from app.admin_actions import add_new_school
from app.data_store import SCHOOLS


def test_add_primary_school_success():
    """Should add a primary school when all inputs are valid"""
    SCHOOLS.clear()
    inputs = ["Primary School", "1", "London", "2"]
    inputs_iter = iter(inputs)

    result = add_new_school(
        input_func=lambda _: next(inputs_iter),
        print_func=lambda _: None
    )

    assert result == True
    assert len(SCHOOLS) == 1
    assert SCHOOLS[0]["name"] == "Primary School"
    assert SCHOOLS[0]["level"] == "primary"
    assert SCHOOLS[0]["location"] == "London"


def test_add_secondary_school():
    """Adding a secondary level school when iputs are valid"""
    SCHOOLS.clear()
    inputs = iter(["Secondary School", "2", "London", "2"])

    result = add_new_school(
        input_func=lambda _: next(inputs),
        print_func=lambda _: None
    )

    assert result is True
    assert SCHOOLS[0]["level"] == "secondary"


def test_add_combined_school():
    SCHOOLS.clear()
    inputs = iter(["Combined School", "3", "Derby", "2"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert SCHOOLS[0]["level"] == "combined"


def test_name_validation_empty():
    """Empty name should be rejected"""
    SCHOOLS.clear()
    inputs = iter(["", "0"])
    output = []

    result = add_new_school(
        input_func=lambda _: next(inputs),
        print_func=lambda msg: output.append(msg)
    )

    assert result is False
    assert any("cannot be empty" in s for s in output)


def test_name_too_short():
    """Name with less than 5 characters should fail"""
    SCHOOLS.clear()
    inputs = iter(["Test", "0"])
    output = []

    result = add_new_school(
        input_func=lambda _: next(inputs),
        print_func=output.append
    )

    assert not result
    assert any("at least 5 characters" in s for s in output)


def test_invalid_level_choice():
    """Level should be rejected"""
    SCHOOLS.clear()
    inputs = iter(["Valid School", "4", "0"])
    output = []

    result = add_new_school(
        lambda _: next(inputs),
        output.append
    )

    assert result is False
    assert any("Invalid input" in s for s in output)


def test_location_too_short():
    """Location must be at least 3 characters"""
    SCHOOLS.clear()
    inputs = iter(["Valid School", "1", "AB", "0"])
    output = []

    result = add_new_school(
        lambda _: next(inputs),
        output.append
    )

    assert result == False
    assert any("at least 3 characters" in s for s in output)


def test_duplicate_school_rejected():
    """System should reject duplicate school (same name + location)"""
    SCHOOLS.clear()
    SCHOOLS.append({
        "school_id": 1,
        "name": "Duplicate School",
        "level": "primary",
        "location": "London"
    })

    inputs = iter(["Duplicate School", "2", "London", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is False
    assert len(SCHOOLS) == 1  # no new school added


def test_exit_at_name_prompt():
    SCHOOLS.clear()
    result = add_new_school(lambda _: "0", lambda _: None)

    assert not result
    assert len(SCHOOLS) == 0


def test_exit_at_level():
    SCHOOLS.clear()
    inputs = iter(["Test School", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_exit_at_location():
    SCHOOLS.clear()
    inputs = iter(["Test School", "1", "0"])
    result = add_new_school(lambda _: next(inputs), lambda _: None)
    assert result == False


def test_add_multiple_schools():
    """Adding multiple schools in one session allowed"""
    SCHOOLS.clear()
    inputs = iter([
        "School One", "1", "City A", "1",
        "School Two", "2", "City B", "2"
    ])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 2
    assert SCHOOLS[0]["name"] == "School One"
    assert SCHOOLS[1]["name"] == "School Two"


def test_add_one_then_exit():
    SCHOOLS.clear()
    inputs = iter(["Single School", "1", "Location", "0"])

    result = add_new_school(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1
