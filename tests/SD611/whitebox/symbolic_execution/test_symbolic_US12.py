from app.data_store import SCHOOLS
from app.reviews import RATINGS
from app.school_actions import view_top_schools

"""S = number of schools, R = number of ratings"""

def test_symbolic_no_schools_path():
    """
    Symbolic Path P1: S = 0
    """
    SCHOOLS.clear()
    RATINGS.clear()

    outputs = []
    view_top_schools(print_func=lambda x: outputs.append(x))

    assert outputs == ["No schools available."]


def test_symbolic_zero_ratings_path():
    """
    Symbolic Path P2: S > 0 ∧ R = 0
    """
    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "A", "level": "primary", "location": "X"})

    outputs = []
    view_top_schools(print_func=lambda x: outputs.append(x))

    assert any("Avg Rating: 0.00" in line for line in outputs)