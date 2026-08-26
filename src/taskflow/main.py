import logging

from dotenv import load_dotenv

from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.get_tasks import GetTasks
from taskflow.application.remove_task import RemoveTask
from taskflow.cli import run_cli
from taskflow.logging_config import configure_logging
from taskflow.repository_factory import create_repository

logger = logging.getLogger(__name__)


def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    load_dotenv()
    configure_logging()
    logger.info("TaskFlow gestartet")

    repository = create_repository()
    create_task = CreateTask(repository)
    complete_task = CompleteTask(repository)
    remove_task = RemoveTask(repository)
    get_tasks = GetTasks(repository)

    run_cli(create_task, complete_task, remove_task, get_tasks)
    logger.info("TaskFlow beendet")


if __name__ == "__main__":
    main()
