import logging
import os
from pathlib import Path

from taskflow.exceptions import ConfigurationError


def configure_logging() -> None:
    """Konfiguriert das Logging für TaskFlow."""
    log_to_file = os.environ.get("LOG_TO_FILE", "true").lower() == "true"
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        log_level = getattr(logging, log_level_name)
    except AttributeError as error:
        raise ConfigurationError(f"Ungültiges LOG_LEVEL: {log_level_name}") from error

    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_to_file:
        log_directory = Path("logs")
        log_directory.mkdir(exist_ok=True)
        handlers.append(
            logging.FileHandler(log_directory / "taskflow.log", encoding="utf-8")
        )

    logging.basicConfig(
        level=log_level,
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
        handlers=handlers,
    )
