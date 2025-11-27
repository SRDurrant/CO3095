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