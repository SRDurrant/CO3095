"""
Authentication and registration logic for US21
"""

from typing import Callable, Tuple, Optional, List, Dict
from .data_store import get_users, add_user
from .validation import validate_username_format, validate_password_format
from app.system_log import log_event, log_error


def find_user_by_username(users: List[Dict], username: str):
    """
    Find a user by username

    Inputs:
        users (List[Dict]): list of users dictionaries
        username (str): the username to search for

    Returns:
        Optional[Dict]: The matched user dictionary if found, else None
    """

    for user in users:
        if user['username'] == username:
            return user
    return None


def get_next_user_id(users: List[Dict]) -> int:
    """
    Gets the next available user ID based on the existing users

    Inputs:
        users (List[Dict]): list of users dictionaries

    Returns:
        int: next available user ID, assigned as max(existing IDs) + 1 or 1 if the list is empty
    """

    if not users:
        return 1
    existing_ids = [u.get("user_id", 0) for u in users]
    return max(existing_ids) + 1


def validate_new_username(users: List[Dict], username: str) -> Tuple[bool, str]:
    """
    Validate the username rules for registration

    Inputs:
        users (List[Dict]): list of users dictionaries
        username (str): the username provided by the user

    Returns:
        Tuple[bool, str]:
            - bool: True if the username is valid, False otherwise
            - str: "Username Valid" or the error message describing the failure reason
    """

    is_valid_format, msg = validate_username_format(username)
    if not is_valid_format:
        return False, msg

    cleaned = username.strip()

    if find_user_by_username(users, cleaned) is not None:
        return False, "Username already exists"

    return True, "Username valid"


def validate_new_password(password: str, confirm: Optional[str] = None) -> Tuple[bool, str]:
    """
    Validate the password rules for registration

    Inputs:
        password (str): the password provided by the user
        confirm (Optional[str]): confirm the password provided by the user

    Returns:
        Tuple[bool, str]:
            - bool: True if the password is valid, False otherwise
            - str: "Password Valid" or the error message describing the failure reason
    """

    is_valid, msg = validate_password_format(password)
    if not is_valid:
        return False, msg

    if confirm is not None and password != confirm:
        return False, "Passwords must match"

    return True, "Password valid"


def register_user(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> Tuple[bool, object]:
    """
    Register for a new user and them to the global list of users

    Inputs:
        input_func(Callable[[str], str]): function that takes a username and a password and returns a boolean
        print_func(Callable[[str], None]): function that prints a message

    Returns:
        Tuple[bool, object]:
            - True, user_dict (Dict) on a successful registration
            Example user_dict:
                {
                "user_id": int,
                "username": str,
                "password": str,
                "role": str
                }
            - False, error_message (str) on failure
    """

    users = get_users()

    print_func("User Registration")

    username = input_func("Enter your Username: ").strip()
    is_valid, msg = validate_new_username(users, username)
    if not is_valid:
        print_func(f"Invalid Username: {msg}")
        return False, msg

    password = input_func("Enter your Password: ")
    confirm_password = input_func("Confirm your Password: ")
    is_valid_pw, msg_pw = validate_new_password(password, confirm_password)
    if not is_valid_pw:
        print_func(f"Invalid Password: {msg_pw}")
        return False, msg_pw

    new_user = {
        "user_id": get_next_user_id(users),
        "username": username,
        "password": password,
        "role": "student"           # Default role for new Logged in Users
    }

    add_user(new_user)
    log_event(f"New user registered: {username} (ID {new_user['user_id']})")

    print_func("Registration Successful: Welcome {}".format(username))
    return True, new_user


def login_user(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> Tuple[bool, object]:
    """
    Login for a existing user by checking their username and password

    Inputs:
        input_func(Callable[[str], str]): function that is used to recieve a username and a password
        print_func(Callable[[str], None]): function that prints a message

    Returns:
        Tuple[bool, object]:
            - True, user_dict (Dict) on a successful login
            - False, error_message (str) on failure
    """

    users = get_users()

    print_func("\nUser Login")

    if not users:
        print_func("\nNo registered users. Please register first")
        return False, "\nNo registered users"

    while True:
        print_func("\nEnter your Login details")
        print_func("Type '0' at any prompt to return to the main menu")

        username = input_func("Enter your Username: ").strip()
        if username == "0":
            print_func("\nReturning to the main menu without logging in")
            return False, "\nLogin cancelled"

        user = find_user_by_username(users, username)
        if user is None:
            print_func("\nLogin failed: Username not found")
            # Keeps the user in the loop and lets them try again
            continue

        password = input_func("Enter your Password: ")
        if password == "0":
            print_func("\nReturning to the main menu without logging in")
            return False, "\nLogin cancelled"

        if password != user.get("password"):
            print_func("\nLogin failed: Incorrect password")
            # Keeps the user in the loop and lets them try again
            log_error(f"Login failed for username '{username}'")
            continue

        # if log in is successful
        from .data_store import set_current_user
        set_current_user(user)
        log_event(f"User logged in: {username}")
        print_func("\nLogin successful, welcome {}".format(username))
        return True, user


def reset_password(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> Tuple[bool, object]:
    """
    Allows a user to reset their password if they forget it, using their username

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output/messages

    Returns:
        Tuple[bool, object]:
            - True, updated_user_dict (Dict) on success
            - False, error_message (str) on failure/cancel
    """

    users = get_users()

    print_func("\nPassword Reset")

    if not users:
        msg = "No registered users. Please register first"
        print_func(f"\n{msg}")
        return False, f"\n{msg}"

    while True:
        print_func("\nEnter your username to reset password")
        print_func("Type '0' to return to the main menu")

        username = input_func("Username: ").strip()
        if username == "0":
            msg = "\nPassword reset cancelled"
            print_func(msg)
            return False, msg

        user = find_user_by_username(users, username)
        if user is None:
            print_func("\nPassword reset failed: Username not found")
            continue

        new_password = input_func("Enter your new password: ")
        if new_password == "0":
            msg = "\nPassword reset cancelled"
            print_func(msg)
            return False, msg

        confirm_password = input_func("Confirm your new password: ")
        if confirm_password == "0":
            msg = "\nPassword reset cancelled"
            print_func(msg)
            return False, msg

        is_valid_pw, msg_pw = validate_new_password(new_password, confirm_password)
        if not is_valid_pw:
            print_func(f"\nInvalid Password: {msg_pw}")
            continue

        user["password"] = new_password
        print_func("\nPassword reset successful.")
        return True, user