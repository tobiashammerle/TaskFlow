import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from taskflow.exceptions import ConfigurationError

load_dotenv()


def configure_logging() -> None:
    """Konfiguriert das Logging für TaskFlow."""
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        log_level = getattr(logging, log_level_name)
    except AttributeError as error:
        raise ConfigurationError(f"Ungültiges LOG_LEVEL: {log_level_name}") from error

    logging.basicConfig(
        level=log_level,
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
        handlers=[
            logging.FileHandler(log_directory / "taskflow.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
