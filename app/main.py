"""
Main menu for the text-based School Evaluation Platform

User Stories included so far:
 - US21 - User Registration
"""

from app.auth import register_user
from app.data_store import get_users, example_users


def show_main_menu():
    """
    Displays the main menu options to the user

    Inputs:
        None

    Returns:
        None
    """

    print("\nWelcome to the School Evaluation Platform App")
    print("1. Register new User")
    print("2. Display Registered Users (debug)")
    print("3. Login (Not yet available)") # Will be implemented in US22
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

        if choice == "1":
            register_user()

        elif choice == "2":
            # Shows all users currently stored in the system
            list_users_debug()

        elif choice == "0":
            print("Thank you for using School Evaluation Platform")
            break

        else:
            print("Invalid option, please select an option shown")


if __name__ == "__main__":
    main()