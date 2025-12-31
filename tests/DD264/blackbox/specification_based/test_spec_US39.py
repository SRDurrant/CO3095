"""
US39 - Black-Box Tests (Specification-Based)

Technique: Specification-based testing
- Derive tests from US39 user story requirements and displayed help content.
- Verify visible outputs and role-specific sections.
"""

from app.help_menu import show_help_menu
from app.access_control import ROLE_ADMIN, ROLE_STUDENT


def _run_help(current_user):
    printed = []

    def fake_print(msg=""):
        printed.append(str(msg))

    def fake_input(_prompt=""):
        return ""

    show_help_menu(current_user=current_user, input_func=fake_input, print_func=fake_print)
    return "\n".join(printed), printed


def test_us39_help_menu_always_shows_header_and_general_navigation():
    text, lines = _run_help(None)
    assert "=== Help Menu ===" in text
    assert "General navigation:" in text
    assert "- Enter the number of a menu option to run it." in text
    assert "- Enter '0' in most sub-menus to cancel/return." in text


def test_us39_help_menu_always_shows_standard_main_menu_options():
    text, _ = _run_help(None)
    assert "Main menu options (standard):" in text
    assert "1. Register new user" in text
    assert "2. Login/Logout" in text
    assert "3. Reset Password" in text
    assert "4. Help Menu" in text
    assert "5. View Schools" in text
    assert "6. View School Rankings" in text
    assert "7. View Top Schools by Category" in text
    assert "8. Search for Schools" in text
    assert "9. View Trending Schools" in text
    assert "10. Compare Two Schools" in text
    assert "0. Exit" in text


def test_us39_help_menu_always_mentions_user_actions_inside_school_menus():
    text, _ = _run_help(None)
    assert "User actions inside school menus:" in text
    assert "- View School Profile" in text
    assert "- Filter Schools" in text
    assert "- Sort Schools" in text


def test_us39_logged_out_user_sees_logged_out_message_and_login_hint():
    text, _ = _run_help(None)
    assert "You are currently logged out." in text
    assert "Login to access student/admin features where applicable." in text
    assert "Admin-only options:" not in text
    assert "You are logged in as a student." not in text


def test_us39_student_user_sees_student_message_and_no_admin_block():
    current_user = {"user_id": 2, "username": "student", "role": ROLE_STUDENT}
    text, _ = _run_help(current_user)
    assert "You are logged in as a student." in text
    assert "Admin-only options:" not in text
    assert "Note: Admin-only actions require you to be logged in as an admin account." not in text


def test_us39_admin_user_sees_admin_only_options_block():
    current_user = {"user_id": 1, "username": "admin", "role": ROLE_ADMIN}
    text, _ = _run_help(current_user)
    assert "Admin-only options:" in text

    assert "11. Add New School (Admin Only)" in text
    assert "12. Delete School (Admin Only)" in text
    assert "13. Update School (Admin Only)" in text
    assert "14. Display Registered Users (Admin Only)" in text
    assert "15. Delete Selected User (Admin Only)" in text
    assert "16. Delete a Comment (Admin Only)" in text
    assert "17. View System Statistics (Admin Only)" in text
    assert "18. Export Top Schools Report (Admin Only)" in text
    assert "19. View Top Contributors (Admin Only)" in text
    assert "Note: Admin-only actions require you to be logged in as an admin account." in text


def test_us39_admin_user_does_not_get_logged_out_or_student_messages():
    current_user = {"user_id": 1, "username": "admin", "role": ROLE_ADMIN}
    text, _ = _run_help(current_user)
    assert "You are currently logged out." not in text
    assert "You are logged in as a student." not in text


def test_us39_student_user_does_not_get_logged_out_message():
    current_user = {"user_id": 2, "username": "student", "role": ROLE_STUDENT}
    text, _ = _run_help(current_user)
    assert "You are currently logged out." not in text
