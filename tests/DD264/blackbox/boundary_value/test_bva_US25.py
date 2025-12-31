from app.access_control import user_has_role, check_access


def test_user_has_role_empty_required_roles_boundary():
    user = {"user_id": 1, "role": "admin"}
    assert user_has_role(user, []) is False


def test_user_has_role_missing_role_boundary():
    user = {"user_id": 1}
    assert user_has_role(user, ["admin"]) is False


def test_check_access_current_user_none_boundary_prints_and_denies():
    printed = []

    ok = check_access(
        current_user=None,
        required_roles=["admin"],
        print_func=lambda s: printed.append(s),
    )
    assert ok is False
    # should show both messages due to current implementation flow
    assert any("must be logged in" in x.lower() for x in printed)
    assert not any("do not have permission" in x.lower() for x in printed)
