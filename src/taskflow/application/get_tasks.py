from taskflow.task import Task
from taskflow.unit_of_work import UnitOfWork


class GetTasks:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(self) -> list[Task]:
        with self.uow:
            return self.uow.tasks.get_all()
