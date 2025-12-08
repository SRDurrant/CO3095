"""
Simple in-memory data store for US21,US1
"""

from typing import List, Dict

USERS: List[Dict] = []
SCHOOLS: List[Dict] = []

def get_users() -> List[Dict]:
    """
    Returns a list of all users in the global list of users

    Returns:
         List[Dict]: A list of all users in the global list of users
    """

    return USERS


def add_user(user: Dict) -> None:
    """
    Adds a user to the global list of users

    Inputs:
        user (Dict): A dictionary containing user data
            {
            "user_id": int,
            "username": str,
            "password": str,
            "role": str
            }
    """

    USERS.append(user)


def example_users() -> None:
    """
    TEMPORARY FUNCTION: This functions adds examples users into memory for development/testing purposes

    This is not persistence: the data will reset every time the program restarts.
    Will be removed or changed when US29/US30 are implemented.
    """

    if USERS:
        return


    add_user(
        {
            "user_id": 1,
            "username": "admin-user",
            "password": "admin123",
            "role": "admin"
        }
    )

    add_user(
        {
            "user_id": 2,
            "username": "student-user",
            "password": "student456",
            "role": "student"
        }
    )


CURRENT_USER = None

def set_current_user(user: Dict) -> None:
    """
    Sets the current user

    Inputs:
        user (Dict): A dictionary containing user data

    Returns:
        None
    """

    global CURRENT_USER
    CURRENT_USER = user


def get_current_user() -> Dict:
    """
    Gets the current user logged in

    Inputs:
        None

    Returns:
        dict | None: A dictionary containing user data, or None if no one is logged in
    """

    return CURRENT_USER


def clear_current_user() -> None:
    """
    Log out the current user and clear the session

    Inputs:
        None

    Returns:
        dict | None: THe current user dictionary, or None if no one is logged in
    """

    global CURRENT_USER
    CURRENT_USER = None


def get_schools() -> List[Dict]:
    """
    Returns a list of all schools in the global list of schools

    Returns:
         List[Dict]: A list of all schools in the global list of schools
    """

    return SCHOOLS


def add_school(school: Dict) -> None:
    """
    Adds a school to the global list of schools

    Inputs:
        school (Dict): A dictionary containing school data
            {
            "school_id": int,
            "name": str,
            "level": str,
            "location": str
            }
    """

    SCHOOLS.append(school)


def get_next_school_id(schools: List[Dict]) -> int:
    """
    Gets the next available school ID based on the existing schools

    Inputs:
        schools (List[Dict]): list of school dictionaries

    Returns:
        int: next available school ID, 1 if the list is empty
    """

    if not schools:
        return 1
    active_ids = [s.get("school_id", 0) for s in schools]
    return max(active_ids) + 1
