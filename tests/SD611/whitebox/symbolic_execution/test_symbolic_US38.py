import app.system_log as sl
def test_log_event_format_symbolic(tmp_path):

    sl.LOG_FILE = tmp_path / "system.log"

    message = "X"
    sl.log_event(message)

    content = sl.LOG_FILE.read_text()

    assert content.startswith("[INFO]")
    assert " - X" in content