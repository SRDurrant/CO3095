from typing import Callable
from app.data_store import get_users
from app.data_store import add_school
from app.data_store import get_schools
from app.data_store import get_next_school_id
from app.reviews import COMMENTS
from app.validation import (
    validate_school_name,
    validate_school_level,
    validate_school_location,
    check_duplicate_school,
    validate_school_id_exists
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


def delete_school_by_id(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> bool:
    """
    US4 - Delete School
    As an admin, I want to delete a school, so the system avoids duplicates
    and outdated records.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output

    Returns:
        bool: True if deletion successful, False otherwise
    """

    schools = get_schools()

    print_func("\n=== Delete a School ===")

    if not schools:
        print_func("No schools found in the system.")
        print_func("Press '0' to return to the main menu")
        input_func("")
        return False

    # Display all schools
    for school in schools:
        school_id = school.get("school_id", "?")
        name = school.get("name", "?")
        level = school.get("level", "?")
        location = school.get("location", "?")

        print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location}")

    # Prompt for school ID to delete
    while True:
        print_func("\nType '0' to return to the main menu")
        school_id_input = input_func("Enter the school ID to delete: ").strip()

        if school_id_input == "0":
            print_func("\nSchool deletion cancelled. Returning to main menu.")
            return False

        # Validate input is not empty
        if not school_id_input:
            print_func("Error: School ID cannot be empty.")
            continue

         # Validate input is numeric
        if not school_id_input.isdigit():
            print_func("Error: School ID must be a number.")
            continue

        school_id = int(school_id_input)

        # Validate school exists
        school_exists, error_msg_id = validate_school_id_exists(schools, school_id)
        if not school_exists:
            print_func(f"Error: {error_msg_id}")
            continue

        # Finds and deletes the school
        for i, school in enumerate(schools):
            if school.get("school_id") == school_id:
                deleted_school = schools.pop(i)
                print_func(f"\n (ID {school_id}):'{deleted_school['name']}' has been deleted.")
                return True


def update_school_by_id(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> bool:
    """
    US3 - Update School Details
    As an admin, I want to update school information so that inaccurate
    information can be corrected.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output

    Returns:
        bool: True if update successful, False otherwise
    """

    schools = get_schools()

    print_func("\n=== Update School Details ===")

    if not schools:
        print_func("No schools found in the system.")
        print_func("Press '0' to return to the main menu")
        input_func("")
        return False

    # Display all schools
    for school in schools:
        school_id = school.get("school_id", "?")
        name = school.get("name", "?")
        level = school.get("level", "?")
        location = school.get("location", "?")

        print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location}")

    # Prompt for school ID to update
    while True:
        print_func("\nType '0' to return to the main menu")
        school_id_input = input_func("Enter the school ID to update: ").strip()

        if school_id_input == "0":
            print_func("\nSchool update cancelled. Returning to main menu.")
            return False

        # Validate input is not empty
        if not school_id_input:
            print_func("Error: School ID cannot be empty.")
            continue

        # Validate input is numeric
        if not school_id_input.isdigit():
            print_func("Error: School ID must be a number.")
            continue

        school_id = int(school_id_input)

        # Validate school exists
        school_exists, error_msg_id = validate_school_id_exists(schools, school_id)
        if not school_exists:
            print_func(f"Error: {error_msg_id}")
            continue

        # Find the school to update
        school_to_update = None
        for school in schools:
            if school.get("school_id") == school_id:
                school_to_update = school
                break

        # Update school name
        while True:
            current_name = school_to_update.get("name", "")
            print_func(f"\nCurrent name: {current_name}")
            new_name = input_func("Enter new school name (or press Enter to keep current): ").strip()

            if new_name == "0":
                print_func("\nSchool update cancelled. Returning to main menu.")
                return False

            if new_name == "":
                new_name = current_name
                break

            is_valid_name, err_msg_name = validate_school_name(new_name)
            if not is_valid_name:
                print_func(f"Error: {err_msg_name}")
                continue

            break

        # Update school level
        while True:
            current_level = school_to_update.get("level", "")
            print_func(f"\nCurrent level: {current_level.capitalize()}")
            print_func("Select new level taught at school:")
            print_func("1. Primary")
            print_func("2. Secondary")
            print_func("3. Combined")
            print_func("Press Enter to keep current level")

            level_input = input_func("Enter choice (1-3): ").strip()

            if level_input == "0":
                print_func("\nSchool update cancelled. Returning to main menu.")
                return False

            if level_input == "":
                level_input = "1" if current_level == "primary" else "2" if current_level == "secondary" else "3"
                break

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

        new_level = level_map[level_input]

        # Update school location
        while True:
            current_location = school_to_update.get("location", "")
            print_func(f"\nCurrent location: {current_location}")
            new_location = input_func("Enter new school location (or press Enter to keep current): ").strip()

            if new_location == "0":
                print_func("\nSchool update cancelled. Returning to main menu.")
                return False

            if new_location == "":
                new_location = current_location
                break

            is_valid_location, err_msg_location = validate_school_location(new_location)
            if not is_valid_location:
                print_func(f"Error: {err_msg_location}")
                continue

            # Check for duplicate school (same name and location) excluding current school
            other_schools = [s for s in schools if s.get("school_id") != school_id]
            is_unique, err_msg_dupli = check_duplicate_school(other_schools, new_name, new_location)
            if not is_unique:
                print_func(f"Error: {err_msg_dupli}")
                continue

            break

        # Update the school
        school_to_update["name"] = new_name
        school_to_update["level"] = new_level
        school_to_update["location"] = new_location

        print_func(f"\nSchool (ID {school_id}) has been successfully updated.")
        return True


def delete_comment_by_id(
        comment_id: int,
        print_func: Callable = print
) -> bool:
    """
    USX – Admin deletes an inappropriate comment.
    Admins maintain quality by removing comments.

    Inputs:
        comment_id (int): ID of comment in COMMENTS list (index+1)
        print_func (Callable): for testing

    Returns:
        bool: True if deletion successful, False if comment does not exist
    """

    # Comments currently do not store IDs. We simulate ID = index+1.
    for i, comment in enumerate(COMMENTS):
        if (i + 1) == comment_id:
            deleted = COMMENTS.pop(i)
            print_func(f"Comment #{comment_id} from user {deleted['user_id']} has been deleted.")
            return True

    print_func("Error: Comment does not exist.")
    return False
