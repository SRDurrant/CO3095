from app.admin_actions import view_system_statistics
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_view_system_statistics(capsys):

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({"user_id": 1})
    SCHOOLS.append({"school_id": 1})
    RATINGS.append({"value": 5})
    COMMENTS.append({"text": "test"})

    view_system_statistics()
    out = capsys.readouterr().out

    assert "Total Users: 1" in out
    assert "Total Schools: 1" in out
    assert "Total Ratings: 1" in out
    assert "Total Comments: 1" in out

def test_system_statistics_multiple_entries_blackbox(capsys):
    """Test system statistics with multiple entries per category."""
    from app.admin_actions import view_system_statistics
    from app.data_store import USERS, SCHOOLS
    from app.reviews import RATINGS, COMMENTS

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    # Add multiple entries
    USERS.extend([{"user_id": i} for i in range(1, 4)])       # 3 users
    SCHOOLS.extend([{"school_id": i} for i in range(1, 5)])   # 4 schools
    RATINGS.extend([{"value": i} for i in range(1, 6)])       # 5 ratings
    COMMENTS.extend([{"text": f"Comment {i}"} for i in range(3)])  # 3 comments

    view_system_statistics()
    out = capsys.readouterr().out

    assert "Total Users: 3" in out
    assert "Total Schools: 4" in out
    assert "Total Ratings: 5" in out
    assert "Total Comments: 3" in out