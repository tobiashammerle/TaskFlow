import logging
from pathlib import Path

from dotenv import load_dotenv

from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.get_tasks import GetTasks
from taskflow.application.remove_task import RemoveTask
from taskflow.cli import run_cli
from taskflow.config import load_repository_type
from taskflow.logging_config import configure_logging
from taskflow.repository_factory import create_repository

logger = logging.getLogger(__name__)


def build_use_cases():
    repository_type = load_repository_type(Path("settings.ini"))
    repository = create_repository(repository_type)
    create_task = CreateTask(repository)
    complete_task = CompleteTask(repository)
    remove_task = RemoveTask(repository)
    get_tasks = GetTasks(repository)
    return create_task, complete_task, remove_task, get_tasks


def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    load_dotenv()
    configure_logging()
    logger.info("TaskFlow gestartet")

    create_task, complete_task, remove_task, get_tasks = build_use_cases()

    run_cli(create_task, complete_task, remove_task, get_tasks)
    logger.info("TaskFlow beendet")


if __name__ == "__main__":
    main()
