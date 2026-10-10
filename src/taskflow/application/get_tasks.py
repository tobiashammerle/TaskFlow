from uuid import UUID

from taskflow.task import Task
from taskflow.unit_of_work import UnitOfWork


class GetTasks:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(self, owner_id: UUID | None = None) -> list[Task]:
        with self.uow:
            if owner_id is None:
                return self.uow.tasks.get_all()
            return self.uow.tasks.get_all_by_owner(owner_id)
