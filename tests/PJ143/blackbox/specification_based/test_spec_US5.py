"""
Specification-based tests for US5 - View School Profile

Testing the view school profile functionality
"""

from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_view_profile_with_rating():
    """View a school profile that has ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["1", ""])
    outputs = []

    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("Test School" in s for s in outputs)
    assert any("Primary" in s for s in outputs)
    assert any("London" in s for s in outputs)
    assert any("4.50" in s for s in outputs)


def test_view_profile_no_rating():
    """View a school with no ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "New School", "level": "secondary", "location": "Paris"})

    inputs = iter(["1", ""])
    outputs = []

    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("New School" in s for s in outputs)
    assert any("No ratings yet" in s for s in outputs)


def test_view_multiple_schools():
    """View profiles of multiple schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Loc2"})

    # view first school
    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)
    assert result is True


def test_exit_without_viewing():
    """Exit by entering 0"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_invalid_school_id():
    """Try to view non-existent school"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("does not exist" in s for s in outputs)


def test_empty_school_id():
    """Empty ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("cannot be empty" in s for s in outputs)


def test_non_numeric_id():
    """Non-numeric ID should be rejected"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("must be a number" in s for s in outputs)


def test_school_with_combined_level():
    """View a combined level school"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "combined", "location": "Burnley"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("Combined" in s for s in outputs)


def test_invalid_then_valid_id():
    """Retry after entering invalid ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_display_all_fields():
    """Ensure all school fields are displayed"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test School", "level": "primary", "location": "York"})
    RATINGS.append({"school_id": "5", "value": 3})

    inputs = iter(["5", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("5" in s for s in outputs)
    assert any("Test School" in s for s in outputs)
    assert any("Primary" in s for s in outputs)
    assert any("York" in s for s in outputs)
    assert any("3.00" in s for s in outputs)


def test_school_id_whitespace():
    """ID with whitespace should be stripped"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["  1  ", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True
