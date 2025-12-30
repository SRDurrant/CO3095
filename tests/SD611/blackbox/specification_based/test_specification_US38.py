from app.system_log import log_event, log_error
import app.system_log as system_log

def test_log_event_writes_info(tmp_path):

    system_log.LOG_FILE = tmp_path / "system.log"

    log_event("System started")

    content = system_log.LOG_FILE.read_text()
    assert "[INFO]" in content
    assert "System started" in content

def test_log_error_writes_error(tmp_path):

    system_log.LOG_FILE = tmp_path / "system.log"

    log_error("Unexpected failure")

    content = system_log.LOG_FILE.read_text()
    assert "[ERROR]" in content
    assert "Unexpected failure" in content