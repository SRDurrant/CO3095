"""
Symbolic execution tests for US4 - Delete School

Testing symbolic path conditions
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def test_symbolic_schools_empty():
    """Symbolic: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_schools_not_empty():
    """Symbolic: schools exist"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    delete_school_by_id(lambda _: next(inputs), lambda _: None)
    # execution continues past empty check


def test_symbolic_id_equals_zero():
    """Symbolic: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == False


def test_symbolic_id_not_zero():
    """Symbolic: school_id_input != '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_id_empty():
    """Symbolic: not school_id_input (empty)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("cannot be empty" in s for s in outputs)


def test_symbolic_id_not_digit():
    """Symbolic: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["xyz", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert result is False
    assert any("must be a number" in s for s in outputs)


def test_symbolic_school_exists_false():
    """Symbolic: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["100", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("does not exist" in s for s in outputs)


def test_symbolic_school_exists_true():
    """Symbolic: school_exists is True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_symbolic_school_id_match():
    """Symbolic: school.get('school_id') == school_id"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "AAAAA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "BBBBB", "level": "primary", "location": "Loc2"})

    inputs = iter(["2", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 1
    assert SCHOOLS[0]["school_id"] == 1


def test_symbolic_choice_equals_one():
    """Symbolic: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "ShhhA", "level": "primary", "location": "Lo1"})
    SCHOOLS.append({"school_id": 2, "name": "ShhhB", "level": "primary", "location": "Lo2"})

    inputs = iter(["1", "1", "2", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_symbolic_choice_not_one():
    """Symbolic: choice != '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_deleted_any_false():
    """Symbolic: deleted_any remains False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_symbolic_deleted_any_true():
    """Symbolic: deleted_any becomes True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_symbolic_strip_method():
    """Symbolic: school_id_input.strip()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    # input with spaces should be stripped
    inputs = iter(["  1  ", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0
