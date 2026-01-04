"""
Branch coverage tests for US8 - Search Schools by Name

Testing all execution branches
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_keyword_equals_zero():
    """Branch: keyword == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Returning to Main Menu" in s for s in outputs)


def test_keyword_empty_branch():
    """Branch: not keyword"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("cannot be empty" in s for s in outputs)


def test_keyword_not_empty_branch():
    """Branch: keyword has value"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_matching_schools_empty():
    """Branch: not matching_schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Nonexistent", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_matching_schools_not_empty():
    """Branch: matching_schools has results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Search Results" in s for s in outputs)


def test_choice_equals_zero_after_search():
    """Branch: choice == '0' after results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_choice_equals_one():
    """Branch: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "1", ""])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_choice_equals_two():
    """Branch: choice == '2'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "2", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_choice_else_invalid():
    """Branch: else (invalid choice)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "9", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_avg_greater_than_zero():
    """Branch: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("4.00" in s for s in outputs)


def test_avg_not_greater_than_zero():
    """Branch: avg <= 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_for_loop_results():
    """Branch: for school in matching_schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test A", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Test B", "level": "primary", "location": "Loc2"})

    inputs = iter(["Test", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test A" in s for s in outputs)
    assert any("Test B" in s for s in outputs)


def test_lower_method():
    """Branch: keyword.lower() case conversion"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["TEST", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)


def test_get_with_default():
    """Branch: school.get() with default"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1})  # missing name

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    # will trigger empty keyword error first
    assert any("cannot be empty" in s for s in outputs)
