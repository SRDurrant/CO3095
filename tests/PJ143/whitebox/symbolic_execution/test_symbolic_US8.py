"""
Symbolic execution tests for US8 - Search Schools by Name

Testing symbolic path conditions
"""

from app.school_actions import search_schools_by_name
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_symbolic_keyword_equals_zero():
    """Symbolic: keyword == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_keyword_empty():
    """Symbolic: not keyword (empty)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("cannot be empty" in s for s in outputs)


def test_symbolic_keyword_not_empty():
    """Symbolic: keyword has value"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_matching_schools_empty():
    """Symbolic: not matching_schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Nonexistent", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No schools found" in s for s in outputs)


def test_symbolic_matching_schools_not_empty():
    """Symbolic: matching_schools has results"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Search Results" in s for s in outputs)


def test_symbolic_choice_equals_zero():
    """Symbolic: choice == '0'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_equals_one():
    """Symbolic: choice == '1'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test1", "1", ""])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_equals_two():
    """Symbolic: choice == '2'"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test", "2", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_choice_else():
    """Symbolic: choice not in [0,1,2]"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test", "9", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Invalid option" in s for s in outputs)


def test_symbolic_avg_greater_zero():
    """Symbolic: avg > 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("3.00" in s for s in outputs)


def test_symbolic_avg_not_greater_zero():
    """Symbolic: avg <= 0"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("No ratings yet" in s for s in outputs)


def test_symbolic_strip_method():
    """Symbolic: keyword.strip()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["  Test  ", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_lower_method():
    """Symbolic: keyword.lower()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["TEST", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)


def test_symbolic_in_operator():
    """Symbolic: keyword_lower in school.get('name', '').lower()"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test School", "level": "primary", "location": "London"})

    inputs = iter(["Test", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Test School" in s for s in outputs)


def test_symbolic_str_conversion():
    """Symbolic: str(school_id)"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 5, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "5", "value": 4})

    inputs = iter(["Test1", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("4.00" in s for s in outputs)


def test_symbolic_len_function():
    """Symbolic: len(matching_schools)"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test A", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "Test B", "level": "primary", "location": "Loc2"})

    inputs = iter(["Test", "0"])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    assert any("Found 2 school" in s for s in outputs)


def test_symbolic_f_string_format():
    """Symbolic: f-string with :.2f"""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})
    RATINGS.append({"school_id": "1", "value": 3})
    RATINGS.append({"school_id": "1", "value": 4})

    inputs = iter(["Test", "1", ""])
    outputs = []

    search_schools_by_name(lambda _: next(inputs), outputs.append)

    # average is 3.5
    assert any("3.50" in s for s in outputs)


def test_symbolic_while_true_loop():
    """Symbolic: while True continues"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "Test1", "level": "primary", "location": "London"})

    inputs = iter(["Test", "2", "0"])
    search_schools_by_name(lambda _: next(inputs), lambda _: None)


def test_symbolic_for_loop():
    """Symbolic: for school in matching_schools"""
    SCHOOLS.clear()
    SCHOOLS.append({"school_id": 1, "name": "SchoolA", "level": "primary", "location": "Loc1"})
    SCHOOLS.append({"school_id": 2, "name": "SchoolB", "level": "primary", "location": "Loc2"})

    inputs = iter(["", "0"])  # empty will not enter loop
    search_schools_by_name(lambda _: next(inputs), lambda _: None)
