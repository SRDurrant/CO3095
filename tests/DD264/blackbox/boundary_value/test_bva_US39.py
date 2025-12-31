"""
US39 - Black-Box Tests (Boundary-Value)

Technique: Boundary-value testing
- For role handling and user object variations:
  * None vs dict
  * missing key vs empty string role vs unknown role
  * exact valid role strings vs case variations
"""

from app.help_menu import show_help_menu
from app.access_control import ROLE_ADMIN, ROLE_STUDENT


def _capture(current_user):
    out = []

    def p(msg=""):
        out.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user=current_user, input_func=i, print_func=p)
    return "\n".join(out)


def test_boundary_current_user_none():
    text = _capture(None)
    assert "You are currently logged out." in text


def test_boundary_current_user_empty_dict():
    text = _capture({})
    assert "You are currently logged out." in text


def test_boundary_role_missing_key():
    text = _capture({"user_id": 3, "username": "x"})
    assert "You are currently logged out." in text


def test_boundary_role_none_value():
    text = _capture({"user_id": 3, "username": "x", "role": None})
    assert "You are currently logged out." in text


def test_boundary_role_empty_string():
    text = _capture({"user_id": 3, "username": "x", "role": ""})
    assert "You are currently logged out." in text


def test_boundary_role_unknown_string():
    text = _capture({"user_id": 3, "username": "x", "role": "moderator"})
    assert "You are currently logged out." in text


def test_boundary_role_admin_exact_match():
    text = _capture({"user_id": 1, "username": "admin", "role": ROLE_ADMIN})
    assert "Admin-only options:" in text


def test_boundary_role_student_exact_match():
    text = _capture({"user_id": 2, "username": "student", "role": ROLE_STUDENT})
    assert "You are logged in as a student." in text
    assert "Admin-only options:" not in text


def test_boundary_role_admin_wrong_case():
    text = _capture({"user_id": 1, "username": "admin", "role": "Admin"})
    assert "Admin-only options:" not in text
    assert "You are currently logged out." in text


def test_boundary_role_student_wrong_case():
    text = _capture({"user_id": 2, "username": "student", "role": "Student"})
    assert "You are logged in as a student." not in text
    assert "You are currently logged out." in text


def test_boundary_role_with_surrounding_spaces():
    text = _capture({"user_id": 1, "username": "admin", "role": " admin "})
    assert "Admin-only options:" not in text
    assert "You are currently logged out." in text
