"""
White-box tests for US14 - Rate a School.
These tests focus on exercising different internal branches in rate_school.
"""
from app.reviews import rate_school, clear_ratings, set_rating, RATINGS
from app.data_store import set_current_user, clear_current_user

def test_branch_empty_school_id_reprompts():
    """
    Branch: empty school ID should cause a re-prompt (not immediate failure).
    We simulate this by giving an empty string first, then a valid ID and rating.
    """
    clear_ratings()
    clear_current_user()
    user = {"user_id": 10, "username": "tester", "password": "pw", "role": "student"}
    set_current_user(user)

    inputs = iter([
        "",    
        "SCH-10",   
        "5",        
    ])

    outputs = []
    def fake_input(prompt: str) -> str:
        return next(inputs, "")
    def fake_print(message: str) -> None:
        outputs.append(message)
    success, result = rate_school(input_func=fake_input, print_func=fake_print)

    assert success is True
    assert result["school_id"] == "SCH-10"
    assert any("School ID cannot be empty" in line for line in outputs)

def test_branch_update_existing_rating():
    """
    Branch: updating an existing rating rather than creating a new one.
    """
    clear_ratings()
    clear_current_user()

    user = {"user_id": 20, "username": "updater", "password": "pw", "role": "student"}
    set_current_user(user)

    set_rating(user_id=20, school_id="SCH-20", value=2)
    assert len(RATINGS) == 1

    inputs = iter([
        "SCH-20",  
        "5",       
    ])

    def fake_input(prompt: str) -> str:
        return next(inputs, "")

    def fake_print(message: str) -> None:
        pass
    success, result = rate_school(input_func=fake_input, print_func=fake_print)
    assert success is True
    assert len(RATINGS) == 1  
    assert result["value"] == 5
