"""
Authentication and registration logic for US21
"""

from typing import Callable, Tuple, Optional, List, Dict
from .data_store import get_users, add_user


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

    if not username or username.strip() == "":
        return False, "Username cannot be empty"

    username = username.strip()

    if len(username) < 5:
        return False, "Username must be at least 5 characters long"

    if find_user_by_username(users, username) is not None:
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

    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

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

    print_func("User Login")

    if not users:
        print_func("No users are registered yet. Please register first")
        return False, "No registered users"

    username = input_func("Enter your Username: ").strip()
    user = find_user_by_username(users, username)

    if user is None:
        print_func("Username not found")
        return False, "Username not found"

    password = input_func("Enter your Password: ")

    if password != user.get("password"):
        print_func("incorrect password")
        return False, "Incorrect password"

    print_func("Login Successful, Welcome back {}".format(username))
    return True, user