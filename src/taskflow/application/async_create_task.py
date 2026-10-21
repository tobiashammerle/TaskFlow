from datetime import date
from uuid import UUID

from taskflow.async_unit_of_work import AsyncUnitOfWork
from taskflow.exceptions import DuplicateTaskError
from taskflow.priority import Priority
from taskflow.task import Task


class AsyncCreateTask:
    def __init__(self, uow: AsyncUnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self,
        title: str,
        owner_id: UUID,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        async with self.uow:
            tasks = await self.uow.tasks.get_all()
            if any(
                task.title.casefold() == title.casefold() and task.owner_id == owner_id
                for task in tasks
            ):
                raise DuplicateTaskError(
                    "Eine Aufgabe mit diesem Titel existiert bereits."
                )
            task = Task(
                title=title, owner_id=owner_id, priority=priority, due_date=due_date
            )
            await self.uow.tasks.add(task)
            await self.uow.commit()
            return task
