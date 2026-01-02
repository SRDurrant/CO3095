from app.admin_actions import view_system_statistics
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS

def test_statistics_counts():

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()

    USERS.extend([{}, {}])
    SCHOOLS.append({})
    RATINGS.extend([{}, {}, {}])

    outputs = []
    view_system_statistics(print_func=lambda x: outputs.append(x))

    assert "Total Users: 2" in outputs[1]
    assert "Total Ratings: 3" in outputs[3]

def test_statistics_partial_empty_lists():
    """Test branch where some lists are empty and others are not."""
    from app.admin_actions import view_system_statistics
    from app.data_store import USERS, SCHOOLS
    from app.reviews import RATINGS, COMMENTS

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({"user_id": 1})
    RATINGS.extend([{"value": 5}, {"value": 3}])

    outputs = []
    view_system_statistics(print_func=lambda x: outputs.append(x))

    assert "Total Users: 1" in outputs[1]
    assert "Total Schools: 0" in outputs[2]
    assert "Total Ratings: 2" in outputs[3]
    assert "Total Comments: 0" in outputs[4]