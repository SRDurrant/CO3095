"""
Concolic testing for US6 - List All Schools

Concrete execution paths
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_path_no_schools():
    """Path: no schools -> display message -> return"""
    SCHOOLS.clear()

    inputs = iter([""])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_path_list_and_exit():
    """Path: list schools -> choose 0 -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Test" in s for s in outputs)


def test_path_invalid_then_exit():
    """Path: list -> invalid choice -> error -> retry -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["9", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_path_view_profile_then_exit():
    """Path: list -> view profile -> return -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_path_filter_then_exit():
    """Path: list -> filter -> return -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["2", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_path_sort_then_exit():
    """Path: list -> sort -> return -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["3", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_path_multiple_invalid():
    """Path: multiple invalid choices before exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["5", "7", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    error_count = sum(1 for s in outputs if "Invalid option" in s)
    assert error_count == 2


def test_path_with_ratings():
    """Path: list schools with ratings -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("5.00" in s for s in outputs)


def test_path_without_ratings():
    """Path: list schools without ratings -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_path_multiple_schools():
    """Path: list multiple schools -> exit"""
    SCHOOLS.clear()
    for i in range(3):
        SCHOOLS.append({
            "school_id": i + 1,
            "name": f"School{i + 1}",
            "level": "primary",
            "location": "London"
        })

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("School1" in s for s in outputs)
    assert any("School2" in s for s in outputs)
    assert any("School3" in s for s in outputs)
