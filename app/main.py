"""
Main menu for the text-based School Evaluation Platform

User Stories included so far:
 - US21 - User Registration
 - US22 - User Login
 - US23 - Session Handling
 - US31 - Global Session Handling
 - US40 - Auto-load and Auto-save
 - US25 - Role based access Control
 - US24 - Password Reset
 - US1 - Create the Schools
 - US6 - List All Schools
 - US4 - Delete School
 - US3 - Update School Details
 - US8 - Search Schools by Name
 - US10 - Compare Two Schools


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
from app.school_actions import list_all_schools, view_school_rankings, search_schools_by_name, view_top_schools, \
    view_trending_schools, compare_two_schools
from app.persistence import load_system_data, save_system_data

DEFAULT_SYSTEM_DATA_PATH = "system_data.json"

def show_main_menu():
    """
    Displays the main menu options to the user

    Inputs:
        None

    Returns:
        None
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
        if user_has_role(current, [ROLE_ADMIN]):
            print("3. Add New School (Admin Only)")

    print("4. View Schools")
    print("5. View School Rankings")
    print("6. View Top Schools by Category")
    print("7. Search for Schools")
    print("15. View Trending Schools")
    print("17. Compare Two Schools")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("8. Delete School (Admin Only)")
        print("9. Update School (Admin Only)")
        print("10. Display Registered Users (Admin Only)")
        print("11. Delete Selected User (Admin Only)")
        print("12. Delete a Comment (Admin Only)")
        print("13. View System Statistics (Admin Only)")
        print("14. Export Top Schools Report (Admin Only)")
        print("16. View Top Contributors (Admin Only)")

    print("0. Exit")


def main() -> None:
    """
    Main Application

    Inputs:
        None

    Returns:
        None
            Runs the interactive menu loop until the user has exited
    """
    load_system_data(file_path = DEFAULT_SYSTEM_DATA_PATH, print_func = print)

    if not get_users():
        example_users()

    did_explicit_exit_save = False

    try:
        while True:
            show_main_menu()
            current = get_current_user()

            allowed_options = ["1", "2", "4", "5", "6", "7", "15", "17", "0"]


            if current is None:
                allowed_options.append("3")

            if current is not None and user_has_role(current, [ROLE_ADMIN]):
                allowed_options.extend(["3", "8", "9", "10", "11", "12", "13", "14", "16"])



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

                # US1 - Create the Schools
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                add_new_school()

            elif choice == "4":
                # US6 - List all Schools
                list_all_schools()

            elif choice == "5":
                # US11 - View School Rankings
                view_school_rankings(print)

            elif choice == "6":
                # US12 - View Top Schools by Category
                view_top_schools(print_func=print)

            elif choice == "7":
                # US8 - Search Schools by Name
                search_schools_by_name()

            elif choice == "8":
                # US4 - Delete School (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                delete_school_by_id()

            elif choice == "9":
                # US3 - Update School Details (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                update_school_by_id()

            elif choice == "10":
                # US32 - Display Registered User (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                list_all_users(print)

            elif choice == "11":
                # US33 - Delete Selected User (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue

                try:
                    uid = int(input("Enter user ID to delete: "))

                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                delete_user_by_id(uid, print)

            elif choice == "12":
                # US34 - Delete a Comment (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue

                try:
                    cid = int(input("Enter comment ID to delete: "))

                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                delete_comment_by_id(cid, print)

            elif choice == "13":
                # US35 - View System Statistics (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                view_system_statistics(print)

            elif choice == "14":
                # US13 – Export Top Schools Report (Admin Only)
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                export_top_schools_report(print_func=print)
                
            elif choice == "15":
                # US36 - View Trending Schools
                view_trending_schools(print_func=print)

            elif choice == "16":
                if not check_access(current, [ROLE_ADMIN], print_func=print):
                    continue
                view_top_contributors(print_func=print)

            elif choice == "17":
                # US10 - Compare Two Schools
                compare_two_schools()
                
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
