"""
For school-related actions for the system

Implements:
- US6 - List All Schools
"""

from typing import Callable
from app.data_store import get_schools


def list_all_schools(
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    US6 - List All Schools
    Allows any user to see all schools in the system

    Inputs:
        input_func (Callable[[str], str]): Function used to get user input
        print_func (Callable): Function used to print output (for testing)

    Returns:
        None
    """

    schools = get_schools()

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

    print_func("\nPress '0' to return to the main menu")
    input_func("")

def view_school_rankings(print_func=print) -> None:
    """
    US11 – View school rankings for each category (level)
    Shows all schools sorted by average rating
    """

    schools = get_schools()
    if not schools:
        print_func("No schools available.")
        return

    averages = _calculate_average_ratings()
    grouped = defaultdict(list)

    for s in schools:
        avg = averages.get(str(s["school_id"]), 0)
        grouped[s["level"]].append((s, avg))

    for level, items in grouped.items():
        print_func(f"\n=== {level.capitalize()} Schools Ranking ===")
        items.sort(key=lambda x: x[1], reverse=True)

        for s, avg in items:
            print_func(
                f"ID {s['school_id']} | {s['name']} | Avg Rating: {avg:.2f}"
            )