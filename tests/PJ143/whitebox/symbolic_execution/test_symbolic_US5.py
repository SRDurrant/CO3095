"""
Symbolic execution tests for US5 - View School Profile

Testing symbolic path conditions
"""

from app.school_actions import view_school_profile
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_id_equals_zero():
    """Symbolic: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_id_not_zero():
    """Symbolic: school_id_input != '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_symbolic_id_empty():
    """Symbolic: not school_id_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("cannot be empty" in s for s in outputs)


def test_symbolic_id_not_empty():
    """Symbolic: school_id_input has value"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "1Test", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_id_not_digit():
    """Symbolic: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "1Test", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("must be a number" in s for s in outputs)


def test_symbolic_id_is_digit():
    """Symbolic: school_id_input.isdigit() is True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "1Test", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_symbolic_school_exists_false():
    """Symbolic: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "1Test", "level": "primary", "location": "London"})

    inputs = iter(["100", "0"])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("does not exist" in s for s in outputs)


def test_symbolic_school_exists_true():
    """Symbolic: school_exists is True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_school_id_match():
    """Symbolic: school.get('school_id') == school_id"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AmmmA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "BmmmB", "level": "primary", "location": "Loc2"})

    inputs = iter(["2", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("B" in s for s in outputs)


def test_symbolic_avg_greater_zero():
    """Symbolic: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("3.00" in s for s in outputs)


def test_symbolic_no_avg():
    """Symbolic: avg == ''"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result == True
    assert any("No ratings yet" in s for s in outputs)


def test_symbolic_return_true():
    """Symbolic: return True path"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_return_false():
    """Symbolic: return False path"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_strip_method():
    """Symbolic: .strip() applied"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["  1  ", ""])
    result = view_school_profile(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_capitalize_method():
    """Symbolic: .capitalize() on level"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test", "level": "secondary", "location": "London"})

    inputs = iter(["1", ""])
    outputs = []
    result = view_school_profile(lambda _: next(inputs), outputs.append)

    assert result is True
    assert any("Secondary" in s for s in outputs)
