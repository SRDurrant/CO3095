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
