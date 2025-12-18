"""
For school-related actions for the system

Implements:
- US6 - List All Schools
- US5 - View School Profile
- US11 - View School Rankings for Each Category (Level)
- US8 - Search Schools by Name
"""

from typing import Callable, Dict
from collections import defaultdict

from app.data_store import get_schools
from app.validation import validate_school_id_exists
from app.reviews import RATINGS


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

    while True:
        print_func("\nType '0' to return to schools list")
        school_id_input = input_func("Enter the school ID to view profile: ").strip()

        if school_id_input == "0":
            print_func("\nReturning to schools list.")
            return False

        if not school_id_input:
            print_func("Error: School ID cannot be empty.")
            continue

        if not school_id_input.isdigit():
            print_func("Error: School ID must be a number.")
            continue

        school_id = int(school_id_input)

        school_exists, error_msg = validate_school_id_exists(schools, school_id)
        if not school_exists:
            print_func(f"Error: {error_msg}")
            continue

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


def _calculate_average_ratings() -> Dict[str, float]:
    """
    US11 helper: Calculate average rating for each school_id from RATINGS.

    Inputs:
        None

    Returns:
        Dict[str, float]: Mapping of school_id (string) to average rating
    """

    totals: Dict[str, int] = {}
    counts: Dict[str, int] = {}

    for rating in RATINGS:
        school_id = str(rating.get("school_id"))
        value = rating.get("value")

        if school_id is None or value is None:
            continue

        totals[school_id] = totals.get(school_id, 0) + int(value)
        counts[school_id] = counts.get(school_id, 0) + 1

    averages: Dict[str, float] = {}
    for sid, total in totals.items():
        averages[sid] = total / counts[sid]

    return averages


def view_school_rankings(print_func: Callable[[str], None] = print) -> None:
    """
    US11 – View school rankings for each category (level)
    Shows all schools sorted by average rating within each level.

    Inputs:
        print_func (Callable[[str], None]): Function used to print output (for testing)

    Returns:
        None
    """

    schools = get_schools()
    if not schools:
        print_func("No schools available.")
        return

    averages = _calculate_average_ratings()
    grouped = defaultdict(list)

    for school in schools:
        level = school.get("level", "unknown")
        avg = averages.get(str(school.get("school_id")), 0.0)
        grouped[level].append((school, avg))

    for level, items in grouped.items():
        print_func(f"\n=== {str(level).capitalize()} Schools Ranking ===")
        items.sort(key=lambda x: x[1], reverse=True)

        for school, avg in items:
            print_func(
                f"ID {school.get('school_id')} | {school.get('name')} | Avg Rating: {avg:.2f}"
            )


def search_schools_by_name(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    US8 - Search Schools by Name
    As a user, I want to search schools using a keyword so I can quickly
    find a specific school.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output (for testing)

    Returns:
        None
    """


    schools = get_schools()

    while True:
        print_func("\n=== Search Schools ===")
        print_func("Type '0' to return to the main menu")

        keyword = input_func("Enter search: ").strip()

        if keyword == "0":
            print_func("\nReturning to main menu.")
            return

        if not keyword:
            print_func("Error: Search cannot be empty.")
            continue

        # Searches for matches
        keyword_lower = keyword.lower()
        matching_schools = [
            school for school in schools
            if keyword_lower in school.get("name", "").lower()
        ]

        if not matching_schools:
            print_func(f"\nNo schools found matching '{keyword}'.")
            print_func("Try a different search or press '0' to return.")
            continue

        print_func(f"\n=== Search Results for '{keyword}' ===")
        print_func(f"Found {len(matching_schools)} school(s):\n")

        for school in matching_schools:
            school_id = school.get("school_id", "?")
            name = school.get("name", "?")

            print_func(f"ID: {school_id} | Name: {name}")

        print_func("\n1. View School Profile")
        print_func("2. Search Again")
        print_func("0. Return to Main Menu")

        choice = input_func("Select an option: ").strip()

        if choice == "0":
            print_func("\nReturning to main menu.")
            return

        elif choice == "1":
            for school in matching_schools:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                level = school.get("level", "?")
                location = school.get("location", "?")

                print_func(f"ID: {school_id}")
                print_func(f"Name: {name}")
                print_func(f"Level: {level.capitalize()}")
                print_func(f"Location: {location}")
                print_func("\nEnter any key to return to search page")
                input_func("")
                continue

        elif choice == "2":
            continue

        else:
            print_func("Invalid option, please try again")
