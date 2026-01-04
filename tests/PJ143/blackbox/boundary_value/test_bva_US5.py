"""
Boundary Value Analysis for US5 - View School Profile

Testing boundary conditions
"""

from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_school_id_1():
    """Boundary: minimum typical school ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "First", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_school_id_large():
    """Boundary: large school ID"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 100, "name": "Large ID", "level": "primary", "location": "London"})

    inputs = iter(["100", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_rating_exactly_1():
    """Boundary: minimum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 1})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("1.00" in s for s in outputs)


def test_rating_exactly_5():
    """Boundary: maximum rating value"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 5})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("5.00" in s for s in outputs)


def test_zero_ratings():
    """Boundary: no ratings at all"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("No ratings yet" in s for s in outputs)


def test_input_zero_exits():
    """Boundary: 0 should exit"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False
