from pathlib import Path

from taskflow.config import REPOSITORY
from taskflow.exceptions import ConfigurationError
from taskflow.json_task_repository import JsonTaskRepository
from taskflow.repository_type import RepositoryType
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_repository import TaskRepository


def create_repository() -> TaskRepository:
    if REPOSITORY == RepositoryType.SQLITE:
        repository = SqliteTaskRepository(Path("tasks.db"))
        repository.initialize_database()
        return repository
    if REPOSITORY == RepositoryType.JSON:
        return JsonTaskRepository(Path("tasks.json"))
    raise ConfigurationError(f"Unbekanntes Repository: {REPOSITORY}")


