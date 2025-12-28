from datetime import datetime

LOG_FILE = "system.log"


def log_event(message: str) -> None:
    """
    Logs a normal system event (info-level).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[INFO] {timestamp} - {message}\n")


def log_error(message: str) -> None:
    """
    Logs an error event.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ERROR] {timestamp} - {message}\n")