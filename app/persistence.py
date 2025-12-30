"""
Persistence utilities for US29 - Save System Data to File

Saves the in-memory state into a JSON file:
- USERS
- SCHOOLS
- RATINGS
- COMMENTS
- FAVOURITES
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Callable

from app.data_store import get_users, get_schools, USERS, SCHOOLS
from app.reviews import RATINGS, COMMENTS, FAVOURITES
from app.system_log import log_event, log_error


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
    favourites = list(FAVOURITES)

    return {
        'users': users,
        'schools': schools,
        'ratings': ratings,
        'comments': comments,
        'favourites': favourites,
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


def deserialize_comment(comment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a serialized comment dictionary back into in-memory format by restoring created_at

    Inputs:
        comment: serialized comment dictionary

    Returns:
        Dict[str, Any]: JSON string
    """

    restored = dict(comment)
    created_at = restored.get("created_at")

    if isinstance(created_at, str):
        try:
            restored["created_at"] = datetime.fromisoformat(created_at)

        except ValueError:
            restored["created_at"] = None

    else:
        restored["created_at"] = None

    return restored


def load_system_data(
        file_path: str = "system_data.json",
        print_func: Callable[[str], None] = print
) -> bool:
    """
    Loads the system state from a JSON file

    Inputs:
        file_path: path to load the system state from
        print_func: function that prints out the system state

    Returns:
        bool: True if successful, False otherwise
    """

    if not os.path.exists(file_path):
        print_func(f"No saved system data found at {file_path}.")
        return False

    try:
        with open(file_path, 'r', encoding = "utf-8") as file:
            snapshot = json.load(file)

        required_keys = {"users", "schools", "ratings", "comments"}
        if not required_keys.issubset(snapshot.keys()):
            raise ValueError("Invalid system snapshot format")

        USERS.clear()
        USERS.extend(snapshot['users'])

        SCHOOLS.clear()
        SCHOOLS.extend(snapshot['schools'])

        RATINGS.clear()
        RATINGS.extend(snapshot['ratings'])

        COMMENTS.clear()
        for comment in snapshot['comments']:
            COMMENTS.append(deserialize_comment(comment))

        # favourites are optional to preserve backward compatibility
        FAVOURITES.clear()
        if 'favourites' in snapshot and isinstance(snapshot['favourites'], list):
            FAVOURITES.extend(snapshot['favourites'])

        print_func(f"System data loaded successfully from {file_path}.")
        log_event(f"System data saved to {file_path}")
        return True

    except Exception as error:
        print_func(
            f"Failed to load system data from {file_path}. Reason: {error}"
        )
        log_error(f"Failed to load system data: {error}")
        return False
