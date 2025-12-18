from app.school_actions import view_school_rankings
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_view_school_rankings_blackbox(capsys):

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.extend([
        {"school_id": 1, "name": "A", "level": "primary", "location": "X"},
        {"school_id": 2, "name": "B", "level": "primary", "location": "Y"},
    ])

    RATINGS.extend([
        {"user_id": 1, "school_id": "1", "value": 5},
        {"user_id": 2, "school_id": "2", "value": 3},
    ])

    view_school_rankings()
    out = capsys.readouterr().out

    assert "Primary Schools Ranking" in out
    assert out.index("A") < out.index("B")