"""
Global input validation helpers for the system

Implements US31 - Global Input Validation
Username format validation
Password format validation
Menu option validation

Implements US2 - Validate School Creation Input
- School name format validation
- School level format validation
- School location format validation

These helpers are used by modules to ensure consistent validation
rules across the system
"""

from typing import Tuple, List

def validate_username_format(username: str) -> Tuple[bool, str]:
     """
    Validates the format of the username.
    Inputs:
        username(str): Username to validate
    Returns:
        Tuple[bool, str]:
            - bool: True, only if the username is valid and is false otherwise
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
            - bool: True only when and if the password is valid and is false otherwise
            - str: "OK" or an error message with explanation
    """
    if not password:
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    return True, "OK"

def validate_menu_option_format(choice: str, allowed_options: List[str]) -> Tuple[bool, str]:
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
            - bool: True only if the rating value is valid and is false otherwise.
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


def validate_school_name(name: str) -> Tuple[bool, str]:
    """
    Validates the school's name

    Inputs:
        name (str): School name to validate

    Returns:
        Tuple[bool, str]:
            - bool: True if the name is valid, False otherwise
            - str: "Accepted" or an error message with explanation
    """

    if not name or name.strip() == "":
        return False, "School name cannot be empty"

    cleaned = name.strip()

    if len(cleaned) < 5:
        return False, "School name must be at least 5 characters long"

    return True, "Accepted"


def validate_school_level(level_input: str) -> Tuple[bool, str]:
    """
    Validates the school's level

    Inputs:
        level_choice (str): Level choice to validate (should be "1", "2", or "3")

    Returns:
        Tuple[bool, str]:
            - bool: True if the level choice is valid, False otherwise
            - str: "Accepted" or an error message with explanation
    """

    valid_levels = ["1", "2", "3"]

    if level_input not in valid_levels:
        return False, "Invalid input. Please select 1, 2, or 3"

    return True, "Accepted"


def validate_school_location(location: str) -> Tuple[bool, str]:
    """
    Validates the school's location

    Inputs:
        location (str): School location to validate

    Returns:
        Tuple[bool, str]:
            - bool: True if the location is valid, False otherwise
            - str: "Accepted" or an error message with explanation
    """

    if not location or location.strip() == "":
        return False, "School location cannot be empty"

    cleaned = location.strip()

    if len(cleaned) < 3:
        return False, "School location must be at least 3 characters long"

    return True, "Accepted"


def check_duplicate_school(schools: List[dict], name: str, location: str) -> Tuple[bool, str]:
    """
    Checks if a school with the same name and location already exists

    Inputs:
        schools (List[dict]): List of existing schools
        name (str): School name to check
        location (str): School location to check

    Returns:
        Tuple[bool, str]:
            - bool: True if no duplicate exists, False if duplicate found
            - str: "Accepted" or an error message with explanation
    """

    cleaned_name = name.strip().lower()
    cleaned_location = location.strip().lower()

    for school in schools:
        existing_name = school.get("name", "").strip().lower()
        existing_location = school.get("location", "").strip().lower()
        if existing_name == cleaned_name and existing_location == cleaned_location:
            return False, "A school with this name and location already exists"

    return True, "Accepted"
