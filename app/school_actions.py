"""
For school-related actions for the system

Implements:
- US5 - View School Profile
- US6 - List All Schools
- US7 - Filter Schools by Attributes
- US8 - Search Schools by Name
- US11 - View School Rankings for Each Category (Level)
- US12 - Shows top-performing schools per category
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
    averages = _calculate_average_ratings()

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
            avg = averages.get(str(school_id), 0.0)

            if avg > 0:
                print_func(f"ID: {school_id} | Name: {name} | Avg Rating: {avg:.2f}")
            else:
                print_func(f"ID: {school_id} | Name: {name} | Avg Rating: No ratings yet")

        print_func("\n1. View School Profile")
        print_func("2. Filter Schools")
        print_func("0. Return to Main Menu")

        choice = input_func("Select an option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            view_school_profile(input_func, print_func)

        elif choice == "2":
            filter_schools(input_func, print_func)

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
    averages = _calculate_average_ratings()

    print_func("\n=== View School Profile ===")

    for school in schools:
        school_id = school.get("school_id", "?")
        name = school.get("name", "?")
        print_func(f"ID: {school_id} | Name: {name}")

    while True:
        print_func("\nType '0' to return to list of schools")
        school_id_input = input_func("Enter the school ID to view profile: ").strip()

        if school_id_input == "0":
            print_func("\nExiting Viewing School Profile(s).")
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
                avg = averages.get(str(school_id), 0.0)

                print_func("\n=== School Details ===")
                print_func(f"School ID: {school.get('school_id', '?')}")
                print_func(f"Name: {school.get('name', '?')}")
                print_func(f"Level: {school.get('level', '?').capitalize()}")
                print_func(f"Location: {school.get('location', '?')}")

                if avg > 0:
                    print_func(f"Average Rating: {avg:.2f}")
                else:
                    print_func("Average Rating: No ratings yet")

                print_func("\nPress any key to exit")
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


def view_top_schools(limit: int = 3, print_func: Callable[[str], None] = print) -> None:
    """
    US12 – Shows top-performing schools per category

    Inputs:
        limit (int): number of top schools to show per level
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
        avg = averages.get(str(school.get("school_id")), 0.0)
        grouped[school.get("level", "unknown")].append((school, avg))

    for level, items in grouped.items():
        print_func(f"\n=== Top {limit} {str(level).capitalize()} Schools ===")
        items.sort(key=lambda x: x[1], reverse=True)

        for school, avg in items[:limit]:
            print_func(
                f"{school.get('name')} (ID {school.get('school_id')}) - Avg Rating: {avg:.2f}"
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
    averages = _calculate_average_ratings()

    while True:
        print_func("\n=== Search Schools ===")
        print_func("Type '0' to return to the main menu")

        keyword = input_func("Enter search: ").strip()

        if keyword == "0":
            print_func("\nReturning to Main Menu.")
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

        print_func("\n1. View School Profile(s)")
        print_func("2. Search Again")
        print_func("0. Return to Main Menu")

        choice = input_func("Select an option: ").strip()

        if choice == "0":
            print_func("\nReturning to Main Menu.")
            return

        elif choice == "1":
            for school in matching_schools:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                location = school.get("location", "?")
                avg = averages.get(str(school_id), 0.0)

                if avg > 0:
                    print_func(f"ID: {school_id} | Name: {name} | Location: {location} | Avg Rating: {avg:.2f}")
                else:
                    print_func(f"ID: {school_id} | Name: {name} | Location: {location} | Avg Rating: No ratings yet")

                print_func("\nPress any key to exit")
                input_func("")
                return

        elif choice == "2":
            continue

        else:
            print_func("Invalid option, please try again")


def filter_schools(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    US7 - Filter Schools by Attributes
    As a user, I want to filter schools by attributes such as location, type, or rating
    so I can find relevant results.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output (for testing)

    Returns:
        None
    """

    schools = get_schools()

    while True:
        print_func("\n=== Filter Schools ===")
        print_func("1. Filter by Location")
        print_func("2. Filter by Level")
        print_func("3. Filter by Minimum Rating")
        print_func("0. Return to Schools List")

        choice = input_func("Select filter type: ").strip()

        if choice == "0":
            print_func("\nExiting Filtering Schools.")
            return

        elif choice == "1":
            # Filter by location
            print_func("\nType '0' to cancel")
            location = input_func("Enter location to filter by: ").strip()

            if location == "0":
                print_func("\nExiting Filtering Schools.")
                return

            if not location:
                print_func("Error: Location cannot be empty.")
                continue

            location_lower = location.lower()
            filtered = [
                school for school in schools
                if location_lower in school.get("location", "").lower()
            ]

            if not filtered:
                print_func(f"\nNo schools found in location '{location}'.")
                continue

            averages = _calculate_average_ratings()

            print_func(f"\n=== Schools in '{location}' ===")
            print_func(f"Found {len(filtered)} school(s):\n")

            for school in filtered:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                level = school.get("level", "?")
                avg = averages.get(str(school_id), 0.0)

                if avg > 0:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Avg Rating: {avg:.2f}")
                else:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Avg Rating: No ratings yet")

            print_func("\nEnter any other key to return to Filter Menu")
            input_func("")
            continue

        elif choice == "2":
            # Filter by level
            print_func("\nSelect level:")
            print_func("1. Primary")
            print_func("2. Secondary")
            print_func("3. Combined")
            print_func("0. Cancel")

            level_choice = input_func("Enter choice (1-3): ").strip()

            if level_choice == "0":
                print_func("\nExiting Filtering Schools.")
                return

            level_map = {
                "1": "primary",
                "2": "secondary",
                "3": "combined"
            }

            if level_choice not in level_map:
                print_func("Error: Invalid selection.")
                continue

            selected_level = level_map[level_choice]
            filtered = [
                school for school in schools
                if school.get("level", "").lower() == selected_level
            ]

            if not filtered:
                print_func(f"\nNo {selected_level} schools found.")
                continue

            averages = _calculate_average_ratings()

            print_func(f"\n=== {selected_level.capitalize()} Schools ===")
            print_func(f"Found {len(filtered)} school(s):\n")

            for school in filtered:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                location = school.get("location", "?")
                avg = averages.get(str(school_id), 0.0)

                if avg > 0:
                    print_func(f"ID: {school_id} | Name: {name} | Location: {location} | Avg Rating: {avg:.2f}")
                else:
                    print_func(f"ID: {school_id} | Name: {name} | Location: {location} | Avg Rating: No ratings yet")

            print_func("\nEnter any other key to return to Filter Menu")
            input_func("")
            continue

        elif choice == "3":
            # Filter by minimum rating
            print_func("\nType '0' to cancel")
            min_rating_input = input_func("Enter minimum rating (1-5): ").strip()

            if min_rating_input == "0":
                print_func("\nExiting Filtering Schools.")
                return

            if not min_rating_input.isdigit():
                print_func("Error: Rating must be a number.")
                continue

            min_rating = int(min_rating_input)

            if min_rating < 1 or min_rating > 5:
                print_func("Error: Rating must be between 1 and 5.")
                continue

            averages = _calculate_average_ratings()

            filtered = [
                school for school in schools
                if averages.get(str(school.get("school_id")), 0.0) >= min_rating
            ]

            if not filtered:
                print_func(f"\nNo schools found with rating >= {min_rating}.")
                continue

            print_func(f"\n=== Schools with Rating >= {min_rating} ===")
            print_func(f"Found {len(filtered)} school(s):\n")

            for school in filtered:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                level = school.get("level", "?")
                location = school.get("location", "?")
                avg = averages.get(str(school_id), 0.0)

                print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location} | Avg Rating: {avg:.2f}")

            print_func("\nEnter any other key to return to Filter Menu")
            input_func("")
            continue

        else:
            print_func("Invalid option, please try again")
