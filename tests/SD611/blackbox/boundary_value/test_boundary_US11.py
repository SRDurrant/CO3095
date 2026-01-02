from app.school_actions import view_school_rankings
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_view_school_rankings_no_schools(capsys):

    SCHOOLS.clear()
    RATINGS.clear()

    view_school_rankings()
    out = capsys.readouterr().out

    assert "No schools available." in out

def test_view_school_rankings_no_ratings(capsys):
    from app.school_actions import view_school_rankings
    from app.data_store import SCHOOLS
    from app.reviews import RATINGS

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "A", "level": "primary"})

    view_school_rankings()
    out = capsys.readouterr().out

    assert "Avg Rating: 0.00" in out