from app.admin_actions import delete_comment_by_id
from app.reviews import add_comment_record, clear_comments

def test_concolic_delete_comment_paths():
    clear_comments()

    # Path 1 → empty list path
    outputs = []
    delete_comment_by_id(1, lambda m: outputs.append(m))
    assert "does not exist" in outputs[0]

    # Path 2 → first-item deletion path
    clear_comments()
    add_comment_record(10, "S1", "A")
    outputs.clear()
    delete_comment_by_id(1, lambda m: outputs.append(m))
    assert "deleted" in outputs[0]

    # Path 3 → non-first deletion path
    clear_comments()
    add_comment_record(1, "S1", "First")
    add_comment_record(2, "S1", "Second")
    outputs.clear()
    delete_comment_by_id(2, lambda m: outputs.append(m))
    assert "deleted" in outputs[0]