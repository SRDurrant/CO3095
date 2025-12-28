from app.admin_actions import export_top_schools_report
from app.data_store import SCHOOLS

def test_export_empty_summary_branch(capsys):

    SCHOOLS.clear()

    result = export_top_schools_report()
    assert result is False

def test_export_file_write_failure(monkeypatch, capsys):

    def mock_open(*args, **kwargs):
        raise IOError("Disk error")

    monkeypatch.setattr("builtins.open", mock_open)

    result = export_top_schools_report("invalid.txt")
    out = capsys.readouterr().out

    assert result is False
    assert "Failed to export report" in out

