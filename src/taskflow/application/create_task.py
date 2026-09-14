from datetime import date

from taskflow.exceptions import DuplicateTaskError
from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.unit_of_work import UnitOfWork


class CreateTask:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        with self.uow:
            tasks = self.uow.tasks.get_all()
            if any(task.title.casefold() == title.casefold() for task in tasks):
                raise DuplicateTaskError(
                    "Eine Aufgabe mit diesem Titel existiert bereits."
                )
            task = Task(title=title, priority=priority, due_date=due_date)
            self.uow.tasks.add(task)
            self.uow.commit()
            return task
