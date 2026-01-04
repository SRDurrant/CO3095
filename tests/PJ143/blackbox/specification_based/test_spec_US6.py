"""
Specification-based tests for US6 - List All Schools

Testing the list all schools functionality
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_list_schools_with_ratings():
    """List schools that have ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School A", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "School B", "level": "secondary", "location": "Per"})
    RATINGS.append({"school_id": "1", "value": 4})
    RATINGS.append({"school_id": "2", "value": 5})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("School A" in s for s in outputs)
    assert any("School B" in s for s in outputs)
    assert any("4.00" in s for s in outputs)
    assert any("5.00" in s for s in outputs)


def test_list_schools_no_ratings():
    """List schools without any ratings"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "New School", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("New School" in s for s in outputs)
    assert any("No ratings yet" in s for s in outputs)


def test_no_schools_in_system():
    """Should display message when no schools exist"""
    SCHOOLS.clear()

    inputs = iter([""])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_exit_with_zero():
    """Exit by choosing option 0"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)
    # should exit without error


def test_invalid_option():
    """Invalid menu option should show error"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["5", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_list_multiple_schools():
    """List multiple schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "School 1", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "School 2", "level": "secondary", "location": "Loc2"})
    SCHOOLS.append({"school_id": 3, "name": "School 3", "level": "combined", "location": "Loc3"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("School 1" in s for s in outputs)
    assert any("School 2" in s for s in outputs)
    assert any("School 3" in s for s in outputs)


def test_menu_options_displayed():
    """Check that all menu options are shown"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("View School Profile" in s for s in outputs)
    assert any("Filter Schools" in s for s in outputs)
    assert any("Sort Schools by Rating" in s for s in outputs)
    assert any("Return to Main Menu" in s for s in outputs)


def test_schools_with_mixed_ratings():
    """Some schools with ratings, some without"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Rated", "level": "primary", "location": "London"})
    SCHOOLS.append({"school_id": 2, "name": "Unrated", "level": "primary", "location": "Derby"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Rated" in s and "3.00" in s for s in outputs)
    assert any("Unrated" in s and "No ratings yet" in s for s in outputs)


def test_school_id_displayed():
    """Verify school IDs are displayed"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("ID: 5" in s for s in outputs)


def test_average_rating_format():
    """Check average rating formatting"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    # average should be 3.5
    assert any("3.50" in s for s in outputs)
