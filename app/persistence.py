"""
Persistence utilities for US29 - Save System Data to File

Saves the in-memory state into a JSON file:
- USERS
- SCHOOLS
- RATINGS
- COMMENTS
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Callable

from app.data_store import get_users, get_schools
from app.reviews import RATINGS, COMMENTS

def serialize_comment(comment: Dict[str, Any]) -> Dict[str, Any]:
    """
    converts a comment dictionary into a JSON string

    Inputs:
        comment: comment dictionary

    Returns:
        Dict[str, Any]: JSON string
    """

    serialized = dict(comment)
    created_at = serialized.get('created_at')

    if isinstance(created_at, datetime):
        serialized['created_at'] = created_at.isoformat()

    elif created_at is None:
        serialized['created_at'] = None

    else:
        serialized['created_at'] = str(created_at)

    return serialized


def build_system_snapshot() -> Dict[str, Any]:
    """
    Builds a snapshot of the current system state

    Inputs:
        None

    Returns:
        Dict[str, Any]: JSON string
    """

    users = list(get_users())
    schools = list(get_schools())
    ratings = list(RATINGS)
    comments = [serialize_comment(c) for c in COMMENTS]

    return {
        'users': users,
        'schools': schools,
        'ratings': ratings,
        'comments': comments
    }


def save_system_data(
        file_path: str = "system_data.json",
        print_func: Callable[[str], None] = print,
) -> bool:
    """
    Saves the system state into a JSON file

    Inputs:
        file_path: path to save the system state to
        print_func: function that prints out the system state

    Returns:
        bool: True if successful, False otherwise
    """

    snapshot = build_system_snapshot()
    temp_path = f"{file_path}.tmp"

    try:
        parent_dir = os.path.dirname(file_path)

        if parent_dir:
            os.makedirs(parent_dir, exist_ok = True)

        with open(temp_path, 'w', encoding = "utf-8") as file:
            json.dump(snapshot, file, indent = 2, ensure_ascii = False)

        os.replace(temp_path, file_path)
        print_func(f"System data saved successfully to {file_path}.")
        return True
    except Exception as error:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

        print_func(
            f"Failed to save system state to {file_path}. Reason: {error}"
        )
        return False