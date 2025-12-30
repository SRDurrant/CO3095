"""
Black-box specification-based tests for US28 - View Favourite Schools

Verifies:
- login required
- cancel works
- message when no favourites
- favourites are listed when present
"""

from app.reviews import view_favourite_schools, FAVOURITES
from app.data_store import set_current_user, clear_current_user


def reset_state():
    FAVOURITES.clear()
    clear_current_user()


def run_view(inputs):
    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(msg: str) -> None:
        outputs.append(msg)

    ok, result = view_favourite_schools(input_func=fake_input, print_func=fake_print)
    return ok, result, outputs


def test_view_favourites_requires_login():
    reset_state()
    ok, result, outputs = run_view([""])
    assert ok is False
    assert "logged in" in str(result).lower()
    assert any("logged in" in line.lower() for line in outputs)


def test_view_favourites_cancel():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    ok, result, outputs = run_view(["0"])
    assert ok is False
    assert "cancelled" in str(result).lower()
    assert any("cancelled" in line.lower() for line in outputs)


def test_view_favourites_none_message():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    ok, result, outputs = run_view([""])
    assert ok is True
    assert result == []
    assert any("no favourite" in line.lower() for line in outputs)


def test_view_favourites_lists_items():
    reset_state()
    set_current_user({"user_id": 1, "username": "u", "role": "student"})
    FAVOURITES.append({"user_id": 1, "school_id": "1"})
    FAVOURITES.append({"user_id": 1, "school_id": "2"})

    ok, result, outputs = run_view([""])
    assert ok is True
    assert isinstance(result, list)
    assert len(result) == 2
    assert any("- 1" in line for line in outputs)
    assert any("- 2" in line for line in outputs)
