"""
Boundary Value Analysis for US8 - Search Schools by Name

Testing boundary conditions for search
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_search_single_character():
    """Boundary: search with 1 character"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "A School", "level": "primary", "location": "London"})

    inputs = iter(["A", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("A School" in s for s in outputs)


def test_search_empty_string():
    """Boundary: empty search string"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("cannot be empty" in s for s in outputs)


def test_exactly_one_match():
    """Boundary: exactly 1 matching school"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Unique School", "level": "primary", "location": "London"})

    inputs = iter(["Unique", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Found 1 school" in s for s in outputs)


def test_zero_matches():
    """Boundary: 0 matching schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Nonexistent", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_choice_0_exits():
    """Boundary: choice 0 exits"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_choice_1_views():
    """Boundary: choice 1 views profile"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "1", ""])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_choice_2_searches_again():
    """Boundary: choice 2 continues"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "2", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_rating_1_0():
    """Boundary: rating exactly 1.0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 1})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("1.00" in s for s in outputs)


def test_rating_5_0():
    """Boundary: rating exactly 5.0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("5.00" in s for s in outputs)
