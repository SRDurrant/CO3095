"""
Black-box Boundary Value tests for US26 - Favourite a School

Boundary cases:
- Empty school_id ("" / whitespace) rejected
- After rejection, user can cancel with '0'
- Minimal valid non-empty ID accepted
"""

from app.reviews import favourite_school, FAVOURITES, clear_favourites
from app.data_store import set_current_user, clear_current_user


def run_favourite(inputs, user):
    clear_favourites()
    clear_current_user()
    set_current_user(user)

    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = favourite_school(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_boundary_empty_school_id_then_cancel():
    user = {"user_id": 10, "username": "u", "password": "pw", "role": "student"}
    success, result, outputs = run_favourite(["", "0"], user)
    assert success is False
    assert "cancelled" in str(result).lower()
    assert any("cannot be empty" in line.lower() for line in outputs)
    assert len(FAVOURITES) == 0


def test_boundary_whitespace_school_id_then_valid():
    user = {"user_id": 11, "username": "u2", "password": "pw", "role": "student"}
    success, result, outputs = run_favourite(["   ", "A"], user)
    assert success is True
    assert result["school_id"] == "A"
    assert len(FAVOURITES) == 1
