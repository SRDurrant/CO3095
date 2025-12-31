"""
For school-related actions for the system

Implements:
- US5 - View School Profile
- US6 - List All Schools

- US8 - Search Schools by Name
- US9 - Sort Schools by Rating
- US11 - View School Rankings for Each Category (Level)
- US12 - Shows top-performing schools per category
"""

from typing import Callable, Dict
from collections import defaultdict

from app.data_store import get_schools
from app.validation import validate_school_id_exists
from app.reviews import RATINGS, COMMENTS
from app.data_store import SCHOOLS


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

        print_func("3. Sort Schools by Rating")
        print_func("0. Return to Main Menu")

        choice = input_func("Select an option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            view_school_profile(input_func, print_func)




        elif choice == "3":
            sort_schools_by_rating(input_func, print_func)

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

def view_trending_schools(
    limit: int = 5,
    print_func: Callable[[str], None] = print,
):
    """
    US36 – View Trending Schools based on review activity.

    Trending score = number of ratings + number of comments.
    """

    if not SCHOOLS:
        print_func("No schools available.")
        return

    activity_count = defaultdict(int)

    # Count ratings
    for rating in RATINGS:
        sid = str(rating.get("school_id"))
        activity_count[sid] += 1

    # Count comments
    for comment in COMMENTS:
        sid = str(comment.get("school_id"))
        activity_count[sid] += 1

    # Build sortable list
    trending = []
    for school in SCHOOLS:
        sid = str(school.get("school_id"))
        score = activity_count.get(sid, 0)
        trending.append((school, score))

    # Sort by activity score (descending)
    trending.sort(key=lambda x: x[1], reverse=True)
    trending = trending[:limit]

    print_func("\n=== Trending Schools ===")

    if all(score == 0 for _, score in trending):
        print_func("No recent activity for any school.")
        return

    for idx, (school, score) in enumerate(trending, start=1):
        print_func(
            f"{idx}. {school.get('name')} "
            f"(ID {school.get('school_id')}) - "
            f"Activity Score: {score}"
        )





















































































































































































def sort_schools_by_rating(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    US9 - Sort Schools by Rating
    As a user, I want to sort schools by highest or lowest rating for easy comparison.

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable[[str], None]): Function used to print output (for testing)

    Returns:
        None
    """

    schools = get_schools()
    averages = _calculate_average_ratings()

    while True:
        print_func("\n=== Sort Schools by Rating ===")
        print_func("1. Highest to Lowest")
        print_func("2. Lowest to Highest")
        print_func("0. Return to Schools List")

        choice = input_func("Select sort order: ").strip()

        if choice == "0":
            print_func("\nExiting Sort Schools.")
            return

        elif choice == "1":
            # Sort highest to lowest
            sorted_schools = sorted(
                schools,
                key=lambda s: averages.get(str(s.get("school_id")), 0.0),
                reverse=True
            )

            print_func("\n=== Schools Sorted by Rating (Highest to Lowest) ===")
            print_func(f"Found {len(sorted_schools)} school(s):\n")

            for school in sorted_schools:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                level = school.get("level", "?")
                location = school.get("location", "?")
                avg = averages.get(str(school_id), 0.0)

                if avg > 0:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location} | Avg Rating: {avg:.2f}")
                else:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location} | Avg Rating: No ratings yet")

            print_func("\nEnter any other key to return to Sort Menu")
            input_func("")
            continue

        elif choice == "2":
            # Sort lowest to highest
            sorted_schools = sorted(
                schools,
                key=lambda s: averages.get(str(s.get("school_id")), 0.0),
                reverse=False
            )

            print_func("\n=== Schools Sorted by Rating (Lowest to Highest) ===")
            print_func(f"Found {len(sorted_schools)} school(s):\n")

            for school in sorted_schools:
                school_id = school.get("school_id", "?")
                name = school.get("name", "?")
                level = school.get("level", "?")
                location = school.get("location", "?")
                avg = averages.get(str(school_id), 0.0)

                if avg > 0:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location} | Avg Rating: {avg:.2f}")
                else:
                    print_func(f"ID: {school_id} | Name: {name} | Level: {level.capitalize()} | Location: {location} | Avg Rating: No ratings yet")

            print_func("\nEnter any other key to return to Sort Menu")
            input_func("")
            continue

        else:
            print_func("Invalid option, please try again")
