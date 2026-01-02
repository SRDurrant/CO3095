from app.admin_actions import view_system_statistics
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_system_statistics_empty_blackbox(capsys):
    """Test when there are no users, schools, ratings, or comments."""

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    view_system_statistics()
    out = capsys.readouterr().out

    assert "Total Users: 0" in out
    assert "Total Schools: 0" in out
    assert "Total Ratings: 0" in out
    assert "Total Comments: 0" in out

def test_system_statistics_large_numbers(capsys):
    """Test behavior with very large numbers of entries."""
    """This test is both a Boundary value test and a Robustness test"""
    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.extend([{"user_id": i} for i in range(1000)])
    SCHOOLS.extend([{"school_id": i} for i in range(1000)])
    RATINGS.extend([{"value": i} for i in range(1000)])
    COMMENTS.extend([{"text": f"Comment {i}"} for i in range(1000)])

    view_system_statistics()
    out = capsys.readouterr().out

    assert "Total Users: 1000" in out
    assert "Total Schools: 1000" in out
    assert "Total Ratings: 1000" in out
    assert "Total Comments: 1000" in out