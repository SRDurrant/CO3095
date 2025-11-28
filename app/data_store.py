"""
Simple in-memory data store for US21
"""

from typing import List, Dict

USERS: List[Dict] = []

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