from uuid import UUID

from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from taskflow.unit_of_work import UnitOfWork


class CompleteTask:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(self, task_id: UUID) -> Task:
        with self.uow:
            task = self.uow.tasks.get_by_id(task_id)
            if task is None:
                raise TaskNotFoundError("Task nicht gefunden.")
            task.complete()
            self.uow.tasks.update(task)
            self.uow.commit()
            return task
