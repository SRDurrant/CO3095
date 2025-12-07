from typing import Callable
from app.data_store import get_users

def list_all_users(print_func=print) -> None:
    """
    US - Admin View All Registered Users
    Allows an administrator to see all registered users.

    Inputs:
        print_func (Callable): Function used to print output (for testing)

    Returns:
        None
    """

    users = get_users()

    if not users:
        print_func("\nNo users found in the system.")
        return

    print_func("\n=== Registered Users ===")
    for user in users:
        uid = user.get("user_id", "?")
        username = user.get("username", "?")
        role = user.get("role", "?")

        print_func(f"ID: {uid} | Username: {username} | Role: {role}")

def delete_user_by_id(user_id: int, print_func: Callable = print) -> bool:
    """
    US33 – Admin deletes abusive/fake user accounts.

    Admin accounts cannot be deleted.

    Inputs:
        user_id (int): ID of the user to delete
        print_func (Callable): Injected print function for testing

    Returns:
        bool: True if deletion successful, False otherwise
    """

    users = get_users()

    for i, user in enumerate(users):
        if user.get("user_id") == user_id:
            if user.get("role") == "admin":
                print_func("Error: Admin accounts cannot be deleted.")
                return False

            deleted_user = users.pop(i)
            print_func(f"User '{deleted_user['username']}' (ID {user_id}) has been deleted.")
            return True

    print_func("Error: User does not exist.")
    return False