from pathlib import Path
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.json_task_repository import JsonTaskRepository
from taskflow.task_repository import TaskRepository
from taskflow.config import USE_SQLITE

def create_repository() -> TaskRepository:
    if USE_SQLITE:
        repository = SqliteTaskRepository(Path("tasks.db"))
        repository.initialize_database()
        return repository
    return JsonTaskRepository(Path("tasks.json"))

