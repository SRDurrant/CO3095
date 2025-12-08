from typing import Callable
from app.data_store import get_users
from app.data_store import add_school
from app.data_store import get_schools
from app.data_store import get_next_school_id

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

    # Obtain school name
    name = input_func("Enter school name: ").strip()

    # Obtain level taught at school
    print_func("\nSelect level taught at school:")
    print_func("1. Primary")
    print_func("2. Secondary")
    print_func("3. Combined")

    level_choice = input_func("Enter choice (1-3): ").strip()

    level_map = {
        "1": "primary",
        "2": "secondary",
        "3": "combined"
    }

    level = level_map.get(level_choice, level_choice)

    # Obtain school location
    location = input_func("Enter school location: ").strip()

    # Create new school dictionary
    new_school = {
        "school_id": get_next_school_id(schools),
        "name": name,
        "level": level,
        "location": location
    }

    # Add school to global list of schools
    add_school(new_school)

    print_func(f"\nSchool '{name}' has been successfully added with ID {new_school['school_id']}.")
    return True
