from app.admin_actions import list_all_users
from app.data_store import USERS


def test_loop_single_iteration():
    """
    Loop test: exactly one user in USERS triggers loop exactly once.
    """

    USERS.clear()
    USERS.append({
        "user_id": 1,
        "username": "single-user",
        "role": "student"
    })

    out = []
    list_all_users(print_func=out.append)

    assert len(out) == 2    # header + one printed user line
    assert "single-user" in out[1]


def test_loop_multiple_iterations():
    """
    Loop test: multiple users → multiple loop iterations.
    """

    USERS.clear()
    USERS.extend([
        {"user_id": 1, "username": "u1", "role": "admin"},
        {"user_id": 2, "username": "u2", "role": "student"},
        {"user_id": 3, "username": "u3", "role": "student"},
    ])

    out = []
    list_all_users(print_func=out.append)

    # header + 3 user lines
    assert len(out) == 4
    assert "u3" in out[3]