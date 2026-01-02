from app.admin_actions import delete_comment_by_id
from app.reviews import clear_comments, add_comment_record, COMMENTS


def test_symbolic_delete_comment_not_found():
    """
    Path condition:
    len(COMMENTS) > 0 AND comment_id not in COMMENTS
    """
    clear_comments()
    add_comment_record(1, "S1", "Only comment")

    outputs = []
    mock_print = lambda msg: outputs.append(msg)

    result = delete_comment_by_id(99, mock_print)

    assert result is False
    assert outputs[0] == "Error: Comment does not exist."
    assert len(COMMENTS) == 1