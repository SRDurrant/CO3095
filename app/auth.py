"""
Authentication and registration logic for US21
"""

from typing import Callable, Tuple, Optional, List, Dict
from .data_store import get_users, add_user

def find_user_by_username(users: List[Dict], username: str):
    """returns the user dict if the username exists already, if it doesn't None"""
    for user in users:
        if user['username'] == username:
            return user
    return None

def get_next_user_id(users: List[Dict]) -> int:
    """returns the next user id if it exists, else return None"""
    if not users:
        return 1
    exisiting_ids = [u.get("user_id", 0) for u in users]
    return max(exisiting_ids) + 1
