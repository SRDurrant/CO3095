from app.access_control import user_has_role


def test_user_has_role_symbolic_small_domain():
    users = [
        None,
        {"user_id": 1},
        {"user_id": 1, "role": None},
        {"user_id": 1, "role": "student"},
        {"user_id": 1, "role": "admin"},
    ]
    required_sets = [
        [],
        ["student"],
        ["admin"],
        ["student", "admin"],
    ]

    for u in users:
        for req in required_sets:
            ok = user_has_role(u, req)
            if u is None:
                assert ok is False
            else:
                role = u.get("role")
                assert ok is (role in req)
