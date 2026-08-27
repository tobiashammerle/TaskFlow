from pathlib import Path

from taskflow.exceptions import ConfigurationError
from taskflow.json_task_repository import JsonTaskRepository
from taskflow.repository_type import RepositoryType
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_repository import TaskRepository


def create_repository(repository_type: RepositoryType) -> TaskRepository:
    if repository_type == RepositoryType.SQLITE:
        repository = SqliteTaskRepository(Path("tasks.db"))
        repository.initialize_database()
        return repository
    if repository_type == RepositoryType.JSON:
        return JsonTaskRepository(Path("tasks.json"))
    raise ConfigurationError(f"Unbekanntes Repository: {repository_type}")
