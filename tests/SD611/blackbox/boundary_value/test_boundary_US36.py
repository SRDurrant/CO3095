from app.school_actions import view_trending_schools
from app.data_store import SCHOOLS
from app.reviews import RATINGS


def test_trending_limit_exceeds_schools(capsys):
    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Solo"})
    RATINGS.append({"school_id": 1})

    view_trending_schools(limit=10)
    out = capsys.readouterr().out

    assert "Solo" in out