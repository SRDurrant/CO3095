from app.admin_actions import export_top_schools_report
from app.data_store import SCHOOLS
from app.reviews import RATINGS

def test_export_top_schools_success(tmp_path, capsys):

    SCHOOLS.clear()
    RATINGS.clear()

    SCHOOLS.append({"school_id": 1, "name": "Alpha", "level": "primary", "location": "X"})
    RATINGS.append({"user_id": 1, "school_id": "1", "value": 5})

    file_path = tmp_path / "report.txt"
    result = export_top_schools_report(str(file_path))

    assert result is True
    assert file_path.exists()
    assert "Alpha" in file_path.read_text()

def test_export_no_schools(capsys):

    SCHOOLS.clear()

    result = export_top_schools_report()
    out = capsys.readouterr().out

    assert result is False
    assert "No schools available to export" in out