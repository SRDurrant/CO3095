"""
US39 - White-Box Tests (Branch-Based)

Technique: Branch-based testing
Goal: execute every branch in show_help_menu():

Branches:
1) current_user is truthy -> role = current_user.get("role")
2) current_user falsy -> role stays None
3) role == ROLE_ADMIN -> admin block
4) elif role == ROLE_STUDENT -> student message
5) else -> logged-out message
6) final input_func call executed
"""

from app.help_menu import show_help_menu
from app.access_control import ROLE_ADMIN, ROLE_STUDENT


def test_branch_current_user_none_goes_to_logged_out_branch_and_calls_input():
    printed = []
    input_called = {"count": 0}

    def p(msg=""):
        printed.append(str(msg))

    def i(_prompt=""):
        input_called["count"] += 1
        return ""

    show_help_menu(current_user=None, input_func=i, print_func=p)

    text = "\n".join(printed)
    assert "You are currently logged out." in text
    assert input_called["count"] == 1


def test_branch_current_user_present_role_admin_hits_admin_branch_and_calls_input():
    printed = []
    input_called = {"count": 0}

    def p(msg=""):
        printed.append(str(msg))

    def i(_prompt=""):
        input_called["count"] += 1
        return ""

    show_help_menu(current_user={"role": ROLE_ADMIN}, input_func=i, print_func=p)

    text = "\n".join(printed)
    assert "Admin-only options:" in text
    assert input_called["count"] == 1


def test_branch_current_user_present_role_student_hits_student_branch_and_calls_input():
    printed = []
    input_called = {"count": 0}

    def p(msg=""):
        printed.append(str(msg))

    def i(_prompt=""):
        input_called["count"] += 1
        return ""

    show_help_menu(current_user={"role": ROLE_STUDENT}, input_func=i, print_func=p)

    text = "\n".join(printed)
    assert "You are logged in as a student." in text
    assert "Admin-only options:" not in text
    assert input_called["count"] == 1


def test_branch_current_user_present_role_unknown_hits_else_branch():
    printed = []

    def p(msg=""):
        printed.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user={"role": "unknown"}, input_func=i, print_func=p)

    text = "\n".join(printed)
    assert "You are currently logged out." in text
    assert "Admin-only options:" not in text
    assert "You are logged in as a student." not in text


def test_branch_current_user_present_but_role_missing_hits_else_branch():
    printed = []

    def p(msg=""):
        printed.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user={"user_id": 99}, input_func=i, print_func=p)

    text = "\n".join(printed)
    assert "You are currently logged out." in text
