from app.admin_actions import delete_comment_by_id
from app.reviews import COMMENTS, add_comment_record, clear_comments

def test_delete_comment_empty_list():
    """Ensures code does NOT enter loop when COMMENTS is empty."""
    clear_comments()

    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(1, mock_print)

    assert result is False
    assert outputs[0] == "Error: Comment does not exist."

def test_delete_comment_boundary_first_item():
    """Tests deleting first loop iteration (branch coverage)."""
    clear_comments()
    add_comment_record(10, "S1", "Boundary test")

    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(1, mock_print)

    assert result is True
    assert outputs[0] == "Comment #1 from user 10 has been deleted."
    assert len(COMMENTS) == 0