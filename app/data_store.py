"""
Simple in-memory data store for US21
"""

from typing import List, Dict

USERS: List[Dict] = []

def get_users() -> List[Dict]:
    """Will return the global list of users"""
    return USERS

def add_user(user: Dict) -> None:
    """Adds a user to the global list of users"""
    USERS.append(user)