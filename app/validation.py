"""
Global input validation helpers for the system

Implements US31 - Global Input Validation
- Username format validation
- Password format validation
- Menu option validation

These helpers are used by modules to ensure consistent validation
rules across the system
"""

from typing import Tuple, List

def validate_username_format(username: str) -> Tuple[bool, str]:
    """
    Validates the username format

    Inputs:
        username(str): Username to validate

    Returns:
        Tuple[bool, str]:
            - bool: True if the username is valid, False otherwise
            - str: "OK" or an error message with explanation
    """

    if not username or username.strip() == "":
        return False, "Username cannot be empty"

    cleaned = username.strip()

    if len(cleaned) < 3:
        return False, "Username must be at least 3 characters long"

    return True, "OK"


def validate_password_format(password: str) -> Tuple[bool, str]:
    """
    Validates the password format

    Inputs:
        password(str): Password to validate

    Returns:
        Tuple[bool, str]:
            - bool: True if the password is valid, False otherwise
            - str: "OK" or an error message with explanation
    """

    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    return True, "OK"

def validate_menu_option_format(choice: str, allowed_options: List[str]) -> Tuple[bool, str]:
    """
    Validates the menu option format

    Inputs:
        choice(str): Menu option to validate
        allowed_options(List[str]):

    Returns:
        Tuple[bool, str]:
            - bool: True if the menu option is valid, False otherwise
            - str: "OK" or an error message with explanation
    """

    if choice in allowed_options:
        return True, "OK"
    return False, "Invalid option, please try again"

def validate_rating_input(rating_value: str,
                          min_rating: int = 1,
                          max_rating: int = 5) -> Tuple[bool, str]:
    """
    Validates the rating input for US20 - Validate Rating Input.

    Inputs:
        rating_value (str): Raw user input for rating (e.g. from input()).
        min_rating (int): Minimum allowed rating value (inclusive).
        max_rating (int): Maximum allowed rating value (inclusive).

    Returns:
        Tuple[bool, str]:
            - bool: True if the rating value is valid, False otherwise.
            - str: "OK" or an error message with explanation.
    """

    if rating_value is None:
        return False, "Rating cannot be empty"

    stripped = rating_value.strip()

    if stripped == "":
        return False, "Rating cannot be empty"

    if not stripped.isdigit():
        if stripped.startswith("-") and stripped[1:].isdigit():
            return False, "Rating cannot be negative"
        return False, "Rating must be a whole number"

    value = int(stripped)
    if value < min_rating:
        return False, f"Rating must be at least {min_rating}"

    if value > max_rating:
        return False, f"Rating must be at most {max_rating}"

    return True, "OK"
