"""
Black-box tests for US26 - Favourite a School (Specification Based)

These tests validate observable behaviour:
- Requires login
- Requires student role
- Allows cancel with '0'
- Adds favourite successfully
- Prevents duplicates
"""

from app.reviews import favourite_school, FAVOURITES, clear_favourites
from app.data_store import set_current_user, clear_current_user


def run_favourite_with_inputs(example_user, inputs):
    clear_favourites()
    clear_current_user()

    if example_user is not None:
        set_current_user(example_user)

    inputs_iter = iter(inputs)
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success, result = favourite_school(input_func=fake_input, print_func=fake_print)
    return success, result, outputs


def test_favourite_requires_login():
    success, result, outputs = run_favourite_with_inputs(None, [])
    assert success is False
    assert "logged in" in str(result).lower()
    assert len(FAVOURITES) == 0


def test_favourite_requires_student_role():
    admin = {"user_id": 1, "username": "admin", "password": "pw", "role": "admin"}
    success, result, outputs = run_favourite_with_inputs(admin, ["SCH-1"])
    assert success is False
    assert "only students" in str(result).lower()
    assert len(FAVOURITES) == 0


def test_favourite_cancelled_by_user():
    student = {"user_id": 2, "username": "stud", "password": "pw", "role": "student"}
    success, result, outputs = run_favourite_with_inputs(student, ["0"])
    assert success is False
    assert "cancelled" in str(result).lower()
    assert len(FAVOURITES) == 0


def test_favourite_success_adds_record():
    student = {"user_id": 3, "username": "alice", "password": "pw", "role": "student"}
    success, result, outputs = run_favourite_with_inputs(student, ["SCH-123"])
    assert success is True
    assert isinstance(result, dict)
    assert result["user_id"] == 3
    assert result["school_id"] == "SCH-123"
    assert "created_at" in result
    assert len(FAVOURITES) == 1


def test_favourite_duplicate_does_not_duplicate():
    student = {"user_id": 4, "username": "bob", "password": "pw", "role": "student"}

    # first add
    success1, result1, _ = run_favourite_with_inputs(student, ["SCH-999"])
    assert success1 is True
    assert len(FAVOURITES) == 1

    clear_favourites()
    clear_current_user()
    set_current_user(student)

    # pre-seed favourite
    from app.reviews import add_favourite_record
    add_favourite_record(student["user_id"], "SCH-999")

    inputs_iter = iter(["SCH-999"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs_iter, "")

    def fake_print(message: str) -> None:
        outputs.append(message)

    success2, result2 = favourite_school(input_func=fake_input, print_func=fake_print)

    assert success2 is True
    assert len(FAVOURITES) == 1
    assert any("already" in line.lower() for line in outputs)
