import random
from app.admin_actions import export_top_schools_report
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_export_random_ratings(tmp_path):

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(10):
        SCHOOLS.append({"school_id": i, "name": f"S{i}", "level": "primary", "location": "X"})
        RATINGS.append({"user_id": i, "school_id": str(i), "value": random.randint(1, 5)})

    file_path = tmp_path / "report.txt"
    assert export_top_schools_report(str(file_path)) is True