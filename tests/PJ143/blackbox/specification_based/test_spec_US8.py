"""
Specification-based tests for US8 - Search Schools by Name

Testing the search schools functionality
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_search_exact_match():
    """Search with exact school name"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test School", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)
    assert any("Found 1 school" in s for s in outputs)


def test_search_partial_match():
    """Search with partial keyword"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)


def test_search_case_insensitive():
    """Search should be case insensitive"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["TEST", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)


def test_search_no_matches():
    """Search with no matching results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Nonexistent", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found matching" in s for s in outputs)


def test_search_multiple_matches():
    """Search returns multiple schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Primary School A", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Primary School B", "level": "primary", "location": "Loc2"})

    inputs = iter(["Primary", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Found 2 school" in s for s in outputs)
    assert any("Primary School A" in s for s in outputs)
    assert any("Primary School B" in s for s in outputs)


def test_search_empty_keyword():
    """Empty search should show error"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("cannot be empty" in s for s in outputs)


def test_exit_with_zero():
    """Exit by entering 0"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Returning to Main Menu" in s for s in outputs)


def test_view_profile_after_search():
    """View profile after finding school"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["Test School", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)
    assert any("4.00" in s for s in outputs)


def test_search_again():
    """Search again after first search"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "First School", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Second School", "level": "primary", "location": "Loc2"})

    inputs = iter(["First", "2", "Second", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("First School" in s for s in outputs)
    assert any("Second School" in s for s in outputs)


def test_invalid_menu_choice():
    """Invalid menu choice after search"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test", "5", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_profile_with_no_rating():
    """View profile of school without rating"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)
