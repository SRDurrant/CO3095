def test_log_error_concolic(tmp_path):
    from app.system_log import log_error
    import app.system_log

    log_file = tmp_path / "system.log"
    app.system_log.LOG_FILE = str(log_file)

    concrete_message = "Disk failure"
    log_error(concrete_message)

    content = log_file.read_text()

    # Concrete assertion
    assert concrete_message in content

    # Symbolic reasoning: any message M must appear in output
    assert "[ERROR]" in content