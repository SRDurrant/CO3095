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
from .data_store import get_current_user, SCHOOLS
from .validation import validate_rating_input

RATINGS: List[Dict] = []
COMMENTS: List[Dict] = []
FAVOURITES: List[Dict] = []

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

def clear_favourites() -> None:
    """
    Clears all favourites (test helper).
    """
    FAVOURITES.clear()


def find_favourite(user_id: int, school_id: str) -> Optional[Dict]:
    """
    Returns a favourite record if it exists for a (user, school) pair.
    """
    for fav in FAVOURITES:
        if fav.get("user_id") == user_id and fav.get("school_id") == school_id:
            return fav
    return None


def add_favourite_record(user_id: int, school_id: str, created_at: Optional[datetime] = None) -> Dict:
    """
    Creates and stores a favourite record.
    """
    if created_at is None:
        created_at = datetime.now(timezone.utc)

    fav = {
        "user_id": user_id,
        "school_id": school_id,
        "created_at": created_at,
    }
    FAVOURITES.append(fav)
    return fav

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

def get_comments_for_school(school_id: str, newest_first: bool = True) -> List[Dict]:
    matching = [c for c in COMMENTS if c.get("school_id") == school_id]
    matching.sort(key=lambda c: c["created_at"], reverse=newest_first)
    return matching

def view_comments_for_school(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:
    print_func("\nView Comments for a School")
    print_func("Type '0' to return to the previous menu.")
    school_id = input_func("Enter the school ID to view comments: ").strip()
    if school_id == "0":
        msg = "Viewing comments cancelled by user"
        print_func(msg)
        return False, msg
    if not school_id:
        msg = "School ID cannot be empty."
        print_func(msg)
        return False, msg
    comments = get_comments_for_school(school_id)
    if not comments:
        msg = f"No comments found for school '{school_id}'."
        print_func(msg)
        return True, []
    print_func(f"\nComments for school '{school_id}':")
    for c in comments:
        ts = c["created_at"].strftime("%Y-%m-%d %H:%M:%S UTC")
        print_func(f"- ({ts}) User {c['user_id']}: {c['text']}")
    return True, comments


def get_user_comments_for_school(user_id: int, school_id: str) -> List[Dict]:
    """
    Return comments for a specific (user, school) pair.
    """
    return [c for c in COMMENTS if c.get("user_id") == user_id and c.get("school_id") == school_id]


def edit_comment_record(comment: Dict, new_text: str, max_length: int = 500) -> Tuple[bool, str]:
    """
    Edit the text of a specific comment dict with basic validation.
    """
    if new_text is None:
        return False, "Comment cannot be empty."

    stripped = new_text.strip()

    if stripped == "":
        return False, "Comment cannot be empty."

    if len(stripped) > max_length:
        return False, f"Comment must be at most {max_length} characters."

    comment["text"] = stripped
    comment["created_at"] = datetime.now(timezone.utc)  # treat edit as updated timestamp
    return True, "OK"


def edit_my_comment(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
    max_length: int = 500,
) -> Tuple[bool, object]:
    """
    US16 - Edit My Comment

    Flow:
    - user must be logged in
    - ask for school id
    - show only the user's comments for that school
    - user selects which comment to edit
    - validate new comment text and update in place
    """
    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to edit a comment"
        print_func(msg)
        return False, msg

    print_func("\nEdit My Comment")
    print_func("Type '0' at any prompt to return to the previous menu.")

    school_id = input_func("Enter the school ID to edit a comment on: ").strip()
    if school_id == "0":
        msg = "Edit comment cancelled by user"
        print_func(msg)
        return False, msg
    if not school_id:
        msg = "School ID cannot be empty."
        print_func(msg)
        return False, msg

    user_id = current_user["user_id"]
    mine = get_user_comments_for_school(user_id, school_id)

    if not mine:
        msg = f"No comments found for you on school '{school_id}'."
        print_func(msg)
        return True, []

    print_func(f"\nYour comments for school '{school_id}':")
    for i, c in enumerate(mine, start=1):
        ts = c["created_at"].strftime("%Y-%m-%d %H:%M:%S UTC")
        print_func(f"{i}. ({ts}) {c['text']}")

    while True:
        choice = input_func("Select comment number to edit: ").strip()
        if choice == "0":
            msg = "Edit comment cancelled by user"
            print_func(msg)
            return False, msg

        if not choice.isdigit():
            print_func("Invalid option, please try again")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(mine):
            print_func("Invalid option, please try again")
            continue

        target = mine[idx - 1]
        break

    while True:
        new_text = input_func("Enter the updated comment text: ")
        if new_text is None:
            new_text = ""
        if new_text.strip() == "0":
            msg = "Edit comment cancelled by user"
            print_func(msg)
            return False, msg

        ok, message = edit_comment_record(target, new_text, max_length=max_length)
        if not ok:
            print_func(message)
            print_func("Type '0' to cancel or enter a new comment.")
            continue

        msg = "Comment updated successfully."
        print_func(msg)
        return True, target


def get_average_rating_for_school(school_id: str) -> Optional[float]:
    """
    US19 helper: compute average rating for a school.

    Inputs:
        school_id (str): school identifier to compute average for

    Returns:
        float | None:
            - average rating if at least one rating exists
            - None if no ratings exist for that school
    """
    matching = [r for r in RATINGS if r.get("school_id") == school_id]
    if not matching:
        return None

    total = sum(int(r.get("value", 0)) for r in matching)
    return total / len(matching)


def view_average_rating_for_school(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:
    """
    US19 - View Average Rating for a School

    Flow:
    - ask for school ID
    - allow cancel with '0'
    - validate school id not empty
    - compute average from RATINGS
    - if none found, return True with None
    - else print average and return it
    """
    print_func("\nView Average Rating for a School")
    print_func("Type '0' to return to the previous menu.")

    school_id = input_func("Enter the school ID to view average rating: ").strip()

    if school_id == "0":
        msg = "Viewing average rating cancelled by user"
        print_func(msg)
        return False, msg

    if not school_id:
        msg = "School ID cannot be empty."
        print_func(msg)
        return False, msg

    avg = get_average_rating_for_school(school_id)

    if avg is None:
        msg = f"No ratings found for school '{school_id}'."
        print_func(msg)
        return True, None

    msg = f"Average rating for school '{school_id}': {avg:.2f}"
    print_func(msg)
    return True, avg


def delete_comment_record(comment: Dict) -> Dict:
    """
    Delete a specific comment dict from COMMENTS.

    Inputs:
        comment (dict): comment dict to remove

    Returns:
        dict: the removed comment
    """
    COMMENTS.remove(comment)
    return comment


def delete_my_comment(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:
    """
    US17 - Delete My Comment

    Flow:
    - user must be logged in
    - ask for school id
    - list only the user's comments for that school
    - user selects which comment to delete
    - deletes it from COMMENTS
    """
    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to delete a comment"
        print_func(msg)
        return False, msg

    print_func("\nDelete My Comment")
    print_func("Type '0' at any prompt to return to the previous menu.")

    school_id = input_func("Enter the school ID to delete a comment from: ").strip()
    if school_id == "0":
        msg = "Delete comment cancelled by user"
        print_func(msg)
        return False, msg

    if not school_id:
        msg = "School ID cannot be empty."
        print_func(msg)
        return False, msg

    user_id = current_user["user_id"]
    mine = get_user_comments_for_school(user_id, school_id)

    if not mine:
        msg = f"No comments found for you on school '{school_id}'."
        print_func(msg)
        return True, []

    print_func(f"\nYour comments for school '{school_id}':")
    for i, c in enumerate(mine, start=1):
        ts = c["created_at"].strftime("%Y-%m-%d %H:%M:%S UTC")
        print_func(f"{i}. ({ts}) {c['text']}")

    while True:
        choice = input_func("Select comment number to delete: ").strip()
        if choice == "0":
            msg = "Delete comment cancelled by user"
            print_func(msg)
            return False, msg

        if not choice.isdigit():
            print_func("Invalid option, please try again")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(mine):
            print_func("Invalid option, please try again")
            continue

        target = mine[idx - 1]
        deleted = delete_comment_record(target)

        msg = "Comment deleted successfully."
        print_func(msg)
        return True, deleted

def get_favourites_for_user(user_id: int) -> List[Dict]:
    """
    Returns all favourite records for a given user.
    """
    return [f for f in FAVOURITES if f.get("user_id") == user_id]


def _find_school_name(school_id: str) -> Optional[str]:
    """
    Best-effort helper to show school name if SCHOOLS is populated.
    """
    for s in SCHOOLS:
        if str(s.get("school_id")) == str(school_id):
            return s.get("name")
    return None


def favourite_school(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:
    """
    US26 - Favourite a School

    Flow:
    - user must be logged in
    - user must be a student
    - prompt for school_id
    - '0' cancels
    - empty school_id rejected (re-prompt)
    - if already favourited -> no duplicate, return success
    - else store favourite record and return success
    """
    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to favourite a school"
        print_func(msg)
        return False, msg

    if current_user.get("role") != "student":
        msg = "Only students can favourite a school"
        print_func(msg)
        return False, msg

    print_func("\nFavourite a School")
    print_func("Type '0' at any prompt to return to the previous menu.")

    while True:
        school_id = input_func("Enter the school ID to favourite: ").strip()

        if school_id == "0":
            msg = "Favourite cancelled by user"
            print_func(msg)
            return False, msg

        if not school_id:
            print_func("School ID cannot be empty.")
            continue

        existing = find_favourite(current_user["user_id"], school_id)
        if existing is not None:
            msg = f"School '{school_id}' is already in your favourites."
            print_func(msg)
            return True, existing

        fav = add_favourite_record(current_user["user_id"], school_id)
        msg = f"School '{school_id}' added to favourites."
        print_func(msg)
        return True, fav


def view_favourite_schools(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> Tuple[bool, object]:
    """
    US28 - View Favourite Schools
    """
    current_user = get_current_user()
    if current_user is None:
        msg = "You must be logged in to view favourites"
        print_func(msg)
        return False, msg

    print_func("\nView Favourite Schools")
    print_func("Type '0' to return to the previous menu.")
    choice = input_func("Press Enter to view favourites (or 0 to cancel): ").strip()

    if choice == "0":
        msg = "Viewing favourites cancelled by user"
        print_func(msg)
        return False, msg

    favs = get_favourites_for_user(current_user["user_id"])
    if not favs:
        msg = "You have no favourite schools yet."
        print_func(msg)
        return True, []

    print_func("\nYour favourite schools:")
    for f in favs:
        sid = f.get("school_id")
        name = _find_school_name(str(sid))
        if name:
            print_func(f"- {sid}: {name}")
        else:
            print_func(f"- {sid}")

    return True, favs
