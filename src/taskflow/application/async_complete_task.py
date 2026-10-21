from uuid import UUID

from taskflow.async_unit_of_work import AsyncUnitOfWork
from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task


class AsyncCompleteTask:
    def __init__(self, uow: AsyncUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, task_id: UUID, owner_id: UUID | None = None) -> Task:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if task is None:
                raise TaskNotFoundError("Task nicht gefunden.")
            if owner_id is not None and task.owner_id != owner_id:
                raise TaskNotFoundError("Task nicht gefunden.")
            task.complete()
            await self.uow.tasks.update(task)
            await self.uow.commit()
            return task
