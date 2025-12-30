from app.school_actions import view_trending_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_trending_schools_basic(capsys):


    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Alpha"})
    RATINGS.append({"school_id": 1})
    COMMENTS.append({"school_id": 1})

    view_trending_schools()
    out = capsys.readouterr().out

    assert "Trending Schools" in out
    assert "Alpha" in out

def test_trending_no_schools(capsys):

    SCHOOLS.clear()

    view_trending_schools()
    out = capsys.readouterr().out

    assert "No schools available" in out