from app.admin_actions import delete_comment_by_id
from app.reviews import COMMENTS, clear_comments

def test_delete_nonexistent_comment_blackbox():
    clear_comments()
    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(99, mock_print)

    assert result is False
    assert outputs[0] == "Error: Comment does not exist."
    assert len(COMMENTS) == 0