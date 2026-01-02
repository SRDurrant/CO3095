from app.admin_actions import view_system_statistics
from app.data_store import USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS

def test_statistics_order_of_output():
    """Ensure the print order is consistent (header first, then counts)."""

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