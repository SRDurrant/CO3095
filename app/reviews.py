"""
Ratings and reviews logic for schools.

Implements:
    - US14: Rate a School
    - US15: Add a Comment to a School

Later user stories (US18 - View Comments, favourites, etc.) can reuse
the data structures defined here.
"""
from typing import Callable, Tuple, List, Dict, Optional
from datetime import datetime, timezone
from .data_store import get_current_user
from .validation import validate_rating_input

RATINGS: List[Dict] = []
COMMENTS: List[Dict] = []

def clear_ratings() -> None:
    RATINGS.clear()

def find_rating(user_id: int, school_id: str) -> Optional[Dict]:

    for rating in RATINGS:
        if rating.get("user_id") == user_id and rating.get("school_id") == school_id:
            return rating
    return None

def set_rating(user_id: int, school_id: str, value: int) -> Dict:
    existing = find_rating(user_id, school_id)
    if existing is not None:
        existing["value"] = value
        return existing

    rating = {
        "user_id": user_id,
        "school_id": school_id,
        "value": value,
    }
    RATINGS.append(rating)
    return rating

def clear_comments() -> None:

    COMMENTS.clear()
def add_comment_record(
    user_id: int,
    school_id: str,
    text: str,
    created_at: Optional[datetime] = None,
) -> Dict:

    if created_at is None:
        created_at = datetime.now(timezone.utc)
    comment = {
        "user_id": user_id,
        "school_id": school_id,
        "text": text,
        "created_at": created_at,
    }
    COMMENTS.append(comment)
    return comment

def rate_school(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:

    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to rate a school"
        print_func(msg)
        return False, msg
    while True:
        print_func("\nRate a School")
        print_func("Type '0' at any prompt to return to the previous menu.")

        school_id = input_func("Enter the school ID to rate: ").strip()
        if school_id == "0":
            msg = "Rating cancelled by user"
            print_func(msg)
            return False, msg

        if not school_id:
            print_func("School ID cannot be empty.")
            continue
        break

    while True:
        rating_input = input_func("Enter your rating (1-5): ")

        is_valid, validation_msg = validate_rating_input(rating_input)
        if not is_valid:
            print_func(validation_msg)
            print_func("Type '0' to cancel or try again.")
            retry_or_cancel = input_func("")
            if retry_or_cancel.strip() == "0":
                msg = "Rating cancelled by user"
                print_func(msg)
                return False, msg
            continue
        value = int(rating_input.strip())
        rating = set_rating(current_user["user_id"], school_id, value)

        msg = f"Successfully rated school '{school_id}' with {value} stars."
        print_func(msg)
        return True, rating

def add_comment(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
    max_length: int = 500,
) -> Tuple[bool, object]:

    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to add a comment"
        print_func(msg)
        return False, msg
    while True:
        print_func("\nAdd a Comment")
        print_func("Type '0' at any prompt to return to the previous menu.")

        school_id = input_func("Enter the school ID to comment on: ").strip()
        if school_id == "0":
            msg = "Comment cancelled by user"
            print_func(msg)
            return False, msg

        if not school_id:
            print_func("School ID cannot be empty.")
            continue

        break

    while True:
        raw_text = input_func("Enter your comment: ")
        if raw_text is None:
            raw_text = ""

        stripped = raw_text.strip()
        if stripped == "0":
            msg = "Comment cancelled by user"
            print_func(msg)
            return False, msg

        if stripped == "":
            print_func("Comment cannot be empty.")
            print_func("Type '0' to cancel or enter a non-empty comment.")
        elif len(stripped) > max_length:
            print_func(f"Comment must be at most {max_length} characters.")
            print_func("Type '0' to cancel or enter a shorter comment.")
        else:
            comment = add_comment_record(
                user_id=current_user["user_id"],
                school_id=school_id,
                text=stripped,
            )
            msg = "Comment added successfully."
            print_func(msg)
            return True, comment
       
    
