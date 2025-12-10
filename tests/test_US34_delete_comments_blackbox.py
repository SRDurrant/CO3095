from app.admin_actions import delete_comment_by_id
from app.reviews import COMMENTS, add_comment_record, clear_comments

def test_delete_existing_comment_blackbox():
    clear_comments()
    # Setup
    add_comment_record(user_id=2, school_id="SCH1", text="Bad comment")
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(1, mock_print)

    assert result is True
    assert "deleted" in outputs[0].lower()
    assert len(COMMENTS) == 0


def test_delete_nonexistent_comment_blackbox():
    clear_comments()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(99, mock_print)

    assert result is False
    assert outputs[0] == "Error: Comment does not exist."
    assert len(COMMENTS) == 0