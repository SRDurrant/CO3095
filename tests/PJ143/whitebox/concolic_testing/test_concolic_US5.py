"""
Concolic testing for US5 - View School Profile

Concrete execution paths
"""

from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_path_exit_immediately():
    """Path: enter 0 -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_empty_id_then_exit():
    """Path: empty ID -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_path_non_numeric_then_exit():
    """Path: non-numeric ID -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert not result


def test_path_invalid_id_then_exit():
    """Path: invalid school ID -> error -> exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_path_view_with_rating():
    """Path: valid ID -> has rating -> display -> exit"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("4.00" in s for s in outputs)


def test_path_view_no_rating():
    """Path: valid ID -> no rating -> display 'No ratings yet'"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("No ratings yet" in s for s in outputs)


def test_path_retry_after_error():
    """Path: error -> retry with valid -> view profile"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_path_multiple_errors_then_success():
    """Path: multiple errors -> finally valid ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "abc", "999", "5", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_path_view_second_school():
    """Path: skip first school, view second"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "First", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Second", "level": "secondary", "location": "Loc2"})

    inputs = iter(["2", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("Second" in s for s in outputs)
    assert any("Secondary" in s for s in outputs)


def test_path_view_combined_level():
    """Path: view combined level school"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Combined", "level": "combined", "location": "Newcastle"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("Combined" in s for s in outputs)
