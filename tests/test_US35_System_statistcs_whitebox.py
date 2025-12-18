from app.admin_actions import view_system_statistics
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS

def test_statistics_counts_whitebox():

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

def test_statistics_order_of_output_whitebox():
    """Ensure the print order is consistent (header first, then counts)."""
    from app.admin_actions import view_system_statistics
    from app.data_store import USERS, SCHOOLS
    from app.reviews import RATINGS, COMMENTS

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({})
    SCHOOLS.append({})
    RATINGS.append({})
    COMMENTS.append({})

    outputs = []
    view_system_statistics(print_func=lambda x: outputs.append(x))

    # Header should be first
    assert outputs[0] == "\n=== System Statistics ==="
    # Counts appear in the correct sequence
    assert outputs[1].startswith("Total Users:")
    assert outputs[2].startswith("Total Schools:")
    assert outputs[3].startswith("Total Ratings:")
    assert outputs[4].startswith("Total Comments:")

def test_statistics_custom_print_func_whitebox():
    """Test that custom print_func is correctly used."""
    from app.admin_actions import view_system_statistics
    from app.data_store import USERS, SCHOOLS
    from app.reviews import RATINGS, COMMENTS

    USERS.clear()
    SCHOOLS.clear()
    RATINGS.clear()
    COMMENTS.clear()

    USERS.append({})
    SCHOOLS.append({})
    RATINGS.append({})
    COMMENTS.append({})

    collected = []

    def fake_print(s):
        collected.append(s)

    view_system_statistics(print_func=fake_print)

    # The collected list should have 5 elements (header + 4 counts)
    assert len(collected) == 5
    assert "Total Users: 1" in collected[1]
    assert "Total Schools: 1" in collected[2]
    assert "Total Ratings: 1" in collected[3]
    assert "Total Comments: 1" in collected[4]

def test_statistics_partial_empty_lists_whitebox():
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