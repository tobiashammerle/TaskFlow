from uuid import UUID

from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from taskflow.task_repository import TaskRepository


class CompleteTask:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError("Task not found")
        task.complete()
        self.repository.update(task)
        return task
