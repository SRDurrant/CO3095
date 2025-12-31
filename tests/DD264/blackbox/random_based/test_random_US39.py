"""
US39 - Black-Box Tests (Random-Based)

Technique: Random-based testing
- Generate random current_user shapes and role values.
- Assert key invariants:
  * header always present
  * standard menu block always present
  * admin block present IFF role == 'admin'
  * student message present IFF role == 'student'
"""

import random
import string

from app.help_menu import show_help_menu
from app.access_control import ROLE_ADMIN, ROLE_STUDENT

def _run(current_user):
    out = []

    def p(msg=""):
        out.append(str(msg))

    def i(_prompt=""):
        return ""

    show_help_menu(current_user=current_user, input_func=i, print_func=p)
    return "\n".join(out)


def _rand_role():
    choices = [ROLE_ADMIN, ROLE_STUDENT, "", None, "ADMIN", "student ", "moderator", "guest"]
    if random.random() < 0.3:
        return "".join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 12)))
    return random.choice(choices)


def _rand_user():
    if random.random() < 0.2:
        return None
    user = {}
    if random.random() < 0.7:
        user["user_id"] = random.randint(1, 999)
    if random.random() < 0.7:
        user["username"] = "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, 10)))
    if random.random() < 0.8:
        user["role"] = _rand_role()
    return user


def test_random_invariants_over_many_trials():
    random.seed(1337)
    for _ in range(200):
        u = _rand_user()
        text = _run(u)

        assert "=== Help Menu ===" in text
        assert "Main menu options (standard):" in text
        assert "General navigation:" in text

        role = None
        if u:
            role = u.get("role")

        if role == ROLE_ADMIN:
            assert "Admin-only options:" in text
            assert "You are currently logged out." not in text
            assert "You are logged in as a student." not in text
        elif role == ROLE_STUDENT:
            assert "You are logged in as a student." in text
            assert "Admin-only options:" not in text
            assert "You are currently logged out." not in text
        else:
            assert "You are currently logged out." in text
            assert "Admin-only options:" not in text
            assert "You are logged in as a student." not in text
