from uuid import UUID

from taskflow.async_unit_of_work import AsyncUnitOfWork
from taskflow.task import Task


class AsyncGetTasks:
    def __init__(self, uow: AsyncUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, owner_id: UUID | None = None) -> list[Task]:
        async with self.uow:
            if owner_id is None:
                return await self.uow.tasks.get_all()
            return await self.uow.tasks.get_all_by_owner(owner_id)
