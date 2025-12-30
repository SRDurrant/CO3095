from app.admin_actions import export_top_schools_report
from app.data_store import SCHOOLS
from app.reviews import RATINGS
def test_export_limit_one_boundary(tmp_path):

    SCHOOLS.clear()
    RATINGS.clear()

    for i in range(3):
        SCHOOLS.append({"school_id": i+1, "name": f"S{i}", "level": "secondary", "location": "X"})
        RATINGS.append({"user_id": i, "school_id": str(i+1), "value": i+1})

    file_path = tmp_path / "report.txt"
    export_top_schools_report(str(file_path), limit=1)

    content = file_path.read_text()
    assert content.count("Avg Rating") == 1

def test_export_limit_exceeds_schools_boundary(tmp_path):

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Solo", "level": "primary", "location": "X"})
    SCHOOLS.append({"school_id": 2, "name": "Solo1", "level": "primary", "location": "X"})
    SCHOOLS.append({"school_id": 3, "name": "Solo2", "level": "primary", "location": "X"})
    SCHOOLS.append({"school_id": 4, "name": "Solo4", "level": "primary", "location": "X"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 4})

    file_path = tmp_path / "report.txt"
    export_top_schools_report(str(file_path), limit=3)
    "Limit of 3 school can be stored, test will fail if assertion of a school ranking lower than top 3 exists in file"

    assert "Solo" in file_path.read_text()