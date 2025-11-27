"""
Authentication and registration logic for US21
"""

from typing import Callable, Tuple, Optional, List, Dict
from .data_store import get_users, add_user

def find_user_by_username(users: List[Dict], username: str):
    """returns the user dict if the username exists already, if it doesn't None"""
    for user in users:
        if user['username'] == username:
            return user
    return None

def get_next_user_id(users: List[Dict]) -> int:
    """returns the next user id if it exists, else return None"""
    if not users:
        return 1
    exisiting_ids = [u.get("user_id", 0) for u in users]
    return max(exisiting_ids) + 1

def validate_new_username(users: List[Dict], username: str) -> Tuple[bool, str]:
    """validates the username exists, if it doesn't exist, return False and a message"""
    if not username or username.strip() == "":
        return False, "Username cannot be empty"

    username = username.strip()

    if len(username) < 5:
        return False, "Username must be at least 5 characters long"

    if find_user_by_username(users, username) if not None:
        return False, "Username already exists"

    return True, "Username valid"

def validate_new_password(password: str, confirm: Optional[str] = None) -> Tuple[bool, str]:
    """validates the password of the user"""

    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if confirm is not None and password != confirm:
        return False, "Password and confirm must match"

    return True, "Password valid"

def register_user(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
):
    """
    Register for a new user and them to the global list of users

    Returns:
        (True, user_dict) on success
        (False, error_message) on failure
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