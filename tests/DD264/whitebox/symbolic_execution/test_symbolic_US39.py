"""
US39 - White-Box Tests (Symbolic Execution Style)

Technique: Symbolic execution (manual/path-condition derived)
We derive path conditions for show_help_menu():

Let U = current_user
Let R = role (if U truthy then U.get("role") else None)

Paths:
P1: U is falsy -> role = None -> logged out branch
P2: U is truthy AND R='admin' -> admin branch
P3: U is truthy AND R='student' -> student branch
P4: U is truthy AND R not in {'admin','student'} -> logged out branch

These tests explicitly satisfy each path condition.
"""

from app.help_menu import show_help_menu


def _capture(user):
    out = []

    def p(msg=""):
        out.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user=user, input_func=i, print_func=p)
    return "\n".join(out)


def test_symbolic_P1_U_falsy_logged_out():
    # Path condition: U is falsy => role = None => else branch
    text = _capture(None)
    assert "You are currently logged out." in text


def test_symbolic_P2_U_truthy_R_admin_admin_block():
    # Path condition: U truthy AND R == 'admin'
    text = _capture({"role": "admin"})
    assert "Admin-only options:" in text


def test_symbolic_P3_U_truthy_R_student_student_block():
    # Path condition: U truthy AND R == 'student'
    text = _capture({"role": "student"})
    assert "You are logged in as a student." in text
    assert "Admin-only options:" not in text


def test_symbolic_P4_U_truthy_R_other_logged_out():
    # Path condition: U truthy AND R not in {'admin','student'}
    text = _capture({"role": "moderator"})
    assert "You are currently logged out." in text
    assert "Admin-only options:" not in text
    assert "You are logged in as a student." not in text


def test_symbolic_P4b_U_truthy_R_missing_logged_out():
    # Another satisfying assignment for P4: U truthy AND role missing => R=None
    text = _capture({"user_id": 10})
    assert "You are currently logged out." in text
