"""
Ratings and reviews logic for schools.

Implements:
    - US14: Rate a School
    - US15: Add a Comment to a School

Later user stories (US18 - View Comments, favourites, etc.) can reuse
the data structures defined here.
"""

from typing import Callable, Tuple, List, Dict, Optional
from datetime import datetime
from .data_store import get_current_user
from .validation import validate_rating_input

RATINGS: List[Dict] = []
COMMENTS: List[Dict] = []

def clear_ratings() -> None:
    """
    Clear all stored ratings (primarily for testing purposes).

    Inputs:
        None

    Returns:
        None
    """
    RATINGS.clear()


def find_rating(user_id: int, school_id: str) -> Optional[Dict]:
    """
    Find an existing rating for a given (user, school) pair, if any.

    Inputs:
        user_id (int): ID of the user
        school_id (str): ID of the school

    Returns:
        dict | None: The rating dictionary if found, otherwise None
    """
    for rating in RATINGS:
        if rating.get("user_id") == user_id and rating.get("school_id") == school_id:
            return rating
    return None


def set_rating(user_id: int, school_id: str, value: int) -> Dict:
    """
    Create or update a rating entry and return it.

    If the user has already rated this school, their rating is updated.
    Otherwise a new rating entry is created.

    Inputs:
        user_id (int): ID of the user
        school_id (str): ID of the school
        value (int): Rating value (e.g. 1–5)

    Returns:
        dict: The rating dictionary after creation or update
    """
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
    """
    Clear all stored comments (primarily for testing purposes).

    Inputs:
        None

    Returns:
        None
    """
    COMMENTS.clear()


def add_comment_record(user_id: int,
                       school_id: str,
                       text: str,
                       created_at: Optional[datetime] = None) -> Dict:
    """
    Create a new comment entry and return it.

    Inputs:
        user_id (int): ID of the user adding the comment
        school_id (str): ID of the school being commented on
        text (str): Comment text (already validated)
        created_at (datetime | None): Optional timestamp. If None, now() is used.

    Returns:
        dict: The created comment dictionary with keys:
              'user_id', 'school_id', 'text', 'created_at'
    """
    if created_at is None:
        created_at = datetime.utcnow()

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
    """
    Rate a school for the currently logged-in user (US14).

    This function will:
        - ensure a user is logged in
        - ask the user for a school identifier
        - ask for a rating value
        - validate the rating using validate_rating_input
        - store or update the rating in RATINGS

    Inputs:
        input_func (Callable[[str], str]): function used to obtain user input
        print_func (Callable[[str], None]): function used to print messages

    Returns:
        Tuple[bool, object]:
            - (True, rating_dict) on success, where rating_dict is like:
                {
                    "user_id": int,
                    "school_id": str,
                    "value": int
                }
            - (False, error_message) on failure
    """

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
            # Otherwise loop again and ask for rating_input.
            continue

        # At this point we have a valid rating.
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
    """
    Add a comment to a school for the currently logged-in user (US15).

    This function will:
        - ensure a user is logged in
        - ask the user for a school identifier
        - ask for a comment text
        - validate the comment (non-empty, max_length)
        - store the comment in COMMENTS with a timestamp

    Inputs:
        input_func (Callable[[str], str]): function used to obtain user input
        print_func (Callable[[str], None]): function used to print messages
        max_length (int): maximum allowed length for the comment text

    Returns:
        Tuple[bool, object]:
            - (True, comment_dict) on success, where comment_dict is like:
                {
                    "user_id": int,
                    "school_id": str,
                    "text": str,
                    "created_at": datetime
                }
            - (False, error_message) on failure
    """

    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to add a comment"
        print_func(msg)
        return False, msg

    # Prompt for the school identifier.
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

    # Prompt for the comment text.
    while True:
        raw_text = input_func("Enter your comment: ")
        if raw_text is None:
            raw_text = ""

        stripped = raw_text.strip()

        # Allow user to cancel from this prompt as well.
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
            # Valid comment text.
            comment = add_comment_record(
                user_id=current_user["user_id"],
                school_id=school_id,
                text=stripped,
            )
            msg = "Comment added successfully."
            print_func(msg)
            return True, comment
        # If we reach this point, loop continues for another attempt.
