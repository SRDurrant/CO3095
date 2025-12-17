from app.school_actions import view_top_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_top_schools_limit_whitebox():

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "OnlyOne", "level": "primary", "location": "X"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 5})

    outputs = []
    view_top_schools(limit=3, print_func=lambda x: outputs.append(x))

    assert len(outputs) > 0

def test_top_schools_no_schools_whitebox():
    """Test path when there are no schools in the system."""
    SCHOOLS.clear()
    RATINGS.clear()

    outputs = []
    view_top_schools(print_func=lambda x: outputs.append(x))
    assert outputs[0] == "\n=== Top 3 "  # Empty or no ranking message can be handled

def test_top_schools_zero_ratings_whitebox():
    """Test path where schools exist but no ratings yet."""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.extend([
        {"school_id": 1, "name": "A", "level": "primary", "location": "X"},
        {"school_id": 2, "name": "B", "level": "primary", "location": "Y"},
    ])

    outputs = []
    view_top_schools(print_func=lambda x: outputs.append(x))

    # Check that averages default to 0
    assert "Avg Rating: 0.00" in "".join(outputs)

def test_top_schools_multiple_levels_whitebox():
    """Test internal path where schools exist across multiple levels."""
    SCHOOLS.clear()
    RATINGS.clear()
    SCHOOLS.extend([
        {"school_id": 1, "name": "Primary1", "level": "primary", "location": "X"},
        {"school_id": 2, "name": "Secondary1", "level": "secondary", "location": "Y"},
    ])
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 3},
        {"user_id": 2, "school_id": "2", "value": 5},
    ])

    outputs = []
    view_top_schools(limit=1, print_func=lambda x: outputs.append(x))

    # Check that each level prints separately
    assert any("Primary Schools" in line for line in outputs)
    assert any("Secondary Schools" in line for line in outputs)