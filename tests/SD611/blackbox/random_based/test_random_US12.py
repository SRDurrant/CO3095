import random

from app.data_store import SCHOOLS
from app.reviews import RATINGS
from app.school_actions import view_top_schools


def test_randomized_top_schools():
    """
    Random-based testing for US12.
    Ensures no crashes and valid output.
    """
    SCHOOLS.clear()
    RATINGS.clear()

    levels = ["primary", "secondary"]
    num_schools = random.randint(1, 20)

    for i in range(1, num_schools + 1):
        SCHOOLS.append({
            "school_id": i,
            "name": f"School{i}",
            "level": random.choice(levels),
            "location": "X"
        })

        # Random number of ratings per school
        for _ in range(random.randint(0, 5)):
            RATINGS.append({
                "user_id": random.randint(1, 50),
                "school_id": str(i),
                "value": random.randint(1, 5)
            })

    outputs = []
    view_top_schools(limit=random.randint(1, 5), print_func=lambda x: outputs.append(x))

    # Assertions focus on safety & structure
    assert len(outputs) > 0
    assert any("Top" in line for line in outputs)