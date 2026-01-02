from app.system_log import log_event
import app.system_log as system_log

def test_log_event_empty_message_boundary(tmp_path):

    system_log.LOG_FILE = tmp_path / "system.log"

    log_event("")
    "tests empty string being lowest bound"
    content = system_log.LOG_FILE.read_text()
    assert "[INFO]" in content
