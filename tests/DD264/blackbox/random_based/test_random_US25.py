import random
from app.data_store import set_current_user, get_current_user, clear_current_user


def test_session_random_user_dicts():
    for _ in range(25):
        uid = random.randint(1, 10_000)
        user = {"user_id": uid, "username": f"u{uid}", "role": random.choice(["student", "admin"])}

        set_current_user(user)
        assert get_current_user()["user_id"] == uid

        clear_current_user()
        assert get_current_user() is None
