import logging
from pathlib import Path


def configure_logging() -> None:
    """Konfiguriert das Logging für TaskFlow."""
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
        handlers=[
            logging.FileHandler(log_directory / "taskflow.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
