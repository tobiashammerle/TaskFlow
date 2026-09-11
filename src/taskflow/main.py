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
from taskflow.unit_of_work_factory import create_unit_of_work

logger = logging.getLogger(__name__)


def main() -> None:
    """Startet die TaskFlow-Anwendung."""
    load_dotenv()
    configure_logging()
    logger.info("TaskFlow gestartet")

    repository_type = load_repository_type(Path("settings.ini"))
    uow = create_unit_of_work(repository_type)
    create_task = CreateTask(uow)
    complete_task = CompleteTask(uow)
    remove_task = RemoveTask(uow)
    get_tasks = GetTasks(uow)

    run_cli(create_task, complete_task, remove_task, get_tasks)
    logger.info("TaskFlow beendet")


if __name__ == "__main__":
    main()
