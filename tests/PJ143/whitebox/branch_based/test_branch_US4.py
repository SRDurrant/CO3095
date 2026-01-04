"""
Branch coverage tests for US4 - Delete School

Testing all execution branches
"""

from app.admin_actions import delete_school_by_id
from app.data_store import SCHOOLS


def test_schools_empty_branch():
    """Branch: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_schools_not_empty_branch():
    """Branch: schools exist"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_id_input_zero_branch():
    """Branch: school_id_input == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_id_input_not_empty():
    """Branch: not school_id_input"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("cannot be empty" in s for s in outputs)


def test_id_not_digit_branch():
    """Branch: not school_id_input.isdigit()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["abc", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert result == False
    assert any("must be a number" in s for s in outputs)


def test_school_exists_false_branch():
    """Branch: school_exists is False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["999", "0"])
    outputs = []
    result = delete_school_by_id(lambda _: next(inputs), outputs.append)

    assert not result
    assert any("does not exist" in s for s in outputs)


def test_school_found_and_deleted():
    """Branch: school.get('school_id') == school_id"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_school_deleted_from_middle():
    """Branch: deleting school from middle of list"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})
    SCHOOLS.append({"school_id": 3, "name": "SchoolC", "level": "primary", "location": "Loc3"})

    inputs = iter(["2", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 2
    assert SCHOOLS[0]["school_id"] == 1
    assert SCHOOLS[1]["school_id"] == 3


def test_choice_equals_one_branch():
    """Branch: choice == '1' (continue)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SChoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["1", "1", "2", "2"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0


def test_choice_not_one_branch():
    """Branch: choice != '1' (exit)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True
    assert len(SCHOOLS) == 0


def test_deleted_any_false():
    """Branch: deleted_any remains False"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is False


def test_deleted_any_true():
    """Branch: deleted_any becomes True"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True


def test_break_after_deletion():
    """Branch: break after successful deletion"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result == True


def test_continue_after_empty_input():
    """Branch: continue after validation error"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "1", "0"])
    result = delete_school_by_id(lambda _: next(inputs), lambda _: None)

    assert result is True
    assert len(SCHOOLS) == 0
