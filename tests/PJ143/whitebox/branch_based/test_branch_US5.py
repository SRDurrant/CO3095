"""
Branch coverage tests for US5 - View School Profile

Testing all execution branches
"""

from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_id_equals_zero_branch():
    """Branch: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_id_not_zero_branch():
    """Branch: school_id_input != '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_id_empty_branch():
    """Branch: not school_id_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("cannot be empty" in s for s in outputs)


def test_id_not_digit_branch():
    """Branch: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["xyz", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("must be a number" in s for s in outputs)


def test_school_exists_false_branch():
    """Branch: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("does not exist" in s for s in outputs)


def test_school_exists_true_branch():
    """Branch: school_exists is True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_school_id_match_branch():
    """Branch: school.get('school_id') == school_id"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "First", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Second", "level": "primary", "location": "Lc2"})

    inputs = iter(["2", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("Second" in s for s in outputs)


def test_avg_greater_than_zero_branch():
    """Branch: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("4.00" in s for s in outputs)


def test_avg_equals_zero_branch():
    """Branch: avg <= 0 (no ratings)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("No ratings yet" in s for s in outputs)


def test_return_true_after_view():
    """Branch: return True after viewing"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_continue_after_error():
    """Branch: continue after validation error"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_capitalize_level():
    """Branch: level.capitalize() applied"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("Primary" in s for s in outputs)


def test_strip_whitespace():
    """Branch: school_id_input.strip()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["  1  ", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True
