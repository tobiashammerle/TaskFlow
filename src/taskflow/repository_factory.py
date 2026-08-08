from pathlib import Path
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_repository import TaskRepository

def create_repository() -> TaskRepository:
    repository = SqliteTaskRepository(Path("taks.db"))
    repository.initialize_database()
    return repository
