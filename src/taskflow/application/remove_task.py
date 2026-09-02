from uuid import UUID

from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from taskflow.task_repository import TaskRepository


class RemoveTask:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, task_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError("Task nicht gefunden.")
        self.repository.delete(task_id)
        return task
