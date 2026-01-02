from app.data_store import SCHOOLS
from app.reviews import RATINGS
from app.school_actions import view_top_schools

"""S = number of schools, L= limit"""
def test_concolic_less_than_limit():
    """
    Concrete run: S=1, L=3
    Symbolic outcome: S ≤ L branch
    """
    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Solo", "level": "secondary", "location": "X"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 4})

    outputs = []
    view_top_schools(limit=3, print_func=lambda x: outputs.append(x))

    assert any("Solo" in line for line in outputs)


def test_concolic_exceeds_limit():
    """
    Concrete run: S=4, L=3
    Symbolic flip: S > L branch
    """
    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(1, 5):
        SCHOOLS.append({"school_id": i, "name": f"S{i}", "level": "secondary", "location": "X"})
        RATINGS.append({"user_id": i, "school_id": str(i), "value": i})

    outputs = []
    view_top_schools(limit=3, print_func=lambda x: outputs.append(x))

    # Only top 3 should appear
    assert "S4" in "".join(outputs)
    assert "S1" not in "".join(outputs)