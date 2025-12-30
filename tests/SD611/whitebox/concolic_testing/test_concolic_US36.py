def test_trending_concolic_paths():
    from app.school_actions import view_trending_schools
    from app.data_store import SCHOOLS
    from app.reviews import RATINGS

    # Path 1: score > 0
    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({
        "school_id": 1,
        "name": "Hot",
        "level": "primary",
        "location": "Town"
    })

    RATINGS.append({
        "user_id": 1,
        "school_id": 1,
        "value": 5
    })

    outputs1 = []
    view_trending_schools(print_func=lambda x: outputs1.append(x))
    assert any("Hot" in o for o in outputs1)

    # Path 2: score == 0
    RATINGS.clear()
    outputs2 = []
    view_trending_schools(print_func=lambda x: outputs2.append(x))
    assert any("No" in o for o in outputs2) or any("activity" in o.lower() for o in outputs2)