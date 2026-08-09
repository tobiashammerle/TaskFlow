from taskflow.logging_config import configure_logging
import logging
from taskflow.repository_factory import create_repository
from taskflow.task_service import TaskService
from taskflow.cli import run_cli

logger = logging.getLogger(__name__)


def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    configure_logging()
    logger.info("TaskFlow gestartet")

    repository = create_repository()
    task_service = TaskService(repository)

    run_cli(task_service)
    logger.info("TaskFlow beendet")

if __name__ == "__main__":
    main()