"""
Symbolic execution tests for US6 - List All Schools

Testing symbolic path conditions
"""

from app.school_actions import list_all_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_schools_empty():
    """Symbolic: not schools"""
    SCHOOLS.clear()

    inputs = iter([""])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_symbolic_schools_not_empty():
    """Symbolic: schools is not empty"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Schools" in s for s in outputs)


def test_symbolic_choice_equals_zero():
    """Symbolic: choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_equals_one():
    """Symbolic: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["1", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_equals_two():
    """Symbolic: choice == '2'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["2", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_equals_three():
    """Symbolic: choice == '3'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["3", "0", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_else_branch():
    """Symbolic: choice not in [0,1,2,3]"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["5", "0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_symbolic_avg_greater_zero():
    """Symbolic: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("3.00" in s for s in outputs)


def test_symbolic_avg_not_greater_zero():
    """Symbolic: avg <= 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_symbolic_while_true():
    """Symbolic: while True loop continues"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["5", "0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_for_loop():
    """Symbolic: for school in schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("A" in s for s in outputs)
    assert any("B" in s for s in outputs)


def test_symbolic_strip_method():
    """Symbolic: choice.strip()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["  0  "])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_get_default_school_id():
    """Symbolic: school.get('school_id', '?')"""
    SCHOOLS.clear()
    SCHOOLS.append({})  # no school_id

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("?" in s for s in outputs)


def test_symbolic_get_default_name():
    """Symbolic: school.get('name', '?')"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1})  # no name

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("?" in s for s in outputs)


def test_symbolic_averages_get():
    """Symbolic: averages.get(str(school_id), 0.0)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    list_all_schools(lambda _: next(inputs), lambda _: None)


def test_symbolic_str_conversion():
    """Symbolic: str(school_id)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "5", "value": 4})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    assert any("4.00" in s for s in outputs)


def test_symbolic_f_string_format():
    """Symbolic: f-string formatting with :.2f"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["0"])
    outputs = []

    list_all_schools(lambda _: next(inputs), outputs.append)

    # average is 3.5, formatted as 3.50
    assert any("3.50" in s for s in outputs)
