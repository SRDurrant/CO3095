"""
For school-related actions for the system

Implements:
- US6 - List All Schools
- US5 - View School Profile
"""

from typing import Callable
from app.data_store import get_schools
from app.validation import validate_school_id_exists

def list_all_schools(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    US6 - List All Schools
    As a user, I want to see a full list of schools, so I can browse available options.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable): Function used to print output (for testing)

    Returns:
        None
    """

    schools = get_schools()

    while True:
        if not schools:
            print_func("\nNo schools found in the system.")
            print_func("Press '0' to return to the main menu")
            input_func("")
            return

        print_func("\n=== Schools ===")
        for school in schools:
            school_id = school.get("school_id", "?")
            name = school.get("name", "?")

            print_func(f"ID: {school_id} | Name: {name}")

        print_func("\n1. View School Profile")
        print_func("0. Return to Main Menu")

        choice = input_func("Select an option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            # View School Profile
            view_school_profile(input_func, print_func)

        else:
            print_func("Invalid option, please try again")


def view_school_profile(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> bool:
    """
    US5 - View School Profile
    As a user, I want to view detailed information about a school, so I can understand its characteristics.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable): Function used to print output (for testing)

    Returns:
        bool: True if profile was viewed, False if cancelled
    """

    schools = get_schools()

    print_func("\n=== View School Profile ===")

    for school in schools:
        school_id = school.get("school_id", "?")
        name = school.get("name", "?")

        print_func(f"ID: {school_id} | Name: {name}")

    # Prompt for school ID to view
    while True:
        print_func("\nType '0' to return to schools list")
        school_id_input = input_func("Enter the school ID to view profile: ").strip()

        if school_id_input == "0":
            print_func("\nReturning to schools list.")
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
        school_exists, error_msg = validate_school_id_exists(schools, school_id)
        if not school_exists:
            print_func(f"Error: {error_msg}")
            continue

        # Find and display the school
        for school in schools:
            if school.get("school_id") == school_id:
                print_func("\n=== School Details ===")
                print_func(f"School ID: {school.get('school_id', '?')}")
                print_func(f"Name: {school.get('name', '?')}")
                print_func(f"Level: {school.get('level', '?').capitalize()}")
                print_func(f"Location: {school.get('location', '?')}")

                print_func("\nPress any key to return to schools list")
                input_func("")
                return True
