from pathlib import Path
from taskflow.repository_type import RepositoryType
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.json_task_repository import JsonTaskRepository
from taskflow.task_repository import TaskRepository
from taskflow.config import REPOSITORY
from taskflow.exceptions import ConfigurationError

def create_repository() -> TaskRepository:
    if REPOSITORY == RepositoryType.SQLITE:
        repository = SqliteTaskRepository(Path("tasks.db"))
        repository.initialize_database()
        return repository
    if REPOSITORY == RepositoryType.JSON:
        return JsonTaskRepository(Path("tasks.json"))
    raise ConfigurationError(f"Unbekanntes Repository: {REPOSITORY}")


