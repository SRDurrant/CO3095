from app.admin_actions import delete_comment_by_id
from app.reviews import COMMENTS, add_comment_record, clear_comments

def test_delete_comment_not_first():
    """Ensures loop checks multiple items before deleting."""
    clear_comments()
    # Build: 3 comments; we delete the 2nd (ID=2)
    add_comment_record(1, "S1", "First")
    add_comment_record(2, "S1", "Second (Target)")
    add_comment_record(3, "S1", "Third")

    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(2, mock_print)

    assert result is True
    assert outputs[0] == "Comment #2 from user 2 has been deleted."
    assert len(COMMENTS) == 2
    assert COMMENTS[0]["text"] == "First"
    assert COMMENTS[1]["text"] == "Third"