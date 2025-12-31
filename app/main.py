"""
Main menu for the text-based School Evaluation Platform

Includes:

- US1  - Create the Schools (Admin)
- US3  - Update School Details (Admin)
- US4  - Delete School (Admin)
- US5  - View School Profile
- US6  - List All Schools
- US7  - Filter Schools by Attributes
- US8  - Search Schools by Name
- US9  - Sort Schools by Rating
- US10 - Compare Two Schools
- US11 - View School Rankings
- US12 - View Top Schools
- US13 - Export Top Schools Report (Admin)
- US21 - User Registration
- US22 - User Login
- US23 - Session Handling
- US24 - Password Reset
- US25 - Role-based Access Control
- US31 - Global Input Validation
- US32 - Display Registered Users (Admin)
- US33 - Delete Selected User (Admin)
- US34 - Delete a Comment (Admin)
- US35 - View System Statistics (Admin)
- US36 - View Trending Schools
- US37 - View Top Contributors (Admin)
- US39 - Help Menu
- US40 - Auto-load and Auto-save
"""

from app.auth import register_user, login_user, reset_password
from app.data_store import get_users, example_users, get_current_user, clear_current_user
from app.validation import validate_menu_option_format
from app.access_control import user_has_role, check_access, ROLE_ADMIN
from app.admin_actions import (
    list_all_users,
    delete_user_by_id,
    add_new_school,
    delete_comment_by_id,
    delete_school_by_id,
    update_school_by_id,
    view_system_statistics, 
    view_top_contributors,
    view_system_statistics,
    export_top_schools_report
)
from app.school_actions import (
    list_all_schools,
    view_school_rankings,
    search_schools_by_name,
    view_top_schools,
    view_trending_schools,
    compare_two_schools
)
from app.persistence import load_system_data, save_system_data
from app.help_menu import show_help_menu

DEFAULT_SYSTEM_DATA_PATH = "system_data.json"

def show_main_menu():
    """
    Displays the main menu options to the user
    """

    current = get_current_user()

    print("\nWelcome to the School Evaluation Platform App")

    if current:
        print(f"Logged in as {current.get('username')}")

    print("1. Register new User")

    if current is None:
        print("2. Login")
        print("3. Reset Password")
    else:
        print("2. Logout")

    print("4. Help Menu")
    print("5. View Schools")
    print("6. View School Rankings")
    print("7. View Top Schools by Category")
    print("8. Search for Schools")
    print("9. View Trending Schools")
    print("10. Compare Two Schools")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("11. Add New School (Admin Only)")
        print("12. Delete School (Admin Only)")
        print("13. Update School (Admin Only)")
        print("14. Display Registered Users (Admin Only)")
        print("15. Delete Selected User (Admin Only)")
        print("16. Delete a Comment (Admin Only)")
        print("17. View System Statistics (Admin Only)")
        print("18. Export Top Schools Report (Admin Only)")
        print("19. View Top Contributors (Admin Only)")

    print("0. Exit")


def main() -> None:
    """
    Main Application Loop
    """

    load_system_data(file_path = DEFAULT_SYSTEM_DATA_PATH, print_func = print)

    if not get_users():
        example_users()

    did_explicit_exit_save = False

    try:
        while True:
            show_main_menu()
            current = get_current_user()

            # Allowed options mirror the menu displayed
            allowed_options = ["0", "2", "1", "4", "5", "6", "7", "8", "9", "10"]

            # Reset password only when logged out
            if current is None:
                allowed_options.append("3")

            # Admin only block 11-19
            if current is not None and user_has_role(current, [ROLE_ADMIN]):
                allowed_options.extend(["11", "12", "13", "14", "15", "16", "17", "18", "19"])

            choice = input("Select an option: ").strip()

            valid, msg = validate_menu_option_format(choice, allowed_options)
            if not valid:
                print(msg)
                continue

            if choice == "1":
                #US21 - User Registration
                register_user()

            elif choice == "2":
                if current is None:
                    # US22 - Log in Feature
                    login_user()
                else:
                    # US23 - Log out feature
                    clear_current_user()
                    print("\nYou have been logged out")

            elif choice == "3":
                # US24 - Password Reset
                if current is None:
                    reset_password()
                    continue

            elif choice == "4":
                # US39 - Help Menu
                show_help_menu(current_user = current, input_func = input, print_func = print)

            elif choice == "5":
                # US6 - List Schools (includes US5/US7/US9 in its internal menu)
                list_all_schools()

            elif choice == "6":
                # US11 - Rankings
                view_school_rankings(print_func = print)

            elif choice == "7":
                # US12 - Top Schools
                view_top_schools(print_func = print)

            elif choice == "8":
                # US8 - Search
                search_schools_by_name()

            elif choice == "9":
                # US36 - Trending
                view_trending_schools(print_func = print)

            elif choice == "10":
                # US10 - Compare two Schools
                compare_two_schools()

            elif choice == "11":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                add_new_school()

            elif choice == "12":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                delete_school_by_id()

            elif choice == "13":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                update_school_by_id()

            elif choice == "14":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                list_all_users(print_func = print)

            elif choice == "15":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue

                try:
                    uid = int(input("Enter User ID to delete: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                delete_user_by_id(uid, print_func = print)

            elif choice == "16":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue

                try:
                    cid = int(input("Enter User ID to delete: ").strip())
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                delete_comment_by_id(cid, print_func = print)

            elif choice == "17":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                view_system_statistics(print_func = print)

            elif choice == "18":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                export_top_schools_report(print_func = print)

            elif choice == "19":
                if not check_access(current, [ROLE_ADMIN], print_func = print):
                    continue
                view_top_contributors(print_func = print)

            elif choice == "0":

                save_system_data(file_path = DEFAULT_SYSTEM_DATA_PATH, print_func = print)
                did_explicit_exit_save = True

                print("\nThank you for using School Evaluation Platform")
                break
    finally:
        if not did_explicit_exit_save:
            save_system_data(file_path = DEFAULT_SYSTEM_DATA_PATH, print_func = print)


if __name__ == "__main__":
    main()
