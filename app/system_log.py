from datetime import datetime

LOG_FILE = "system.log"


def log_event(message: str) -> None:
    """
    Writes an info-level system event message to the log file.

    Inputs:
        message (str): Message to be logged

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[INFO] {timestamp} - {message}\n")


def log_error(message: str) -> None:
    """
    Writes an error-level system message to the log file.

    Inputs:
        message (str): Message to be logged as an error

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ERROR] {timestamp} - {message}\n")