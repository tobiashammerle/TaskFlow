from datetime import date

from taskflow.exceptions import DuplicateTaskError
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
        tasks = self.repository.get_all()
        if any(task.title.casefold() == title.casefold() for task in tasks):
            raise DuplicateTaskError("Eine Aufgabe mit diesem Titel existiert bereits.")
        task = Task(title=title, priority=priority, due_date=due_date)
        self.repository.add(task)
        return task
