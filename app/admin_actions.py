from typing import Callable
from app.data_store import get_users
from app.data_store import add_school
from app.data_store import get_schools
from app.data_store import get_next_school_id
from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school
)


def list_all_users(print_func=print) -> None:
    """
    US - Admin View All Registered Users
    Allows an administrator to see all registered users.

    Inputs:
        print_func (Callable): Function used to print output (for testing)

    Returns:
        None
    """

    users = get_users()

    if not users:
        print_func("\nNo users found in the system.")
        return

    print_func("\n=== Registered Users ===")
    for user in users:
        uid = user.get("user_id", "?")
        username = user.get("username", "?")
        role = user.get("role", "?")

        print_func(f"ID: {uid} | Username: {username} | Role: {role}")


def delete_user_by_id(user_id: int, print_func: Callable = print) -> bool:
    """
    US33 – Admin deletes abusive/fake user accounts.

    Admin accounts cannot be deleted.

    Inputs:
        user_id (int): ID of the user to delete
        print_func (Callable): Injected print function for testing

    Returns:
        bool: True if deletion successful, False otherwise
    """

    users = get_users()

    for i, user in enumerate(users):
        if user.get("user_id") == user_id:
            if user.get("role") == "admin":
                print_func("Error: Admin accounts cannot be deleted.")
                return False

            deleted_user = users.pop(i)
            print_func(f"User '{deleted_user['username']}' (ID {user_id}) has been deleted.")
            return True

    print_func("Error: User does not exist.")
    return False


def add_new_school(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> bool:
    """
    US1 - Create the Schools
    As an administrator, I want to add a new school to the system so that it can be evaluated by users.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output

    Returns:
        bool: True if school was successfully added, False otherwise
    """

    schools = get_schools()

    print_func("\n=== Add a New School ===")
    print_func("Type '0' at any prompt to cancel and return to the main menu")


    # Obtain and validate school name
    while True:
        name = input_func("Enter school name: ").strip()

        if name == "0":
            print_func("\nSchool creation cancelled. Returning to main menu.")
            return False

        is_valid_name, err_msg_name = validate_school_name(name)
        if not is_valid_name:
            print_func(f"Error: {err_msg_name}")
            continue

        break

    # Obtain and validate level taught at school
    while True:
        print_func("\nSelect level taught at school:")
        print_func("1. Primary")
        print_func("2. Secondary")
        print_func("3. Combined")

        level_input = input_func("Enter choice (1-3): ").strip()

        if level_input == "0":
            print_func("\nSchool creation cancelled. Returning to main menu.")
            return False

        is_valid_level, err_msg_level = validate_school_level(level_input)
        if not is_valid_level:
            print_func(f"Error: {err_msg_level}")
            continue

        break

    level_map = {
        "1": "primary",
        "2": "secondary",
        "3": "combined"
    }

    level = level_map[level_input]

    # Obtain and validate school location
    while True:
        location = input_func("Enter school location: ").strip()

        if location == "0":
            print_func("\nSchool creation cancelled. Returning to main menu.")
            return False

        is_valid_location, err_msg_location = validate_school_location(location)
        if not is_valid_location:
            print_func(f"Error: {err_msg_location}")
            continue

        # Check for duplicate school (same name and location)
        is_unique, err_msg_dupli = check_duplicate_school(schools, name, location)
        if not is_unique:
            print_func(f"Error: {err_msg_dupli}")
            continue

        break


    # Create new school dictionary
    new_school = {
        "school_id": get_next_school_id(schools),
        "name": name,
        "level": level,
        "location": location
    }

    # Add school to global list of schools
    add_school(new_school)

    print_func(f"\nSchool '{name}' has been successfully added.")
    return True
