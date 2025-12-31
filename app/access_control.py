"""
Role-Based Access Control (RBAC) helpers

Implements the US25 - Role-based Users:
    As an administrator, I would like a role-based system so that no every
    user can edit or delete everything
"""

from typing import List, Optional, Dict, Callable

ROLE_ADMIN = "admin"
ROLE_STUDENT = "student"

def user_has_role(user: Optional[Dict], required_roles: List[str]) -> bool:
    """
    This function checks whether a user has at least one the required roles

    Inputs:
        user (Optional[Dict]): Checks the current user dictionary, or None if not
        logged in
        required_roles (List[str]): List of required roles that are
        allowed to perform actions

    Returns:
        bool: True if user is not None and user["role"] is in
        required_roles, False otherwise
    """

    if user is None:
        return False

    user_role = user.get("role")
    if user_role is None:
        return False

    return user_role in required_roles

def check_access(
        current_user: Optional[Dict],
        required_roles: List[str],
        print_func: Callable[[str], None] = print,
) -> bool:
    """
    Checks whether the current user is allowed to perform an action

    This helper provides consistent messaging for:
        - Not logged-in users
        - Logged-in users without sufficient role

    Inputs:
        current_user (Optional[Dict]): Current user
        required_roles (List[str]): Roles that are permitted for action
        print_func (Callable[[str], None]): Function used to print message

    Returns:
        bool: True if user is allowed to perform action, False otherwise
    """

    if current_user is None:
        print_func("You must be logged in to perform an action")
        return False

    if not user_has_role(current_user, required_roles):
        print_func("You do not have permission to perform this action")
        return False

    return True