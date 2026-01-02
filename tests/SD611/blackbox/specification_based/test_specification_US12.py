from app.data_store import SCHOOLS
from app.reviews import RATINGS
from app.school_actions import view_top_schools


def test_view_top_schools_multiple_categories(capsys):

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.extend([
        {"school_id": 1, "name": "A", "level": "primary", "location": "X"},
        {"school_id": 2, "name": "B", "level": "secondary", "location": "Y"},
    ])
    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "2", "value": 4},
    ])

    view_top_schools()
    out = capsys.readouterr().out
    assert "Top 3 Primary Schools" in out
    assert "Top 3 Secondary Schools" in out

def test_view_top_schools(capsys):
    """This test is both Boundary (top 3 schools) and specification hence why it is in both"""
    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(1, 5):
        SCHOOLS.append(
            {"school_id": i, "name": f"S{i}", "level": "secondary", "location": "X"}
        )
        RATINGS.append(
            {"user_id": i, "school_id": str(i), "value": i}
        )

    view_top_schools()
    out = capsys.readouterr().out

    assert "Top 3 Secondary Schools" in out
    assert "S4" in out
    assert "S1" not in out