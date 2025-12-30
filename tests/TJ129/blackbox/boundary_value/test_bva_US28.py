"""
Black-box boundary value tests for US28 - View Favourite Schools

Focus:
- boundary: user has exactly 0 favourites
- boundary: user has exactly 1 favourite
- boundary: favourites belong to other users (should not display)
"""

from app.reviews import view_favourite_schools, FAVOURITES
from app.data_store import set_current_user, clear_current_user


def reset_state():
    FAVOURITES.clear()
    clear_current_user()


def run_view():
    outputs = []

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    ok, result = view_favourite_schools(input_func=lambda _: "", print_func=fake_print)
    return ok, result, outputs


def test_boundary_zero_favourites():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    ok, result, outputs = run_view()
    assert ok is True
    assert result == []
    assert any("no favourite" in line.lower() for line in outputs)


def test_boundary_one_favourite():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    FAVOURITES.append({"user_id": 1, "school_id": "99"})
    ok, result, outputs = run_view()
    assert ok is True
    assert len(result) == 1
    assert any("- 99" in line for line in outputs)


def test_boundary_other_users_favourites_not_shown():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    FAVOURITES.append({"user_id": 2, "school_id": "1"})  # someone else
    ok, result, outputs = run_view()
    assert ok is True
    assert result == []
    assert any("no favourite" in line.lower() for line in outputs)
