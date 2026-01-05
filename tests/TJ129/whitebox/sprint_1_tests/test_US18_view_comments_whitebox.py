"""
White-box tests for US18 - View Comments for a School.
"""
from datetime import datetime, timezone, timedelta
from app.reviews import (
    clear_comments,
    add_comment_record,
    get_comments_for_school,
)

def test_get_comments_sorted_newest_first():
    clear_comments()
    t1 = datetime.now(timezone.utc) - timedelta(minutes=10)
    t2 = datetime.now(timezone.utc)
    add_comment_record(1, "SCH-9", "Old comment", t1)
    add_comment_record(2, "SCH-9", "New comment", t2)
    result = get_comments_for_school("SCH-9", newest_first=True)
    assert result[0]["text"] == "New comment"
    assert result[1]["text"] == "Old comment"

def test_get_comments_sorted_oldest_first():
    clear_comments()
    t1 = datetime.now(timezone.utc) - timedelta(minutes=10)
    t2 = datetime.now(timezone.utc)
    add_comment_record(1, "SCH-9", "Old", t1)
    add_comment_record(2, "SCH-9", "New", t2)
    result = get_comments_for_school("SCH-9", newest_first=False)
    assert result[0]["text"] == "Old"
    assert result[1]["text"] == "New"
