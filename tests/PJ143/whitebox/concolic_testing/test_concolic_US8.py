"""
Concolic testing for US8 - Search Schools by Name

Concrete execution paths
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_path_exit_immediately():
    """Path: enter 0 -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_path_empty_search_then_exit():
    """Path: empty keyword -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("cannot be empty" in s for s in outputs)


def test_path_no_matches_then_exit():
    """Path: search -> no matches -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Nonexistent", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_path_search_and_exit():
    """Path: search -> results -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test" in s for s in outputs)


def test_path_search_view_profile():
    """Path: search -> results -> view profile"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("5.00" in s for s in outputs)


def test_path_search_again():
    """Path: search -> results -> search again -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "First", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Second", "level": "primary", "location": "Loc2"})

    inputs = iter(["First", "2", "Second", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("First" in s for s in outputs)
    assert any("Second" in s for s in outputs)


def test_path_invalid_choice_then_exit():
    """Path: search -> invalid choice -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "9", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_path_multiple_searches():
    """Path: search -> search again -> search again -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "primary", "location": "Loc2"})

    inputs = iter(["School", "2", "School A", "2", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_path_profile_no_rating():
    """Path: search -> view profile -> no rating"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_path_case_insensitive():
    """Path: search with different case -> match"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "TestSchool", "level": "primary", "location": "London"})

    inputs = iter(["testschool", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("TestSchool" in s for s in outputs)
