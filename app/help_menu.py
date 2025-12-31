"""
US39 - Help Menu

As a user, I want a help menu, so I can understand all the available commands
"""

from typing import Callable, Optional, Dict
from app.access_control import ROLE_ADMIN, ROLE_STUDENT

def show_help_menu(
        current_user: Optional[Dict],
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print
) -> None:
    """
    Displays a help menu describing available commands and how to navigate the system.

    Inputs:
        current_user: dict or None
        input_func: injected input function (for testing)
        print_func: injected print function (for testing)

    Returns:
        None
    """

    role = None
    if current_user:
        role = current_user.get("role")

    print_func("\n=== Help Menu ===")
    print_func("This system is a text-based School Evaluation Platform.")
    print_func("")
    print_func("General navigation:")
    print_func("- Enter the number of a menu option to run it.")
    print_func("- Enter '0' in most sub-menus to cancel/return.")
    print_func("- Some features may ask you to press Enter to continue.")
    print_func("")

    print_func("Main menu options (standard):")
    print_func("1. Register new user - Create a new student account.")
    print_func("2. Login/Logout - Log in if logged out, or log out if logged in.")
    print_func("3. Reset Password - Only visible when logged out.")
    print_func("4. Help Menu - Shows this help information.")
    print_func("5. View Schools - Browse schools, view profiles, filter, sort.")
    print_func("6. View School Rankings - Rankings per category (level).")
    print_func("7. View Top Schools by Category - Top schools per level.")
    print_func("8. Search for Schools - Search by school name keyword.")
    print_func("9. View Trending Schools - Based on rating/comment activity.")
    print_func("10. Compare Two Schools - Compare two schools side-by-side.")
    print_func("0. Exit - Saves system data and exits safely.")
    print_func("")

    print_func("User actions inside school menus:")
    print_func("- View School Profile: shows level, location, and average rating.")
    print_func("- Filter Schools: by location/level/minimum rating.")
    print_func("- Sort Schools: highest-to-lowest or lowest-to-highest average rating.")
    print_func("")

    if role == ROLE_ADMIN:
        print_func("Admin-only options:")
        print_func("11. Add New School (Admin Only)")
        print_func("12. Delete School (Admin Only)")
        print_func("13. Update School (Admin Only)")
        print_func("14. Display Registered Users (Admin Only)")
        print_func("15. Delete Selected User (Admin Only)")
        print_func("16. Delete a Comment (Admin Only)")
        print_func("17. View System Statistics (Admin Only)")
        print_func("18. Export Top Schools Report (Admin Only)")
        print_func("19. View Top Contributors (Admin Only)")
        print_func("")
        print_func("Note: Admin-only actions require you to be logged in as an admin account.")

    elif role == ROLE_STUDENT:
        print_func("You are logged in as a student.")
        print_func("Admin-only options will not be available.")

    else:
        print_func("You are currently logged out.")
        print_func("Login to access student/admin features where applicable.")

    print_func("")
    input_func("Press Enter to return to the main menu...")