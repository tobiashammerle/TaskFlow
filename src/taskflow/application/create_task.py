from datetime import date

from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.task_repository import TaskRepository


class CreateTask:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        task = Task(title=title, priority=priority, due_date=due_date)
        self.repository.add(task)
        return task
