"""
Main menu for the text-based School Evaluation Platform

User Stories included so far:
 - US21 - User Registration
 - US22 - User Login
 - US23 - Session Handling
 - US31 - Global Session Handling
 - US25 - Role based access Control
"""

from app.auth import register_user, login_user
from app.data_store import get_users, example_users, get_current_user, clear_current_user
from app.validation import validate_menu_option_format
from app.access_control import user_has_role, check_access, ROLE_ADMIN
from app.admin_actions import list_all_users

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
    else:
        print("2. Logout")

    if current is not None and user_has_role(current, [ROLE_ADMIN]):
        print("9. Display Registered Users (Admin Only)")

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

        allowed_options = ["1", "2", "0"]

        if current is not None and user_has_role(current, [ROLE_ADMIN]):
            allowed_options.append("9")

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


        elif choice == "9":
            if not check_access(current, [ROLE_ADMIN], print_func=print):
                continue
            list_all_users(print)

        elif choice == "0":
            print("\nThank you for using School Evaluation Platform")
            break


if __name__ == "__main__":
    main()