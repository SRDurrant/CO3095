"""
US39 - White-Box Tests (Concolic Testing Style)

Technique: Concolic testing (concrete + symbolic reasoning)
Approach:
- Start with a concrete input (U, R) and observe which branch executes.
- Then "mutate" the concrete input to satisfy alternative path constraints,
  thereby exploring additional branches.

This is a lightweight, manual concolic approach suitable for this project.
"""

from app.help_menu import show_help_menu
from app.access_control import ROLE_ADMIN, ROLE_STUDENT


def _exec_and_capture(user):
    out = []

    def p(msg=""):
        out.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user=user, input_func=i, print_func=p)
    return "\n".join(out)


def test_concolic_start_logged_out_then_mutate_to_admin_then_student_then_unknown():
    # Concrete run 1: U=None => logged out branch
    text1 = _exec_and_capture(None)
    assert "You are currently logged out." in text1
    assert "Admin-only options:" not in text1

    # Mutate to satisfy admin path constraint: U truthy AND role == 'admin'
    text2 = _exec_and_capture({"role": ROLE_ADMIN})
    assert "Admin-only options:" in text2
    assert "You are currently logged out." not in text2

    # Mutate to satisfy student path constraint: U truthy AND role == 'student'
    text3 = _exec_and_capture({"role": ROLE_STUDENT})
    assert "You are logged in as a student." in text3
    assert "Admin-only options:" not in text3

    # Mutate to satisfy "other role" constraint: U truthy AND role not in valid set
    text4 = _exec_and_capture({"role": "moderator"})
    assert "You are currently logged out." in text4
    assert "Admin-only options:" not in text4
    assert "You are logged in as a student." not in text4


def test_concolic_mutation_on_same_user_object():
    # Begin with a concrete user object and mutate role field between executions.
    user = {"user_id": 7, "username": "u", "role": "student"}
    t_student = _exec_and_capture(user)
    assert "You are logged in as a student." in t_student

    user["role"] = "admin"
    t_admin = _exec_and_capture(user)
    assert "Admin-only options:" in t_admin

    user["role"] = ""
    t_other = _exec_and_capture(user)
    assert "You are currently logged out." in t_other
    assert "Admin-only options:" not in t_other
