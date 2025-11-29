"""
Main menu for the text-based School Evaluation Platform

User Stories included so far:
 - US21 - User Registration
"""

from app.auth import register_user, login_user
from app.data_store import get_users, example_users, get_current_user, clear_current_user
from app.validation import validate_menu_option_format

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
    print("2. Display Registered Users (debug)")

    if current is None:
        print("3. Login")
    else:
        print("3. Logout")

    print("0. Exit")


def list_users_debug() -> None:
    """
    Displays the list of registered users

    Inputs:
        None

    Returns:
        None
            Prints a list of the users registered (Temporary users)
    """

    users = get_users()
    if not users:
        print("No users registered")
        return

    print("\nRegistered Users:")
    for user in users:
        user_id = user.get("user_id", "?")
        username = user.get("username", "?")
        role = user.get("role", "?")
        print(f" - ID: {user_id}, Username: {username}, Role: {role}")


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
        choice = input("Select an option: ").strip()

        allowed_options = ["1", "2", "3", "0"]

        valid, msg = validate_menu_option_format(choice, allowed_options)
        if not valid:
            print(msg)
            continue

        current = get_current_user()

        if choice == "1":
            #US21 - User Registration
            register_user()

        elif choice == "2":
            # Shows all users currently stored in the system
            list_users_debug()

        elif choice == "3":
            if current is None:
                # US23 - Log in Feature
                login_user()
            else:
                # US23 - Log out feature
                clear_current_user()
                print("\nYou have been logged out")

        elif choice == "0":
            print("\nThank you for using School Evaluation Platform")
            break


if __name__ == "__main__":
    main()