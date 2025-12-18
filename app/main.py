"""
Main menu for the text-based School Evaluation Platform

User Stories included so far:
 - US21 - User Registration
 - US22 - User Login
 - US23 - Session Handling
 - US31 - Global Session Handling
 - US25 - Role based access Control
 - US24 - Password Reset
 - US1 - Create the Schools
 - US6 - List All Schools
 - US4 - Delete School
 - US3 - Update School Details
 - US8 - Search Schools by Name

"""

from app.auth import register_user, login_user, reset_password
from app.data_store import get_users, example_users, get_current_user, clear_current_user
from app.validation import validate_menu_option_format
from app.access_control import user_has_role, check_access, ROLE_ADMIN
from app.admin_actions import list_all_users, delete_user_by_id, add_new_school, delete_comment_by_id, delete_school_by_id, update_school_by_id, view_system_statistics
from app.school_actions import list_all_schools, view_school_rankings, search_schools_by_name, view_top_schools


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

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("3. Add New School (Admin Only)")

    print("4. View Schools")

    print("8. View Top Schools by Category")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("5. Delete School (Admin Only)")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("6. Update School (Admin Only)")

    print("7. View School Rankings")
    print("8. Search for Schools")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("9. Display Registered Users (Admin Only)")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("10. Delete Selected User (Admin Only)")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("11. Delete a Comment (Admin Only)")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("12. View System Statistics (Admin Only)")

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

    example_users()

    while True:
        show_main_menu()
        current = get_current_user()

        allowed_options = ["1", "2", "4", "7", "8", "0"]


        if current is None:
            allowed_options.append("3")

        if current is not None and user_has_role(current, [ROLE_ADMIN]):
            allowed_options.append("3")
            allowed_options.append("5")
            allowed_options.append("6")
            allowed_options.append("9")
            allowed_options.append("10")
            allowed_options.append("11")
            allowed_options.append("12")

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
                # US23 - Log in Feature
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
            # US4 - Delete School
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue
            delete_school_by_id()

        elif choice == "6":
            # US3 - Update School Details
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue
            update_school_by_id()
        elif choice == "8":
            view_top_schools(print_func=print)

        elif choice == "7":
            view_school_rankings(print)

        elif choice == "8":
            # US8 - Search Schools by Name
            search_schools_by_name()

        elif choice == "9":
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue
            list_all_users(print)

        elif choice == "10":
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue

            try:
                uid = int(input("Enter user ID to delete: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            delete_user_by_id(uid, print)

        elif choice == "11":
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue

            try:
                cid = int(input("Enter comment ID to delete: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            delete_comment_by_id(cid, print)

        elif choice == "12":
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue
            view_system_statistics(print)

        elif choice == "0":
            print("\nThank you for using School Evaluation Platform")
            break


if __name__ == "__main__":
    main()
