import random
import string
from app.admin_actions import list_all_users
from app.data_store import USERS

def test_view_users_random_blackbox():
    """
    Random testing: randomly generate users and ensure listing does not crash.
    """

    USERS.clear()

    num_users = random.randint(1, 10)

    for i in range(num_users):
        USERS.append({
            "user_id": i,
            "username": ''.join(random.choices(string.ascii_letters, k=8)),
            "password": 'b',
            "role": random.choice(["admin", "student"])
        })

    outputs = []

    def fake_print(msg):
        outputs.append(msg)

    list_all_users(print_func=fake_print)

    # Basic black-box oracle: header printed + some users listed
    assert "=== Registered Users ===" in outputs[0]
    assert len(outputs) == num_users + 1